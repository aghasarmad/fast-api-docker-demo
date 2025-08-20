from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID
import os
import uvicorn
import models, schemas, database

# Initialize the API
app = FastAPI()


# ----------- CRUD Routes ----------- #

@app.post("/teas", response_model=schemas.TeaRead)
def create_tea(tea: schemas.TeaCreate, db: Session = Depends(database.get_db)):
    db_tea = models.TeaDB(name=tea.name, origin=tea.origin)
    db.add(db_tea)
    db.commit()
    db.refresh(db_tea)
    return db_tea


@app.get("/teas", response_model=list[schemas.TeaRead])
def get_teas(db: Session = Depends(database.get_db)):
    return db.query(models.TeaDB).all()


@app.get("/teas/{tea_id}", response_model=schemas.TeaRead)
def get_tea(tea_id: UUID, db: Session = Depends(database.get_db)):
    tea = db.query(models.TeaDB).filter(models.TeaDB.id == tea_id).first()
    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")
    return tea


@app.put("/teas/{tea_id}", response_model=schemas.TeaRead)
def update_tea(tea_id: UUID, tea_update: schemas.TeaCreate, db: Session = Depends(database.get_db)):
    tea = db.query(models.TeaDB).filter(models.TeaDB.id == tea_id).first()
    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")

    tea.name = tea_update.name
    tea.origin = tea_update.origin
    db.commit()
    db.refresh(tea)
    return tea


@app.delete("/teas/{tea_id}")
def delete_tea(tea_id: UUID, db: Session = Depends(database.get_db)):
    tea = db.query(models.TeaDB).filter(models.TeaDB.id == tea_id).first()
    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")
    db.delete(tea)
    db.commit()
    return {"message": "Tea deleted"}


def main():
    port = int(os.environ.get("PORT", 8080)) 
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
