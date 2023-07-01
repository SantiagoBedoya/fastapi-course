from fastapi import APIRouter, Path, HTTPException, status, Request, Depends
from fastapi.templating import Jinja2Templates
from model import Todo, TodoItem, TodoItems

todo_router = APIRouter()

todo_list: list[Todo] = []
templates = Jinja2Templates(directory="templates/")


@todo_router.post("/todo", status_code=status.HTTP_201_CREATED)
async def add_todo(request: Request, todo: Todo = Depends(Todo.as_form)):
    todo.id = len(todo_list) + 1
    todo_list.append(todo)
    return templates.TemplateResponse("todo.html", {
        "request": request,
        "todos": todo_list,
    })


@todo_router.get("/todo", response_model=TodoItems)
async def get_todos(request: Request):
    return templates.TemplateResponse("todo.html", {
        "request": request,
        "todos": todo_list,
    })


@todo_router.get("/todo/{todo_id}")
async def get_todo(
    request: Request,
    todo_id: int = Path(..., title="The ID of the todo to retrieve")
):
    for todo in todo_list:
        if todo.id == todo_id:
            return templates.TemplateResponse("todo.html", {
                "request": request, 
                "todo": todo,
            })

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="todo with given id doesn't exist"
    )


@todo_router.put("/todo/{todo_id}")
async def update_todo(
    request: Request,
    todo_data: TodoItem,
    todo_id: int = Path(..., title="The ID of the todo to be updated"),
):
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
            return {"message": "todo updated successfully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="todo with given id doesn't exist"
    )


@todo_router.delete("/todo/{todo_id}")
async def delete_todo(
    todo_id: int = Path(..., title="The ID of the todo be deleted")
) -> dict:
    for index in range(len(todo_list)):
        todo = todo_list[index]
        if todo.id == todo_id:
            todo_list.pop(index)
            return {"message": "todo deleted successfully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="todo with given id doesn't exist"
    )
