from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, LargeBinary
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    public = Column(Boolean, default=True)

    goods = relationship("Good", back_populates="owner")
    locations = relationship("Location", back_populates="user")
    shares = relationship("Share", back_populates="user")
    images = relationship("Image", back_populates="user")
    

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    public = Column(Boolean, default=True)
    zip = Column(String)
    city = Column(String)
    address = Column(String)
    lat = Column(Float)
    lon = Column(Float)

    user = relationship("User", back_populates="locations")
    goods = relationship("Good", back_populates="location")
    shares = relationship("Share", back_populates="location")
    

class Good(Base):
    __tablename__ = "goods"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))

    owner = relationship("User", back_populates="goods")
    location = relationship("Location", back_populates="goods")
    images = relationship("Image", back_populates="good")
    

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    url = Column(String)
    content = Column(LargeBinary)
    mime_type = Column(String, default="image/jpeg")
    good_id = Column(Integer, ForeignKey("goods.id"))
    share_id = Column(Integer, ForeignKey("shares.id"))
    
    shares = relationship("Share", back_populates="images")
    good = relationship("Good", back_populates="images")
    user = relationship("User", back_populates="images")
    

class Share(Base):
    __tablename__ = "shares"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    good_id = Column(Integer, ForeignKey("goods.id"))
    start_date = Column(DateTime, index=True)
    planned_end_date = Column(DateTime)
    end_date = Column(DateTime)
    location_id = Column(Integer, ForeignKey("locations.id"))

    images = relationship("Image", back_populates="shares")
    user = relationship("User", back_populates="shares")
    location = relationship("Location", back_populates="shares")
