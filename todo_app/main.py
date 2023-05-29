from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Path
from database import engine, SessionLocal
import models
from models import Todos
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str = Field( min_length=3, max_length=50)
    priority: int = Field( ge=1, le=5)
    complete: bool

@app.get('/')
def get_all_todos(db:db_dependency):
    return db.query(Todos).all()

@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def read_todo(db:db_dependency, todo_id: int=Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")

@app.post("/todos/create_todo", status_code=status.HTTP_201_CREATED)
def create_todo(db:db_dependency, todo: TodoRequest):
    new_todo = Todos(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(db:db_dependency, 
                todo: TodoRequest,
                todo_id: int=Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        todo_model.title = todo.title
        todo_model.description = todo.description
        todo_model.priority = todo.priority
        todo_model.complete = todo.complete
        db.commit()
        return
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_by_id(db:db_dependency, todo_id: int=Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        db.delete(todo_model)
        db.commit()
        return
    raise HTTPException(status_code=404, detail="Todo not found")