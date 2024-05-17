from pydantic import BaseModel, Field


class Author(BaseModel):
    name: str
    email: str


class License(BaseModel):
    text: str = Field(serialization_alias="name")


class Project(BaseModel):
    name: str = "Addebitare Backend"
    version: str = "0.1.0"
    description: str = "Addebitare Backend API Description"
    authors: list[Author] = []
    summary: str = "Addebitare Backend API Summary"
