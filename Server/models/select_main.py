import uuid
from typing import List, Optional

from conf.db_session import create_session
from models.address import Address
from models.alert import Alert
from models.bracelet import Bracelet
from models.contact import Contact
from models.location_history import LocationHistory
from models.user import User


# SELECT * FROM users
def select_all_users() -> None:
    with create_session() as session:
        users: List[User] = session.query(User).all()

        for user in users:
            print(f"ID: {user.id}")
            print(f"Name: {user.name}")
    return None


def select_user_by_id(user_id: uuid.uuid4) -> Optional[User]:
    with create_session() as session:
        user: Optional[User] = session.query(User).filter_by(id=user_id).first()
    return user if user else None


def select_bracelet_by_id(bracelet_id: uuid.uuid4) -> Optional[Bracelet]:
    with create_session() as session:
        bracelet: Optional[Bracelet] = session.query(Bracelet).filter_by(id=bracelet_id).first()
    return bracelet if bracelet else None


def select_location_history_by_id(location_history_id: uuid.uuid4) -> Optional[LocationHistory]:
    with create_session() as session:
        location_history: Optional[LocationHistory] = session.query(LocationHistory).filter_by(
            id=location_history_id).first()
    return location_history if location_history else None


def select_address_by_user(user_id: uuid.uuid4) -> Optional[Address]:
    with create_session() as session:
        address: Optional[Address] = session.query(Address).filter_by(user_id=user_id).first()
    return address if address else None


def select_bracelet_by_user(user_id: uuid.uuid4) -> Optional[Bracelet]:
    with create_session() as session:
        bracelet: Optional[Bracelet] = session.query(Bracelet).filter_by(user_id=user_id).first()
    return bracelet if bracelet else None

def fetch_user_data(user_id: uuid.uuid4) -> None:
    with create_session() as session:
        user = session.query(User).filter_by(id=user_id).first()
        print(15 * "*" + f" User " + "*" * 15)
        print(f"User name: {user.name}")

        address = session.query(Address).filter_by(user_id=user_id).first()

        print(15 *"*" + f" Address " + "*" * 15)
        print(f"Street: {address.street}")
        print(f"Neighborhood: {address.neighborhood}")
        print(f"City: {address.city}")
        print(f"State: {address.state}")

        contact = session.query(Contact).filter_by(user_id=user_id).first()

        print(15 *"*" + f" Contact " + "*" * 15)

        print(f"Name: {contact.name}")
        print(f"Telephone: {contact.telephone}")
        print(f"Email: {contact.email}")

        bracelet = session.query(Bracelet).filter_by(user_id=user_id).first()
        print(15 *"-" + f" Bracelet Found " + "-" * 15)

        location_histories = session.query(LocationHistory).filter_by(bracelet_id=bracelet.id).all()

        if len(location_histories) > 0:
            print(15 * "-" + f" Location Histories found " + "-" * 15)
            for location_history in location_histories:
                print(f"Location Time: {location_history.location_time}")
                print(f"Battery: {location_history.battery}")
                print(f"Latitude: {location_history.latitude}")
                print(f"Longitude: {location_history.longitude}")
                alert = session.query(Alert).filter_by(location_history_id=location_history.id).first()
                if alert:
                    print("!" *15 + " Alert Found " + "!" * 15)
                    print(f"Alert Type: {alert.alert_type}")