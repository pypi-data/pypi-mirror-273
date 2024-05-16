from pydantic import BaseModel, model_validator


class SequentialConfig(BaseModel):
    pass


class ParallelConfig(BaseModel):
    workers: int = 8


class InstallerConfig(BaseModel):
    sequential: SequentialConfig | None = None
    parallel: ParallelConfig | None = None

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
