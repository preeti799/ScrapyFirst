import scrapy


class MaseratiLife(scrapy.Spider):
    name = "MaseratiLife"
    allowed_domains = ["www.maseratilife.com"]
    start_urls = ["https://www.maseratilife.com/forums/"]

# MAIN PAGE:

    # get subsection link:
    def parse(self, response):
        sub_section_link = response.css("div.block")

        sub_section_url = sub_section_link.css('h3.node-title a::attr(href)').getall()

        # exclude certain sub-section link:
        excluded_urls = ['/forums/4x4-shop-canada.241/', '/forums/a-s-motorsport.74/', '/forums/asia.33/',
                         '/forums/carid-com.113/', '/forums/dashlynx-com.243/', '/forums/do-it-yourself-dyi.138/',
                         '/forums/ebc-brakes.239/', '/forums/fc-kerbeck-maserati.242/',
                         '/forums/loudoun-county-exotics.219/', '/forums/maseratilife-market.146/',
                         '/forums/middle-east.45/', '/forums/north-america.20/', '/forums/vendor-deals.238/',
                         '/forums/maseratilife-news.130/', '/forums/maserati-events.69/',
                         '/forums/maserati-registry.35/']

        for i in sub_section_url:
            if i not in excluded_urls:
                sl_url = "https://www.maseratilife.com" + i

                yield response.follow(sl_url, callback=self.parse_sub_section_page)

# IN SUB-SECTION PAGE:

    # get thread link:
    def parse_sub_section_page(self, response):

        thread_link = response.css("div.structItemContainer")

        for tl in thread_link:
            relative_thread_url = tl.css("h3.structItem-title>a::attr(href)").get()
            tl_url = "https://www.maseratilife.com" + relative_thread_url

            yield response.follow(tl_url, callback=self.parse_thread_page)

# IN THREAD PAGE:

    def parse_thread_page(self, response):

        Thread = response.css('div.bbWrapper')

        for i in Thread:
            Content = i.css('div.bbWrapper::text').get()

            yield {
                'Content': Content
            }









