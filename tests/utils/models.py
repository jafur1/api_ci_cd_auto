from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class Booking(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: Dict[str, str]
    additionalneeds: str

class BookingResponse(BaseModel):
    bookingid: int
    booking: Booking

class BookingIds(BaseModel):
    bookingid: int

class TokenResponse(BaseModel):
    token: str