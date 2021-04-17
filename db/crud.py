from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, email: str, user_id: int):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u:
        return None
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, email: str, skip: int = 0, limit: int = 100):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u:
        return None
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_goods(db: Session, skip: int = 0, limit: int = 100, q: str = ""):
    if q is not None:
        return db.query(models.Good).filter(models.Good.title.ilike(q)).offset(skip).limit(limit).all()
    else:
        return db.query(models.Good).offset(skip).limit(limit).all()


def create_user_good(db: Session, email: str, good: schemas.GoodCreate, user_id: int):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u or user_id != u.id:
        return None
    db_good = models.Good(**good.dict(), owner_id=user_id)
    db.add(db_good)
    db.commit()
    db.refresh(db_good)
    return db_good


def create_location(db: Session, email: str, location: schemas.LocationCreate, user_id: int):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u or user_id != u.id:
        return None
    db_location = models.Location(**location.dict(), user_id=user_id)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def get_locations(db: Session, email: str, skip: int = 0, limit: int = 100):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u:
        return None
    return db.query(models.Location).filter(models.Location.user_id == u.id).offset(skip).limit(limit).all()


def create_share(db: Session, email: str, share: schemas.ShareCreate, user_id: int):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u or user_id != u.id:
        return None
    db_share = models.Share(**share.dict(), user_id=user_id)
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share


def get_shares(db: Session, email: str, skip: int = 0, limit: int = 100):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u:
        return None
    return db.query(models.Share).filter(models.Share.user_id == u.id).offset(skip).limit(limit).all()


def create_image(db: Session, email: str, image: schemas.ImageCreate, user_id: int):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u or user_id != u.id:
        return None
    db_image = models.Image(**image.dict(), user_id=user_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def add_image_file(db: Session, email: str, image_id: int, content: bytes):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u:
        return None
    db_image = db.query(models.Image).filter(models.Image.user_id == u.id).filter(models.Image.id == image_id).first()
    db_image.content = content
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def get_image(db: Session, email: str, image_id: int):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u:
        return None
    return db.query(models.Image).filter(models.Image.id == image_id).first()


def update_user(db: Session, email: str, user: schemas.UserUpdate, user_id: int):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u or user_id != u.id:
        return None
    db_user = models.User(**user.dict(), id=user_id)
    db_user = db.merge(db_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_good(db: Session, email: str, good: schemas.GoodUpdate, good_id: int):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u:
        return None
    db_good = models.Good(**good.dict(), id=good_id)
    db_good = db.merge(db_good)
    db.add(db_good)
    db.commit()
    db.refresh(db_good)
    return db_good


def update_image(db: Session, email: str, image: schemas.ImageUpdate, image_id: int):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u:
        return None
    db_image = models.Image(**image.dict(), id=image_id)
    db_image = db.merge(db_image)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def update_share(db: Session, email: str, share: schemas.ShareUpdate, share_id: int):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u:
        return None
    db_share = models.Share(**share.dict(), id=share_id)
    db_share = db.merge(db_share)
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share


def update_location(db: Session, email: str, location: schemas.LocationUpdate, location_id: int):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u:
        return None
    db_location = models.Location(**location.dict(), id=location_id)
    db_location = db.merge(db_location)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def delete_image(db: Session, email: str, image_id: int):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u:
        return None
    res = db.query(models.Image).filter(models.Image.user_id == u.id).filter(models.Image.id == image_id).delete()
    db.commit()
    return res


def delete_location(db: Session, email: str, location_id: int):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u:
        return None
    res = db.query(models.Location).filter(models.Location.user_id == u.id).filter(models.Location.id == location_id).delete()
    db.commit()
    return res


def delete_share(db: Session, email: str, share_id: int):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u:
        return None
    res = db.query(models.Share).filter(models.Share.user_id == u.id).filter(models.Share.id == share_id).delete()
    db.commit()
    return res


def delete_good(db: Session, email: str, good_id: int):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u:
        return None
    res = db.query(models.Good).filter(models.Good.user_id == u.id).filter(models.Good.id == good_id).delete()
    db.commit()
    return res


def delete_user(db: Session, email: str, user_id: int):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u or u.id != user_id:
        return None
    res = db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return res


def get_images(db: Session, email: str, skip: int = 0, limit: int = 100):
    u = db.query(models.User).filter(models.User.email == email).first()
    if not u:
        return None
    return db.query(models.Image).filter(models.Image.user_id == u.id).offset(skip).limit(limit).all()
