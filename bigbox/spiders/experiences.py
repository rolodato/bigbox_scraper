import scrapy


class ExperiencesSpider(scrapy.Spider):
    name = "experiences"
    allowed_domains = ["bigbox.com.ar"]
    start_urls = ["https://bigbox.com.ar"]

    def parse(self, response):
        pass
