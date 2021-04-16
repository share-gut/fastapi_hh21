import base64
from typing import List

from fastapi import FastAPI, Depends, HTTPException, File
from fastapi.responses import Response
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/goods/", response_model=schemas.Good)
def create_good_for_user(user_id: int, good: schemas.GoodCreate, db: Session = Depends(get_db)):
    return crud.create_user_good(db=db, good=good, user_id=user_id)


@app.get("/goods/", response_model=List[schemas.Good])
def read_goods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    goods = crud.get_goods(db, skip=skip, limit=limit)
    return goods


@app.post("/users/{user_id}/locations/", response_model=schemas.Location)
def create_location_for_user(user_id: int, location: schemas.LocationCreate, db: Session = Depends(get_db)):
    return crud.create_location(db=db, location=location, user_id=user_id)


@app.get("/locations/", response_model=List[schemas.Location])
def read_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    locations = crud.get_locations(db, skip=skip, limit=limit)
    return locations


@app.post("/users/{user_id}/shares/", response_model=schemas.Share)
def create_share_for_user(user_id: int, share: schemas.ShareCreate, db: Session = Depends(get_db)):
    return crud.create_share(db=db, share=share, user_id=user_id)


@app.get("/shares/", response_model=List[schemas.Share])
def read_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    shares = crud.get_shares(db, skip=skip, limit=limit)
    return shares


@app.post("/users/{user_id}/images/", response_model=schemas.Image)
def create_image_for_user(user_id: int, image: schemas.ImageCreate, db: Session = Depends(get_db)):
    return crud.create_image(db=db, image=image, user_id=user_id)


@app.post("/files/{image_id}")
async def create_file(image_id: int, file: bytes = File(...), db: Session = Depends(get_db)):
    crud.add_image_file(db, image_id=image_id, content=base64.b64encode(file))
    return {"file_size": len(file)}


@app.get("/image/{image_id}", response_class=Response, response_description="Binary image data, content-type as stored in the image model")
def read_image(image_id: int, db: Session = Depends(get_db)):
    db_image = crud.get_image(db, image_id=image_id)
    content = base64.b64decode(db_image.content)
    return Response(content=content, media_type=db_image.mime_type)
