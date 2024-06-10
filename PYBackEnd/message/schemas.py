from pydantic import BaseModel


class Message(BaseModel):
    message_type: bool
    id: int
    latitude: float
    longitude: float
    group_flag: int
    record_time: int
    max_records: int
    hop_count: int
    channel: int
    location_time: int
    help_flag: int
    battery: int
