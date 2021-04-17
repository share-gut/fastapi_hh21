import base64
from typing import List

from fastapi import FastAPI, Depends, HTTPException, File
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine


app = FastAPI(title='Sharegood API', description='PoC backend for sharegood. Create, read, update and delete users, goods, shares, locations and images. Also supports image uploads. WARNING: there is no auth whatsoever.')

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(db, user, user_id)


@app.delete("/users/{user_id}", response_model=int)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id=user_id)


@app.get("/goods/", response_model=List[schemas.Good])
def read_goods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    goods = crud.get_goods(db, skip=skip, limit=limit)
    return goods


@app.post("/users/{user_id}/goods/", response_model=schemas.Good)
def create_good_for_user(user_id: int, good: schemas.GoodCreate, db: Session = Depends(get_db)):
    return crud.create_user_good(db=db, good=good, user_id=user_id)


@app.put("/goods/{good_id}", response_model=schemas.Good)
def update_good(good_id: int, good: schemas.GoodUpdate, db: Session = Depends(get_db)):
    return crud.update_good(db, good, good_id)


@app.delete("/goods/{good_id}", response_model=int)
def delete_good(good_id: int, db: Session = Depends(get_db)):
    return crud.delete_good(db, good_id=good_id)


@app.get("/locations/", response_model=List[schemas.Location])
def read_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    locations = crud.get_locations(db, skip=skip, limit=limit)
    return locations


@app.post("/users/{user_id}/locations/", response_model=schemas.Location)
def create_location_for_user(user_id: int, location: schemas.LocationCreate, db: Session = Depends(get_db)):
    return crud.create_location(db=db, location=location, user_id=user_id)


@app.put("/locations/{location_id}", response_model=schemas.Location)
def update_location(location_id: int, location: schemas.LocationUpdate, db: Session = Depends(get_db)):
    return crud.update_location(db, location, location_id)


@app.delete("/location/{location_id}", response_model=int)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    return crud.delete_location(db, location_id=location_id)


@app.get("/shares/", response_model=List[schemas.Share])
def read_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    shares = crud.get_shares(db, skip=skip, limit=limit)
    return shares


@app.post("/users/{user_id}/shares/", response_model=schemas.Share)
def create_share_for_user(user_id: int, share: schemas.ShareCreate, db: Session = Depends(get_db)):
    return crud.create_share(db=db, share=share, user_id=user_id)


@app.put("/shares/{share_id}", response_model=schemas.Share)
def update_share(share_id: int, share: schemas.ShareUpdate, db: Session = Depends(get_db)):
    return crud.update_share(db, share=share, share_id=share_id)


@app.delete("/share/{share_id}", response_model=int)
def delete_share(share_id: int, db: Session = Depends(get_db)):
    return crud.delete_share(db, share_id=share_id)


@app.get("/images/", response_model=List[schemas.ImageNoContent])
def read_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_images(db, skip=skip, limit=limit)


@app.post("/users/{user_id}/images/", response_model=schemas.Image)
def create_image_for_user(user_id: int, image: schemas.ImageCreate, db: Session = Depends(get_db)):
    return crud.create_image(db=db, image=image, user_id=user_id)


@app.post("/upload/images/{image_id}", response_model=schemas.ImageNoContent)
def upload_image_content(image_id: int, file: bytes = File(...), db: Session = Depends(get_db)):
    return crud.add_image_file(db, image_id=image_id, content=base64.b64encode(file))


@app.get("/images/{image_id}", response_class=Response, response_description="Binary image data, content-type as stored in the image model")
def read_image_content(image_id: int, db: Session = Depends(get_db)):
    db_image = crud.get_image(db, image_id=image_id)
    content = base64.b64decode(db_image.content)
    return Response(content=content, media_type=db_image.mime_type)


@app.put("/images/{image_id}", response_model=schemas.ImageNoContent)
def update_image(image_id: int, image: schemas.ImageUpdate, db: Session = Depends(get_db)):
    return crud.update_image(db, image=image, image_id=image_id)


@app.delete("/images/{image_id}", response_model=int)
def delete_image(image_id: int, db: Session = Depends(get_db)):
    return crud.delete_image(db, image_id=image_id)
