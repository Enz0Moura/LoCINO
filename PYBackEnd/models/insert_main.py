from conf.db_session import create_session
from models.message import Message

def insert_message_result(success: bool, message: str):
    print(f"Adding {str(success)} message to database")
    message = Message(success=success, message=message)

    with create_session() as session:
        session.add(message)
        session.commit()
    print(f"{str(success)} message added to database")
