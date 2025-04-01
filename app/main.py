from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

# Create the FastAPI app
app = FastAPI()

# Initialize the database
models.Base.metadata.create_all(bind=database.engine)

@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    return crud.create_task(db=db, task=task)

@app.get("/tasks/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(database.get_db)):
    db_task = crud.get_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.get("/tasks/", response_model=list[schemas.Task])
def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    tasks = crud.get_tasks(db=db, skip=skip, limit=limit)
    return tasks

@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    db_task = crud.update_task(db=db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    db_task = crud.delete_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
