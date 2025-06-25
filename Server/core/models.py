from mongoengine import Document, StringField, DateTimeField
import secrets
import datetime
class User(Document):
    username = StringField(required=True, max_length=100, unique=True)
    phone = StringField(required=True, max_length=15)
    password = StringField(required=True, max_length=100)
    secret_key =StringField(default=lambda: secrets.token_hex(14))

    def __str__(self):
        return self.username
    
class ContentReport(Document):
    uni_id = StringField(required=True)
    text = StringField(required=True)
    category = StringField(required=True)
    reason = StringField(required=True)
    timestamp = DateTimeField(default=datetime.datetime.utcnow)


