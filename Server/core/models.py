from mongoengine import Document, StringField
import secrets
class User(Document):
    username = StringField(required=True, max_length=100, unique=True)
    phone = StringField(required=True, max_length=15)
    password = StringField(required=True, max_length=100)
    secret_key =StringField(default=lambda: secrets.token_hex(14))

    def __str__(self):
        return self.username
    
class Report(Document):
    secret_key = StringField(required=True)
    
