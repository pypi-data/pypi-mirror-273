from pydantic import BaseModel

from ._extras import Project


class MetadataConfig(BaseModel):
    """Project metadata configuration"""

    project: Project = Project()
