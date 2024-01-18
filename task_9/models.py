from mongoengine import Document, StringField, ListField, ReferenceField, CASCADE


class Author(Document):
    fullname = StringField(required=True)


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField(required=True)
