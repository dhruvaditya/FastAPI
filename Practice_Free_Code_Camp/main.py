from fastapi import FastAPI, HTTPException

app = FastAPI()

# Sample data
tasks = [
    {"id": 1, "title": "Task 1"},
    {"id": 2, "title": "Task 2"},
]

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}

@app.get("/tasks")
def read_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def read_task(task_id: int):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        return task
    else:
        raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks")
def create_task(title: str):
    new_task = {"id": len(tasks) + 1, "title": title}
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: str):
    task_index = next((index for index, t in enumerate(tasks) if t["id"] == task_id), None)
    if task_index is not None:
        tasks[task_index]["title"] = title
        return tasks[task_index]
    else:
        raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return {"message": "Task deleted"}
