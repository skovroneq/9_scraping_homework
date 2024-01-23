import json
from models import Author, Quote
from mongoengine import connect
from dotenv import load_dotenv
import os


load_dotenv()

mongo_user = os.getenv('DB_USER')
mongodb_pass = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
domain = os.getenv('DB_DOMAIN')


def connect_to_mongodb():
    connect(
        host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)


def upload_authors_to_db():
    with open('authors.json', 'r') as file:
        authors_data = json.load(file)

    connect_to_mongodb()

    for author_data in authors_data:
        author_name = author_data['fullname']
        author = Author.objects(fullname=author_name).first()

        if not author:
            author = Author(fullname=author_name)
            author.save()


def upload_quotes_to_db():
    # with open('quotes.json', 'r') as file:
    #     quotes_data = json.load(file)

    # connect_to_mongodb()

    # for quote_data in quotes_data:
    #     author_name = quote_data['author']
    #     author = Author.objects(fullname=author_name).first()

    #     if not author:
    #         author = Author(fullname=author_name)
    #         author.save()

    #     quote_data['author'] = author
    #     quote = Quote(**quote_data)
    #     quote.save()

    with open('quotes.json', 'r') as file:
        quotes_data = json.load(file)

    connect_to_mongodb()

    for quote_data in quotes_data:
        quote_content = quote_data.get('quote')

        existing_quote = Quote.objects(quote=quote_content).first()

        if not existing_quote:
            quote = Quote(**quote_data)
            quote.save()
