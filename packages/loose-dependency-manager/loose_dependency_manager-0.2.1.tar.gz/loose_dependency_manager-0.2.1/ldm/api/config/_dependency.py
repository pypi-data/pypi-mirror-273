from pydantic import BaseModel, Field
from ._scheme import SchemeConfig
from ._installer import InstallerConfig

CONFIG_FILE_NAME = "ldm.yml"


class DependencyConfig(BaseModel):
    schemes: dict[str, SchemeConfig] | None = Field(default_factory=lambda: {})
    dependencies: dict[str, str]
    config: InstallerConfig | None = Field(default_factory=lambda: InstallerConfig())
