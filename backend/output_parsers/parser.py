from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field


class Answer(BaseModel):
    answer: str = Field(description="Answer to a question about book")
    error: bool = Field(description="Is meant to be set to True if you know the answer and False if you don't know the answer")


parser = PydanticOutputParser(pydantic_object=Answer)