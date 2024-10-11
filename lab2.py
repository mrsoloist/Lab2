from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()

# Initial project database
project_db = [
    {"project_id": 1, "project_title": "Website Development", "project_desc": "Create a website for client", "is_finished": False}
]

# Helper function to find a project by ID
def find_project(project_id: int):
    return next((project for project in project_db if project["project_id"] == project_id), None)

# Get a project by ID
@app.get("/projects/{project_id}")
def get_project(project_id: int):
    project = find_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"id {project_id} not found")
    return project

# Create a new project
@app.post("/projects")
def create_project(project_title: str, project_desc: Optional[str] = "", is_finished: bool = False):
    new_project_id = len(project_db) + 1
    new_project = {
        "project_id": new_project_id,
        "project_title": project_title,
        "project_desc": project_desc,
        "is_finished": is_finished
    }
    project_db.append(new_project)
    return {"message": "created", "project": new_project}

# Update a project
@app.patch("/projects/{project_id}")
def update_project(project_id: int, project_title: Optional[str] = None, project_desc: Optional[str] = None, is_finished: Optional[bool] = None):
    project = find_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"id {project_id} not found")

    if project_title:
        project["project_title"] = project_title
    if project_desc:
        project["project_desc"] = project_desc
    if is_finished is not None:
        project["is_finished"] = is_finished

    return {"message": "updated", "project": project}

# Delete a project
@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    project = find_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"id {project_id} not found")

    project_db.remove(project)
    return {"message": "deleted"}

# Replace a project entirely
@app.put("/projects/{project_id}")
def replace_project(project_id: int, project_title: str, project_desc: Optional[str] = "", is_finished: bool = False):
    project = find_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"id {project_id} not found")

    project.update({
        "project_title": project_title,
        "project_desc": project_desc,
        "is_finished": is_finished
    })

    return {"message": "replaced", "project": project}
