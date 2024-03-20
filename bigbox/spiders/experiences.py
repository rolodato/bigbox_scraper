import scrapy


class ExperiencesSpider(scrapy.Spider):
    name = "experiences"
    allowed_domains = ["bigbox.com.ar"]
    start_urls = ["https://www.bigbox.com.ar/catalogo/eyJpZCI6NDIwNDI2N30:1rmeUV:TU4bJPjiJ6_NjzCW3Pt7odf4qL4/bonjour/"]

    def parse(self, response):
        pass
