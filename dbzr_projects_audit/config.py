from babylon.config import ConfigWrapper, FileConfig


class Config:
    def __init__(self, config: ConfigWrapper):
        self.example = config.get(
            "EXAMPLE_CONFIG_VARIABLE", required=False, fallback="foo"
        )


class EnvironmentConfig(Config):
    def __init__(self) -> None:
        super().__init__(ConfigWrapper(FileConfig(".")))
