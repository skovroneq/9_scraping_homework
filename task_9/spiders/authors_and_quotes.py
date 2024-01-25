import scrapy
import json
import os


class AuthorsAndQuotesSpider(scrapy.Spider):
    name = "authors_and_quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def __init__(self, *args, **kwargs):
        super(AuthorsAndQuotesSpider, self).__init__(*args, **kwargs)
        self.authors = set()
        self.quotes = []
        self.author_details = {}

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            quote_data = {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small[@class='author']/text()").get(),
                "quote": quote.xpath("span[@class='text']/text()").get()
            }

            if quote_data['quote']:
                quote_data['quote'] = quote_data['quote'].replace(
                    '\u201c', '').replace('\u201d', '')

            self.quotes.append(quote_data)
            self.authors.add(quote_data['author'])

            author_link = quote.xpath(
                "span/a[contains(@href, \"author\")]/@href").get()
            author_page_link = f"https://quotes.toscrape.com/{author_link}"

            if author_page_link:
                yield scrapy.Request(url=response.urljoin(author_page_link), callback=self.parse_author_about)

            yield quote_data

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_author_about(self, response):
        author_name = response.xpath(
            "//h3[@class='author-title']/text()").get()
        born_date = response.xpath(
            "//span[@class='author-born-date']/text()").get()
        born_location = response.xpath(
            "//span[@class='author-born-location']/text()").get()
        description = response.xpath(
            "//div[@class='author-description']/text()").get().strip()

        self.author_details[author_name] = {
            "born_date": born_date,
            "born_location": born_location,
            "description": description
        }

    def closed(self, reason):
        authors_data = []

        for author_name in self.authors:
            basic_info = {'fullname': author_name}
            additional_info = self.author_details.get(author_name, {})
            author_data = {**basic_info, **additional_info}
            authors_data.append(author_data)

        authors_file_path = 'authors.json'
        quotes_file_path = 'quotes.json'

        if os.path.exists(authors_file_path):
            os.remove(authors_file_path)
        if os.path.exists(quotes_file_path):
            os.remove(quotes_file_path)

        with open('authors.json', 'w') as authors_file:
            json.dump(authors_data, authors_file, indent=2)

        with open('quotes.json', 'w') as quotes_file:
            json.dump(self.quotes, quotes_file, indent=2)
