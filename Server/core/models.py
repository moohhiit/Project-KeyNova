from mongoengine import Document, StringField

class User(Document):
    username = StringField(required=True, max_length=100, unique=True)
    phone = StringField(required=True, max_length=15)
    password = StringField(required=True, max_length=100)

    def __str__(self):
        return self.username
