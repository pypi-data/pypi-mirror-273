from pydantic import BaseModel, Field, AliasChoices


class SchemeConfig(BaseModel):
    uses: str
    with_: dict | None = Field(
        default=None,
        validation_alias=AliasChoices("with_", "with"),
    )
