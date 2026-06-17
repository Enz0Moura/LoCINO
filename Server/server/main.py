from datetime import datetime

from models.insert_main import insert_user, insert_alert, insert_bracelet, insert_address, insert_contact, insert_location_history
from models.select_main import fetch_user_data

if __name__ == '__main__':
    user = insert_user(name="Enzo")
    user_id = user.id

    address = insert_address(user_id=user_id, street="16 de março", neighborhood="Centro", city="Petrópolis", state="Rio de janeiro")

    contact = insert_contact(user_id=user_id, name="Milena", telephone="888888888", email="test@gmail.com")

    bracelet = insert_bracelet(user_id=user_id)
    bracelet_id = bracelet.id

    location_history = insert_location_history(bracelet_id=bracelet_id, location_time=datetime.now(), register_time=datetime.now(), battery=5, latitude=10000, longitude=1000)
    location_history_id = location_history.id

    alert = insert_alert(location_history_id=location_history_id, alert_type=1)

    fetch_user_data(user_id=user_id)