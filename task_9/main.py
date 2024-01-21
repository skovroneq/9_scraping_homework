from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.authors_and_quotes import AuthorsAndQuotesSpider
from upload_data_to_db import upload_authors_to_db, upload_quotes_to_db


def main():

    process = CrawlerProcess(get_project_settings())
    process.crawl(AuthorsAndQuotesSpider)
    process.start()

    upload_authors_to_db()
    upload_quotes_to_db()


if __name__ == '__main__':
    main()
