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
    db_share = models.Share(**share.dict(), user_id=user_id)
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


def get_image(db: Session, image_id: int):
    return db.query(models.Image).filter(models.Image.id == image_id).first()


def update_user(db: Session, user: schemas.UserUpdate, user_id: int):
    db_user = models.User(**user.dict(), id=user_id)
    db_user = db.merge(db_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_good(db: Session, good: schemas.GoodUpdate, good_id: int):
    db_good = models.Good(**good.dict(), id=good_id)
    db_good = db.merge(db_good)
    db.add(db_good)
    db.commit()
    db.refresh(db_good)
    return db_good


def update_image(db: Session, image: schemas.ImageUpdate, image_id: int):
    db_image = models.Image(**image.dict(), id=image_id)
    db_image = db.merge(db_image)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def update_share(db: Session, share: schemas.ShareUpdate, share_id: int):
    db_share = models.Share(**share.dict(), id=share_id)
    db_share = db.merge(db_share)
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share


def update_location(db: Session, location: schemas.LocationUpdate, location_id: int):
    db_location = models.Location(**location.dict(), id=location_id)
    db_location = db.merge(db_location)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def delete_image(db: Session, image_id: int):
    res = db.query(models.Image).filter(models.Image.id == image_id).delete()
    db.commit()
    return res


def delete_location(db: Session, location_id: int):
    res = db.query(models.Location).filter(models.Location.id == location_id).delete()
    db.commit()
    return res


def delete_share(db: Session, share_id: int):
    res = db.query(models.Share).filter(models.Share.id == share_id).delete()
    db.commit()
    return res


def delete_good(db: Session, good_id: int):
    res = db.query(models.Good).filter(models.Good.id == good_id).delete()
    db.commit()
    return res


def delete_user(db: Session, user_id: int):
    res = db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return res


def get_images(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Image).offset(skip).limit(limit).all()

