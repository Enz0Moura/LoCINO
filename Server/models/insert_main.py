import uuid
from datetime import datetime

from typing_extensions import Optional

from conf.db_session import create_session
from models.address import Address
from models.alert import Alert
from models.bracelet import Bracelet
from models.contact import Contact
from models.location_history import LocationHistory
from models.select_main import select_user_by_id, select_address_by_user, select_bracelet_by_user, \
    select_bracelet_by_id, select_location_history_by_id
from models.user import User


def insert_user(name: str) -> User:
    user = User(name=name)

    with create_session() as session:
        session.add(user)
        session.commit()

    return user


def insert_contact(user_id: uuid.uuid4, name: str, telephone: str, email: str) -> Optional[Contact]:
    if not select_user_by_id(user_id):
        print("No user found")
        return None

    contact = Contact(name=name, user_id=user_id, telephone=telephone, email=email)
    with create_session() as session:
        session.add(contact)
        session.commit()
    return contact


def insert_address(user_id: uuid.uuid4, street: str, neighborhood: str, city: str, state: str) -> Optional[Address]:
    if not select_user_by_id(user_id):
        print("No user found")
        return None
    if select_address_by_user(user_id):
        print("Address already exists")
        return None

    address = Address(user_id=user_id, street=street, neighborhood=neighborhood, city=city, state=state)

    with create_session() as session:
        session.add(address)
        session.commit()

    return address


def insert_bracelet(user_id: uuid.uuid4) -> Optional[Bracelet]:
    if not select_user_by_id(user_id):
        print("No user found.")
        return None
    if select_bracelet_by_user(user_id):
        print("User already linked into a bracelet.")
        return None

    bracelet = Bracelet(user_id=user_id)

    with create_session() as session:
        session.add(bracelet)
        session.commit()

    return bracelet


def insert_location_history(bracelet_id: uuid.uuid4, location_time: datetime, register_time: datetime, battery: int, latitude: float,
                            longitude: float) -> Optional[LocationHistory]:
    if not select_bracelet_by_id(bracelet_id):
        print("No bracelet found.")
        return None

    location_history = LocationHistory(bracelet_id=bracelet_id, location_time=location_time, register_time=register_time, battery=battery,
                                       latitude=latitude, longitude=longitude)

    with create_session() as session:
        session.add(location_history)
        session.commit()

    return location_history


def insert_alert(location_history_id: uuid.uuid4, alert_type: int) -> Optional[Alert]:
    if not select_location_history_by_id(location_history_id):
        print("No location history found.")
        return None

    alert = Alert(location_history_id=location_history_id, alert_type=alert_type)

    with create_session() as session:
        session.add(alert)
        session.commit()

    return alert
