import scrapy
from facebook.help import sel, conv
from facebook import db

max_cn = 222645646350
small_step = 500000
step_size = 1500000
dub_step = 3000000

bunnings = "https://www.facebook.com/pages_reaction_units/more/?page_id=539309746236829&cursor=%7B%22timeline_cursor%22%3A%{cn}%22%2C%22timeline_section_cursor%22%3Anull%2C%22has_next_page%22%3Afalse%7D&surface=www_pages_community_tab&unit_count=8&dpr=1&fb_dtsg_ag&__user=0&__a=1&__req=4&__be=-1&__pc=PHASED%3ADEFAULT&__rev=4376521"



class QuotesSpider(scrapy.Spider):
    name = "comments"

    def __init__(self):
        self.db = db.db()
        self.prev_highest_cn = self.db.get_highest_cn()
        self.recent_identifiers = []
        self.duplicate_count = 0


    def start_requests(self):
        # Find a good starting comment number
        yield scrapy.Request(
            url=bunnings.format(cn=max_cn), 
            callback=self.find_starting_cn
        )

    def parse(self, response):
        if QuotesSpider.has_correct_content_type:
            self.current_cn -= small_step
            yield scrapy.Request(
                url=bunnings.format(cn=self.current_cn),
                callback=self.parse
            )
            for comment in sel.all_comments(conv.body_html(response.body)):
                comment_data = sel.comment_data(comment)
                if not self.is_duplicate(comment_data):
                    yield comment_data

    def find_starting_cn(self, response):
        print("------------------------------------------")
        if QuotesSpider.has_correct_content_type:
            self.starting_cn = self.prev_highest_cn
            self.higher_cn = self.starting_cn + dub_step
            self.first_user = sel.first_user(conv.body_html(response.body))
            yield scrapy.Request(
                url=bunnings.format(cn=self.higher_cn),
                callback=self.check_higher_cn
            )

    def check_higher_cn(self, response):
        # keep stepping upwards until the first name remains the same (at which point we've reached the cn for the first comment 
        if QuotesSpider.has_correct_content_type:
            new_first_user = sel.first_user(conv.body_html(response.body))
            if new_first_user != self.first_user:
                self.first_user = new_first_user
                self.starting_cn = self.higher_cn
                self.higher_cn = self.starting_cn + dub_step
                yield scrapy.Request(
                    url=bunnings.format(cn=self.higher_cn),
                    callback=self.check_higher_cn
                )
            else:
                if self.prev_highest_cn != self.starting_cn:
                    print("New highest observed comment number: {}".format(self.starting_cn))
                    self.db.update_highest_cn(self.starting_cn)

                # Keep stepping down the cn recording comments until there are no more comments
                self.current_cn = self.starting_cn
                yield scrapy.Request(
                    url=bunnings.format(cn=self.current_cn),
                    callback=self.parse
                )

    def is_duplicate(self, comment: dict) -> bool:
        identifier = comment["name"] + comment["timestamp"] + comment["link"]
        if identifier in self.recent_identifiers:
            self.duplicate_count += 1
            print(self.duplicate_count)
            return True
        
        self.update_duplicates(identifier)
        return False
    
    def update_duplicates(self, new_identifier: str):
        if len(self.recent_identifiers) > 100:
            self.recent_identifiers.pop(0)

        self.recent_identifiers.append(new_identifier)

    @staticmethod
    def has_correct_content_type(response) -> bool:
        content_type = conv.to_str(response.headers[b"content-type"])
        if "application/x-javascript" not in content_type:
            if "text/html" in content_type:
                print("We got an unexpected response, aborting scrape")
                return False

            print("We got an unexpected response, aborting scrape")
            return False

        try:
            conv.to_json(response.body)
        except:
            return False

        return True