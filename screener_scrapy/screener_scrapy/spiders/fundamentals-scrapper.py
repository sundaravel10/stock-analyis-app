import scrapy

class FundamentalsSpider(scrapy.Spider):
     name = "Fundamentals"

     def start_requests(self):
         urls = [
             'https://www.screener.in/'
         ]

         for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

     def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'fundamental-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')