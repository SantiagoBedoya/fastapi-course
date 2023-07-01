from pydantic import BaseModel
from fastapi import Form
from typing import List, Optional

class TodoItem(BaseModel):
    item: str

    class Config:
        schema_extra = {
            "example": {
                "item": "add other todo"
            }
        }

class TodoItems(BaseModel):
    todos: list[TodoItem]


class Todo(BaseModel):
    id: Optional[int] = 0
    item: str

    @classmethod
    def as_form(cls, item: str = Form(...)):
        return cls(item=item)

   