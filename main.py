import base64
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, File
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine


app = FastAPI(title='Sharegut API', description='PoC backend for sharegut. Create, read, update and delete users, goods, shares, locations and images. Also supports image uploads. WARNING: there is no auth whatsoever.')

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
    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Name already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(email: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, email, skip=skip, limit=limit)
    if not users:
        raise HTTPException(status_code=401, detail="Not authorized")
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, email, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, email: str, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    res = crud.update_user(db, email, user, user_id)
    if not res:
        raise HTTPException(status_code=401, detail="Not authorized")
    return res


@app.delete("/users/{user_id}", response_model=int)
def delete_user(user_id: int, email: str, db: Session = Depends(get_db)):
    res = crud.delete_user(db, email, user_id=user_id)
    if not res:
        raise HTTPException(status_code=401, detail="Not authorized")
    return res


@app.get("/goods/", response_model=List[schemas.Good])
def read_goods(skip: int = 0, limit: int = 100, q: Optional[str] = None, db: Session = Depends(get_db)):
    res = crud.get_goods(db, skip=skip, limit=limit, q=q)
    if not res:
        raise HTTPException(status_code=401, detail="Not authorized")
    return res


@app.post("/users/{user_id}/goods/", response_model=schemas.Good)
def create_good_for_user(user_id: int, email: str, good: schemas.GoodCreate, db: Session = Depends(get_db)):
    res = crud.create_user_good(db, email, good=good, user_id=user_id)
    if not res:
        raise HTTPException(status_code=401, detail="Not authorized")
    return res


@app.put("/goods/{good_id}", response_model=schemas.Good)
def update_good(good_id: int, email: str, good: schemas.GoodUpdate, db: Session = Depends(get_db)):
    res = crud.update_good(db, email, good=good, good_id=good_id)
    if not res:
        raise HTTPException(status_code=401, detail="Not authorized")
    return res


@app.delete("/goods/{good_id}", response_model=int)
def delete_good(good_id: int, email: str, db: Session = Depends(get_db)):
    res = crud.delete_good(db, email, good_id=good_id)
    if not res:
        raise HTTPException(status_code=401, detail="Not authorized")
    return res


@app.get("/locations/", response_model=List[schemas.Location])
def read_locations(email: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    res = crud.get_locations(db, email, skip=skip, limit=limit)
    if not res:
        raise HTTPException(status_code=401, detail="Not authorized")
    return res


@app.post("/users/{user_id}/locations/", response_model=schemas.Location)
def create_location_for_user(user_id: int, email: str, location: schemas.LocationCreate, db: Session = Depends(get_db)):
    res = crud.create_location(db, email, location=location, user_id=user_id)
    if not res:
        raise HTTPException(status_code=401, detail="Not authorized")
    return res


@app.put("/locations/{location_id}", response_model=schemas.Location)
def update_location(location_id: int, email: str, location: schemas.LocationUpdate, db: Session = Depends(get_db)):
    res = crud.update_location(db, email, location=location, location_id=location_id)
    if not res:
        raise HTTPException(status_code=401, detail="Not authorized")
    return res


@app.delete("/location/{location_id}", response_model=int)
def delete_location(location_id: int, email: str, db: Session = Depends(get_db)):
    res = crud.delete_location(db, email, location_id=location_id)
    if not res:
        raise HTTPException(status_code=401, detail="Not authorized")
    return res


@app.get("/shares/", response_model=List[schemas.Share])
def read_locations(email: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    res = crud.get_shares(db, email, skip=skip, limit=limit)
    if not res:
        raise HTTPException(status_code=401, detail="Not authorized")
    return res


@app.post("/users/{user_id}/shares/", response_model=schemas.Share)
def create_share_for_user(user_id: int, email: str, share: schemas.ShareCreate, db: Session = Depends(get_db)):
    res = crud.create_share(db, email, share=share, user_id=user_id)
    if not res:
        raise HTTPException(status_code=401, detail="Not authorized")
    return res


@app.put("/shares/{share_id}", response_model=schemas.Share)
def update_share(share_id: int, email: str, share: schemas.ShareUpdate, db: Session = Depends(get_db)):
    res = crud.update_share(db, email, share=share, share_id=share_id)
    if not res:
        raise HTTPException(status_code=401, detail="Not authorized")
    return res


@app.delete("/share/{share_id}", response_model=int)
def delete_share(share_id: int, email: str, db: Session = Depends(get_db)):
    res = crud.delete_share(db, email, share_id=share_id)
    if not res:
        raise HTTPException(status_code=401, detail="Not authorized")
    return res


@app.get("/images/", response_model=List[schemas.ImageNoContent])
def read_images(email: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    res = crud.get_images(db, email, skip=skip, limit=limit)
    if not res:
        raise HTTPException(status_code=401, detail="Not authorized")
    return res


@app.post("/users/{user_id}/images/", response_model=schemas.Image)
def create_image_for_user(user_id: int, email: str, image: schemas.ImageCreate, db: Session = Depends(get_db)):
    res = crud.create_image(db, email, image=image, user_id=user_id)
    if not res:
        raise HTTPException(status_code=401, detail="Not authorized")
    return res


@app.post("/upload/images/{image_id}", response_model=schemas.ImageNoContent)
def upload_image_content(image_id: int, email: str, file: bytes = File(...), db: Session = Depends(get_db)):
    res = crud.add_image_file(db, email, image_id=image_id, content=base64.b64encode(file))
    if not res:
        raise HTTPException(status_code=401, detail="Not authorized")
    return res


@app.get("/images/{image_id}", response_class=Response, response_description="Binary image data, content-type as stored in the image model")
def read_image_content(image_id: int, email: str, db: Session = Depends(get_db)):
    db_image = crud.get_image(db, email, image_id=image_id)
    if not db_image:
        raise HTTPException(status_code=401, detail="Not authorized")
    content = base64.b64decode(db_image.content)
    return Response(content=content, media_type=db_image.mime_type)


@app.put("/images/{image_id}", response_model=schemas.ImageNoContent)
def update_image(image_id: int, email: str, image: schemas.ImageUpdate, db: Session = Depends(get_db)):
    res = crud.update_image(db, email, image=image, image_id=image_id)
    if not res:
        raise HTTPException(status_code=401, detail="Not authorized")
    return res


@app.delete("/images/{image_id}", response_model=int)
def delete_image(image_id: int, email: str, db: Session = Depends(get_db)):
    res = crud.delete_image(db, email, image_id=image_id)
    if not res:
        raise HTTPException(status_code=401, detail="Not authorized")
    return res
