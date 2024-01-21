import scrapy
import json


class AuthorsAndQuotesSpider(scrapy.Spider):
    name = "authors_and_quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def __init__(self, *args, **kwargs):
        super(AuthorsAndQuotesSpider, self).__init__(*args, **kwargs)
        self.authors = set()
        self.quotes = []

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            quote_data = {
                "keywords": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").extract_first(),
                "quote": quote.xpath("span[@class='text']/text()").get()
            }

            if quote_data['quote']:
                quote_data['quote'] = quote_data['quote'].replace(
                    '\u201c', '').replace('\u201d', '')

            self.quotes.append(quote_data)
            self.authors.add(quote_data['author'])

            yield quote_data

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def closed(self, reason):
        authors_data = [{'fullname': author} for author in self.authors]
        with open('authors.json', 'a') as authors_file:
            json.dump(authors_data, authors_file, indent=2)

        with open('quotes.json', 'a') as quotes_file:
            json.dump(self.quotes, quotes_file, indent=2)
