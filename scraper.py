import scrapy

class FacebookGroupSpider(scrapy.Spider):
    name = 'facebook_group'
    allowed_domains = ['facebook.com']
    start_urls = [
        'https://www.facebook.com/groups/feed'  # Replace with the actual group URL
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    keywords = ['wordpress', 'wix', 'seo', 'web developer', 'web designer', 'social media marketing', 'email marketing', 'digital marketing']

    def parse(self, response):
        posts = response.css('div[data-testid="post_message"]')
        for post in posts:
            post_text = post.css('::text').get()
            for keyword in self.keywords:
                if keyword.lower() in post_text.lower():
                    yield {
                        'keyword': keyword,
                        'post_text': post_text
                    }
        next_page = response.css('a[href*="groups/your-group-id/?epa=SEARCH_BOX&refid=18"]::attr(href)').get()  # Adjust selector as needed
        if next_page:
            yield response.follow(next_page, self.parse)
