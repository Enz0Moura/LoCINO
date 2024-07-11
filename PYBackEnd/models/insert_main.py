import json
from datetime import datetime

from conf.db_session import create_session
from models.message import Message


def insert_message_result(success: bool, message: dict, use_my_sql: bool = False):
    print(f"Adding {str(success)} message to database")
    record_time = datetime.fromtimestamp(message.pop('record_time'))
    if message is not None:
        message = Message(success=success, message=json.dumps(message), battery=message['battery'],
                          channel=message['channel'], group_flag=message['group_flag'], hop_count=message['hop_count'],
                          help_flag=message['help_flag'], latitude=message['latitude'], longitude=message['longitude'],
                          location_time=datetime.now(), max_records=message['max_records'],
                          message_type=message['message_type'], record_time=record_time)
    else:
        message = Message(success=success, message=str(message), location_time=datetime.now())

    with create_session(use_my_sql) as session:
        session.add(message)
        session.commit()
    print(f"{str(success)} message added to database")
