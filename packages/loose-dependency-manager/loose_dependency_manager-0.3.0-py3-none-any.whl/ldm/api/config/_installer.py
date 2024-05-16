from pydantic import BaseModel, model_validator, Field, AliasChoices


class SequentialConfig(BaseModel):
    pass


class ParallelConfig(BaseModel):
    workers: int = 8


class EnvironmentConfig(BaseModel):
    from_: str | list[str] | None = Field(
        default=".env",
        validation_alias=AliasChoices("from_", "from"),
    )

    @property
    def env_files(self) -> list[str]:
        if self.from_ is None:
            return []
        if isinstance(self.from_, str):
            return [self.from_]
        return self.from_


class InstallerConfig(BaseModel):
    sequential: SequentialConfig | None = None
    parallel: ParallelConfig | None = None
    environment: EnvironmentConfig | None = Field(
        default_factory=lambda: EnvironmentConfig()
    )

    @model_validator(mode="after")
    def validate_config(self):
        if self.sequential is not None and self.parallel is not None:
            raise ValueError("Cannot use both sequential and parallel options")
        if self.sequential is None and self.parallel is None:
            self.parallel = ParallelConfig()
        return self

    @property
    def strategy(self):
        if self.sequential is not None:
            return "sequential"
        return "parallel"
