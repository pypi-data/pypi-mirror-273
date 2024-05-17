import re
from argparse import ArgumentParser
from pathlib import Path


def parse_args():
    parser = ArgumentParser(description="Create a new usecase")
    parser.add_argument("classname")
    parser.add_argument("foldername")
    return parser.parse_args()


def make_dir(path: str) -> None:
    path_ = Path(path)
    path_.mkdir(parents=True, exist_ok=True)


def to_snake_case(text: str):
    name = re.sub(r"\s", "_", text)
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def to_pascal_case(text: str):
    name = re.sub(r"[\s_-]+", " ", text)
    return "".join(word.title() for word in name.split())


def make_domain_usecase(classname: str, foldername: str) -> None:
    python_class = f"{to_pascal_case(classname)}{to_pascal_case(foldername)}"
    path = f"src/domain/usecases/{to_snake_case(foldername)}"
    make_dir(path)
    with open(f"{path}/{to_snake_case(classname)}.py", "w") as f:
        f.write(
            f"""from abc import ABC, abstractmethod

from pydantic import BaseModel


class {python_class}Params(BaseModel):
    ...


class {python_class}Result(BaseModel):
    ...


class I{python_class}UseCase(ABC):
    @abstractmethod
    async def execute(self, params: {python_class}Params) -> {python_class}Result: ...

"""
        )


def make_data_usecase(classname: str, foldername: str) -> None:
    python_class = f"{to_pascal_case(classname)}{to_pascal_case(foldername)}"
    path = f"src/data/usecases/{to_snake_case(foldername)}"
    make_dir(path)
    with open(f"{path}/{to_snake_case(classname)}.py", "w") as f:
        f.write(
            f"""from src.domain.usecases.{to_snake_case(foldername)}.{to_snake_case(classname)} import {python_class}Params, {python_class}Result, I{python_class}UseCase


class {python_class}UseCase(I{python_class}UseCase):
    async def execute(self, params: {python_class}Params) -> {python_class}Result:
        ...

"""
        )


def make_presentation_controller(classname: str, foldername: str) -> None:
    python_class = f"{to_pascal_case(classname)}{to_pascal_case(foldername)}"
    path = f"src/presentation/controllers/{to_snake_case(foldername)}"
    make_dir(path)
    with open(f"{path}/{to_snake_case(classname)}.py", "w") as f:
        f.write(
            f"""from fastapi import Depends
from src.domain.usecases.{to_snake_case(foldername)}.{to_snake_case(classname)} import {python_class}Params, {python_class}Result, I{python_class}UseCase


class {python_class}Controller:
    def __init__(self, usecase: I{python_class}UseCase):
        self.usecase = usecase

    async def handle(self, params: {python_class}Params = Depends()) -> {python_class}Result:
        return await self.usecase.execute(params)
    
    async def handle_graphql(self, ...) -> {python_class}Result:
        return await self.usecase.execute({python_class}Params(...))
"""
        )


def make_main_factory_usecase(classname: str, foldername: str) -> None:
    python_class = f"{to_pascal_case(classname)}{to_pascal_case(foldername)}"
    path = f"src/main/factories/usecases/{to_snake_case(foldername)}"
    make_dir(path)
    with open(f"{path}/{to_snake_case(classname)}.py", "w") as f:
        f.write(
            f"""from src.data.usecases.{to_snake_case(foldername)}.{to_snake_case(classname)} import {python_class}UseCase


class {python_class}UsecaseFactory:
    
    @staticmethod
    def create() -> {python_class}UseCase:
        return {python_class}UseCase()
"""
        )


def make_main_factory_controller(classname: str, foldername: str) -> None:
    python_class = f"{to_pascal_case(classname)}{to_pascal_case(foldername)}"
    path = f"src/main/factories/controllers/{to_snake_case(foldername)}"
    make_dir(path)
    with open(f"{path}/{to_snake_case(classname)}.py", "w") as f:
        f.write(
            f"""from src.presentation.controllers.{to_snake_case(foldername)}.{to_snake_case(classname)} import {python_class}Controller
from src.main.factories.usecases.{to_snake_case(foldername)}.{to_snake_case(classname)} import {python_class}UsecaseFactory

class {python_class}ControllerFactory:
    
    @staticmethod
    def create() -> {python_class}Controller:
        return {python_class}Controller(
            {python_class}UsecaseFactory.create()
        )"""
        )


def create():
    args = parse_args()
    make_domain_usecase(args.classname, args.foldername)
    make_data_usecase(args.classname, args.foldername)
    make_presentation_controller(args.classname, args.foldername)
    make_main_factory_usecase(args.classname, args.foldername)
    make_main_factory_controller(args.classname, args.foldername)


if __name__ == "__main__":
    create()
