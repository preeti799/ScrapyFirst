import scrapy


class Maserati(scrapy.Spider):
    name = "Maserati"
    allowed_domains = ["www.maseratilife.com"]
    start_urls = ["https://www.maseratilife.com/forums/"]

# MAIN PAGE:

    # get subsection link:
    def parse(self, response):

        sub_section_link = response.css("div.node-body")

        for i in sub_section_link:
            sub_section_url = i.css('h3.node-title a::attr(href)').get()

            # exclude certain sub-section link:
            excluded_urls = ['/forums/4x4-shop-canada.241/', '/forums/a-s-motorsport.74/', '/forums/asia.33/',
                             '/forums/carid-com.113/', '/forums/dashlynx-com.243/',
                             '/forums/ebc-brakes.239/', '/forums/fc-kerbeck-maserati.242/',
                             '/forums/loudoun-county-exotics.219/', '/forums/maseratilife-market.146/',
                             '/forums/middle-east.45/', '/forums/north-america.20/', '/forums/vendor-deals.238/',
                             '/forums/maseratilife-news.130/', '/forums/maserati-events.69/',
                             '/forums/maserati-registry.35/','/forums/modern-maserati.7/',
                             '/forums/europe.18/']

            if sub_section_url not in excluded_urls:
                sl_url = "https://www.maseratilife.com" + sub_section_url
                yield response.follow(sl_url, callback=self.parse_sub_section_page)

# IN SUB-SECTION PAGE:

    # get thread link:
    def parse_sub_section_page(self, response):

        thread_link = response.css("div.california-thread-item  ")

        for tl in thread_link:
            relative_thread_url = tl.css("h3.structItem-title>a::attr(href)").get()
            tl_url = "https://www.maseratilife.com" + relative_thread_url

            yield response.follow(tl_url, callback=self.parse_thread_page)

# IN THREAD PAGE:

    def parse_thread_page(self, response):

        section_name = response.css('ul.p-breadcrumbs li[itemprop="itemListElement"] a span::text').getall()[3]
        thread_id = response.css("div.p-body-pageContent>script::text").get().split()[2]
        thread_title = response.css('h1.MessageCard__thread-title::text').get()
        thread_views = response.css("div.MessageCard__thread-info>span::text").re(r'\d+')[0]
        thread_replies = response.css("div.MessageCard__thread-info>span::text").re(r'\d+')[1]
        thread_participants = response.css("div.MessageCard__thread-info>span::text").re(r'\d+')[2]
        thread = response.xpath('//div[@class= "MessageCard js-messageCard "]')

        for i in thread:
            post_id = i.xpath('//div[@class="MessageCard js-messageCard "]/@id').get()
            content = i.css('div.bbWrapper::text').get()
            date = i.css('time.u-dt::attr(data-date-string)').get()
            time = i.css('time.u-dt::attr(data-time-string)').get()
            sender_name = i.css('h4.MessageCard__user-info__name>a::text').get()
            post_order = i.css('a.MessageCard__post-position::text').get()
            post_order_clean = post_order.strip().replace('\n', '').replace('#', '') if post_order else None

            yield {
                'Post_ID': post_id,
                'Section_Name': section_name,
                'Thread_ID': thread_id,
                'Thread_Views': thread_views,
                'Thread_Total_Participants': thread_participants,
                'Thread_Replies': thread_replies,
                'Thread_Title': thread_title,
                'Sender_UserName': sender_name,
                'Date': date,
                'Time': time,
                'Content': content,
                'Post_Order': post_order_clean

            }






