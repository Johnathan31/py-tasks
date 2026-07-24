from logging import basicConfig, INFO, StreamHandler, FileHandler


def config_logging() -> None:
    basicConfig(
        level=INFO,
        format="%(asctime)s – %(levelname)s – %(name)s – %(message)s",
        handlers=[
            StreamHandler(),
            FileHandler("app.log")
        ],
        force=True
    )
