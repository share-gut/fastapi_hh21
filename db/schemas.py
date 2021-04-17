from typing import List, Optional

from datetime import datetime

from pydantic import BaseModel


class LocationBase(BaseModel):
    name: str
    zip: str
    city: str
    address: str
    lat: float
    lon: float
    
    
class LocationCreate(LocationBase):
    pass


class LocationUpdate(LocationBase):
    public: bool
    
    class Config:
        orm_mode = True


class Location(LocationBase):
    id: int
    user_id: int
    public: bool
    
    class Config:
        orm_mode = True


class ImageBase(BaseModel):
    name: str
    url: Optional[str]
    mime_type: Optional[str]
    good_id: Optional[int]
    share_id: Optional[int]
    

class ImageCreate(ImageBase):
    pass


class ImageUpdate(ImageBase):
    pass


class Image(ImageBase):
    id: int
    user_id: int
    content: Optional[bytes]
    
    class Config:
        orm_mode = True


class ImageNoContent(ImageBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True
        
        
class GoodBase(BaseModel):
    title: str
    description: Optional[str] = None


class GoodCreate(GoodBase):
    location_id: Optional[int]


class GoodUpdate(GoodBase):
    location_id: Optional[int]


class Good(GoodBase):
    id: int
    owner_id: int
    location: Optional[Location] = None
    images: List[ImageNoContent] = []

    class Config:
        orm_mode = True


class ShareBase(BaseModel):
    good_id: int
    start_date: datetime
    
    
class ShareCreate(ShareBase):
    location_id: Optional[int]


class ShareUpdate(ShareBase):
    planned_end_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location_id: Optional[int]
    

class Share(ShareBase):
    id: int
    user_id: int
    planned_end_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    images: List[ImageNoContent] = []
    location: Optional[Location] = None
    
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    email: str


class UserUpdate(UserBase):
    is_active: bool
    public: bool

    class Config:
        orm_mode = True
        

class User(UserBase):
    id: int
    is_active: bool
    public: bool
    goods: List[Good] = []
    locations: List[Location] = []
    shares: List[Share] = []
    images: List[ImageNoContent] = []

    class Config:
        orm_mode = True
