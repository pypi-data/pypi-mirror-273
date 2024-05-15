import time
from contextlib import asynccontextmanager
from typing import Optional

import infinity_emb
from infinity_emb._optional_imports import CHECK_TYPER, CHECK_UVICORN
from infinity_emb.args import EngineArgs
from infinity_emb.engine import AsyncEmbeddingEngine, AsyncEngineArray
from infinity_emb.fastapi_schemas import docs, errors
from infinity_emb.fastapi_schemas.convert import (
    list_embeddings_to_response,
    to_rerank_response,
)
from infinity_emb.fastapi_schemas.pymodels import (
    OpenAIEmbeddingInput,
    OpenAIEmbeddingResult,
    OpenAIModelInfo,
    RerankInput,
)
from infinity_emb.inference.caching_layer import INFINITY_CACHE_VECTORS
from infinity_emb.log_handler import UVICORN_LOG_LEVELS, logger
from infinity_emb.primitives import (
    Device,
    Dtype,
    InferenceEngine,
    PoolingMethod,
)


def create_server(
    *,
    engine_args_list: list[EngineArgs],
    url_prefix: str = "",
    doc_extra: dict = {},
    redirect_slash: str = "/docs",
    preload_only: bool = False,
):
    """
    creates the FastAPI App
    """
    from fastapi import FastAPI, responses, status
    from prometheus_fastapi_instrumentator import Instrumentator

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        instrumentator.expose(app)  # type: ignore
        app.engine_array = AsyncEngineArray.from_args(engine_args_list)  # type: ignore
        # start in a threadpool
        await app.engine_array.astart()  # type: ignore

        logger.info(
            docs.startup_message(
                host=doc_extra.pop("host", "localhost"),
                port=doc_extra.pop("port", "PORT"),
                prefix=url_prefix,
            )
        )

        if preload_only:
            logger.info(
                f"Preloaded configuration successfully. {engine_args_list} "
                " -> Non-graceful exit ."
            )
            # skip the blocking part
        else:
            # application is blocking here!
            yield
        await app.engine_array.astop()  # type: ignore
        # shutdown!

    app = FastAPI(
        title=docs.FASTAPI_TITLE,
        summary=docs.FASTAPI_SUMMARY,
        description=docs.FASTAPI_DESCRIPTION,
        version=infinity_emb.__version__,
        contact=dict(name="Michael Feil"),
        docs_url="/docs",
        license_info={
            "name": "MIT License",
            "identifier": "MIT",
        },
        lifespan=lifespan,
    )

    instrumentator = Instrumentator().instrument(app)
    app.add_exception_handler(errors.OpenAIException, errors.openai_exception_handler)

    @app.get("/health")
    async def _health() -> dict[str, float]:
        """
        health check endpoint

        Returns:
            dict(unix=float): dict with unix time stamp
        """
        return {"unix": time.time()}

    if redirect_slash:
        from fastapi.responses import RedirectResponse

        assert redirect_slash.startswith("/"), "redirect_slash must start with /"

        @app.get("/")
        async def redirect():
            response = RedirectResponse(url=redirect_slash)
            return response

    @app.get(
        f"{url_prefix}/models",
        response_model=OpenAIModelInfo,
        response_class=responses.ORJSONResponse,
    )
    async def _models():
        """get models endpoint"""
        engine_array: "AsyncEngineArray" = app.engine_array  # type: ignore
        data = []
        for engine in engine_array:
            engine_args = engine.engine_args
            data.append(
                dict(
                    id=engine_args.served_model_name,
                    stats=dict(
                        queue_fraction=engine.overload_status().queue_fraction,
                        queue_absolute=engine.overload_status().queue_absolute,
                        results_pending=engine.overload_status().results_absolute,
                        batch_size=engine_args.batch_size,
                    ),
                    backend=engine_args.engine.name,
                    device=engine_args.device.name,
                )
            )

        return dict(data=data)

    def _resolve_engine(model: str) -> "AsyncEmbeddingEngine":
        try:
            engine: "AsyncEmbeddingEngine" = app.engine_array[model]  # type: ignore
        except IndexError as ex:
            raise errors.OpenAIException(
                f"Invalid model: {ex}",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if engine.is_overloaded():
            raise errors.OpenAIException(
                f"model {model} is currently overloaded",
                code=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        return engine

    @app.post(
        f"{url_prefix}/embeddings",
        response_model=OpenAIEmbeddingResult,
        response_class=responses.ORJSONResponse,
    )
    async def _embeddings(data: OpenAIEmbeddingInput):
        """Encode Embeddings

        ```python
        import requests
        requests.post("http://..:7997/embeddings",
            json={"model":"bge-small-en-v1.5","input":["A sentence to encode."]})
        """
        engine = _resolve_engine(data.model)

        try:
            if isinstance(data.input, str):
                data.input = [data.input]

            logger.debug("[📝] Received request with %s inputs ", len(data.input))
            start = time.perf_counter()

            embedding, usage = await engine.embed(data.input)

            duration = (time.perf_counter() - start) * 1000
            logger.debug("[✅] Done in %s ms", duration)

            res = list_embeddings_to_response(
                embeddings=embedding,
                model=engine.engine_args.served_model_name,
                usage=usage,
            )

            return res
        except Exception as ex:
            raise errors.OpenAIException(
                f"InternalServerError: {ex}",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @app.post(
        f"{url_prefix}/rerank",
        # response_model=RerankResult,
        response_class=responses.ORJSONResponse,
    )
    async def _rerank(data: RerankInput):
        """Encode Embeddings

        ```python
        import requests
        requests.post("http://..:7997/rerank",
            json={"query":"Where is Munich?","texts":["Munich is in Germany."]})
        """
        engine = _resolve_engine(data.model)
        try:
            logger.debug("[📝] Received request with %s docs ", len(data.documents))
            start = time.perf_counter()

            scores, usage = await engine.rerank(
                query=data.query, docs=data.documents, raw_scores=False
            )

            duration = (time.perf_counter() - start) * 1000
            logger.debug("[✅] Done in %s ms", duration)

            if data.return_documents:
                docs = data.documents
            else:
                docs = None

            res = to_rerank_response(
                scores=scores,
                documents=docs,
                model=engine.engine_args.served_model_name,
                usage=usage,
            )

            return res
        except Exception as ex:
            raise errors.OpenAIException(
                f"InternalServerError: {ex}",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return app


def _start_uvicorn(
    model_name_or_path: str = "michaelfeil/bge-small-en-v1.5",
    served_model_name: Optional[str] = None,
    batch_size: int = 32,
    revision: Optional[str] = None,
    trust_remote_code: bool = True,
    url_prefix: str = "",
    host: str = "0.0.0.0",
    port: int = 7997,
    redirect_slash: str = "/docs",
    log_level: UVICORN_LOG_LEVELS = UVICORN_LOG_LEVELS.info.name,  # type: ignore
    engine: InferenceEngine.names_enum() = InferenceEngine.names_enum().torch.name,  # type: ignore # noqa
    model_warmup: bool = True,
    vector_disk_cache: bool = INFINITY_CACHE_VECTORS,
    device: Device.names_enum() = Device.names_enum().auto.name,  # type: ignore
    lengths_via_tokenize: bool = False,
    dtype: Dtype.names_enum() = Dtype.names_enum().auto.name,  # type: ignore
    pooling_method: PoolingMethod.names_enum() = PoolingMethod.names_enum().auto.name,  # type: ignore
    compile: bool = False,
    bettertransformer: bool = True,
    preload_only: bool = False,
):
    """Infinity Embedding API ♾️  cli to start a uvicorn-server instance;
    MIT License; Copyright (c) 2023-now Michael Feil

    Args:
        model_name_or_path, str: Huggingface model, e.g.
            "michaelfeil/bge-small-en-v1.5".
        served_model_name, str: "", e.g. "bge-small-en-v1.5"
        batch_size, int: batch size for forward pass.
        revision: str: revision of the model.
        trust_remote_code, bool: trust remote code.
        url_prefix, str: prefix for api. typically "".
        host, str: host-url, typically either "0.0.0.0" or "127.0.0.1".
        port, int: port that you want to expose.
        redirect_slash, str: redirect to of GET "/". Defaults to "/docs". Empty string to disable.
        log_level: logging level.
            For high performance, use "info" or higher levels. Defaults to "info".
        engine, str: framework that should perform inference.
        model_warmup, bool: perform model warmup before starting the server.
            Defaults to True.
        vector_disk_cache, bool: cache past embeddings in SQL.
            Defaults to False or env-INFINITY_CACHE_VECTORS if set
        device, Device: device to use for inference. Defaults to Device.auto or "auto"
        lengths_via_tokenize: bool: schedule by token usage. Defaults to False.
        dtype, Dtype: data type to use for inference. Defaults to Dtype.auto or "auto"
        pooling_method, PoolingMethod: pooling method to use. Defaults to PoolingMethod.auto or "auto"
        compile, bool: compile model for faster inference. Defaults to False.
        use_bettertransformer, bool: use bettertransformer. Defaults to True.
        preload_only, bool: only preload the model and exit. Defaults to False.
    """
    CHECK_UVICORN.mark_required()
    import uvicorn

    logger.setLevel(log_level.to_int())

    vector_disk_cache_path = (
        f"{engine}_{model_name_or_path.replace('/','_')}" if vector_disk_cache else ""
    )

    engine_args = EngineArgs(
        model_name_or_path=model_name_or_path,
        batch_size=batch_size,
        revision=revision,
        trust_remote_code=trust_remote_code,
        engine=InferenceEngine[engine.value],  # type: ignore
        model_warmup=model_warmup,
        vector_disk_cache_path=vector_disk_cache_path,
        device=Device[device.value],  # type: ignore
        lengths_via_tokenize=lengths_via_tokenize,
        dtype=Dtype[dtype.value],  # type: ignore
        pooling_method=PoolingMethod[pooling_method.value],  # type: ignore
        compile=compile,
        bettertransformer=bettertransformer,
        served_model_name=served_model_name,  # type: ignore
    )

    app = create_server(
        engine_args_list=[engine_args],
        url_prefix=url_prefix,
        doc_extra=dict(host=host, port=port),
        redirect_slash=redirect_slash,
        preload_only=preload_only,
    )
    uvicorn.run(app, host=host, port=port, log_level=log_level.name)


def cli():
    """fires the command line using Python `typer.run()`"""
    CHECK_TYPER.mark_required()
    import typer

    typer.run(_start_uvicorn)


if __name__ == "__main__":
    # for debugging
    cli()
