from pydantic import BaseModel
from typing import Dict, Any, List


class Booking(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: Dict[str, str]
    additionalneeds: str

class BookingIds(BaseModel):
    bookingid: int

class BookingIdsResponse(BaseModel):
    root: List[BookingIds]

    def validate_all_id(self) -> bool:
        return all(booking.bookingid > 0 for booking in self.root)

class TokenResponse(BaseModel):
    token: str