from peewee import *

proxy = Proxy()

class BaseModel(Model):
    class Meta:
        database = proxy

class User(BaseModel):
    username        = TextField()
    chat_id         = TextField()
    client_id       = TextField()
    handler         = TextField()
    auth_token      = TextField()
    plex_username   = TextField()


def add_user(username, chat_id, client_id, handler, auth_token):
  with proxy.atomic() as txn:
    User.create(
        username = username,
        chat_id = chat_id,
        client_id = client_id,
        handler = handler,
        auth_token = auth_token
    ).save()

def get_user_by_username(username):
  with proxy.atomic() as txn:
    return User.get_or_none(User.username == username)

def get_user_by_chat_id(chat_id):
  with proxy.atomic() as txn:
    return User.get_or_none(User.chat_id == chat_id)

def get_user_by_handler(handler):
  with proxy.atomic() as txn:
    return User.get_or_none(User.handler == handler)