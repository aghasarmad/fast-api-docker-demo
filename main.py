from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

class Tea(BaseModel):
    id: Optional[UUID] = None
    name: str
    origin: Optional[str] = None

app = FastAPI()

teas: List[Tea] = []

# @app.get("/")
# def read_root():
#     return {"message": "Hello, World!"}

@app.get("/teas")
def get_teas():
    return teas

@app.post("/teas")
def create_tea(tea: Tea):
    tea.id = uuid4()  # Assign a new UUID to the tea
    teas.append(tea)
    return tea

@app.get("/teas/{tea_id}")
def get_tea(tea_id: UUID):
    for tea in teas:
        if tea.id == tea_id:
            return tea
    return {"error": "Tea not found"}, 404

@app.put("/teas/{tea_id}")
def update_tea(tea_id: UUID, tea: Tea):
    for index, existing_tea in enumerate(teas):
        if existing_tea.id == tea_id:
            #teas[index] = tea
            updated_tea = existing_tea.model_copy(update=tea.model_dump(exclude_unset=True))
            teas[index] = updated_tea
            return updated_tea
    return {"error": "Tea not found"}, 404

@app.delete("/teas/{tea_id}")
def delete_tea(tea_id: UUID):
    for index, tea in enumerate(teas):
        if tea.id == tea_id:
            deleted = teas.pop(index)
            return deleted
    return {"error": "Tea not found"}, 404

def main():
    uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    main()
