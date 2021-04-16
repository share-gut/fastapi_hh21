from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_goods(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Good).offset(skip).limit(limit).all()


def create_user_good(db: Session, good: schemas.GoodCreate, user_id: int):
    db_good = models.Good(**good.dict(), owner_id=user_id)
    db.add(db_good)
    db.commit()
    db.refresh(db_good)
    return db_good


def create_location(db: Session, location: schemas.LocationCreate, user_id: int):
    db_location = models.Location(**location.dict(), user_id=user_id)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def get_locations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Location).offset(skip).limit(limit).all()


def create_share(db: Session, share: schemas.ShareCreate, user_id: int):
    db_share = models.Location(**share.dict(), user_id=user_id)
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share


def get_shares(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Share).offset(skip).limit(limit).all()


def create_image(db: Session, image: schemas.ImageCreate, user_id: int):
    db_image = models.Image(**image.dict(), user_id=user_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def add_image_file(db: Session, image_id: int, content: bytes):
    db_image = db.query(models.Image).filter(models.Image.id == image_id).first()
    db_image.content = content
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image
