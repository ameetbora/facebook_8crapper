import scrapy
from facebook.help import sel, conv, brain, url
from facebook import db

max_cn = 222645646350
small_step = 500000
step_size = 1500000
dub_step = 3000000
huge_step = 10000000

class CommentsSpider(scrapy.Spider):
    name = "comments"

    def __init__(self, base_url, cookies, supplier_id):
        self.db = db.db()
        self.prev_highest_cn = self.db.get_highest_cn()
        self.brain = brain.brain()
        self.base_url = base_url
        self.cookies = cookies
        self.supplier_id = supplier_id

    def start_requests(self):
        # Find a good starting comment number
        yield scrapy.Request(
            url=self.base_url.format(cn=max_cn), 
            cookies=self.cookies,
            callback=self.find_starting_cn
        )

    def parse(self, response):
        print("-----xxxxx-----xxxxxx------" + str(self.brain.current_step))
        if CommentsSpider.has_correct_content_type(response) and CommentsSpider.response_long_enough(response):
            comments_to_save = []
            for comment in sel.all_comments(conv.body_html(response.body)):
                comment_data = sel.comment_data(comment)
                if not self.brain.is_duplicate(comment_data):
                    comments_to_save.append(comment_data)

            self.current_cn -= self.brain.step()
            yield scrapy.Request(
                url=self.base_url.format(cn=self.current_cn),
                cookies=self.cookies,
                callback=self.parse
            )

            for comment in comments_to_save:
                self.db.save_comment(comment, self.supplier_id)
        else:
            print("Scrape finished")

    def find_starting_cn(self, response):
        if CommentsSpider.has_correct_content_type(response):
            self.starting_cn = self.prev_highest_cn
            self.higher_cn = self.starting_cn + dub_step
            self.first_user = sel.first_user(conv.body_html(response.body))
            yield scrapy.Request(
                url=self.base_url.format(cn=self.higher_cn),
                cookies=self.cookies,
                callback=self.check_higher_cn
            )

    def check_higher_cn(self, response):
        # keep stepping upwards until the first name remains the same (at which point we've reached the cn for the first comment 
        if CommentsSpider.has_correct_content_type(response):
            new_first_user = sel.first_user(conv.body_html(response.body))
            if new_first_user != self.first_user:
                self.first_user = new_first_user
                self.starting_cn = self.higher_cn
                self.higher_cn = self.starting_cn + dub_step
                yield scrapy.Request(
                    url=self.base_url.format(cn=self.higher_cn),
                    cookies=self.cookies,
                    callback=self.check_higher_cn
                )
            else:
                if self.prev_highest_cn != self.starting_cn:
                    print("New highest observed comment number: {}".format(self.starting_cn))
                    self.db.update_highest_cn(self.starting_cn)

                # Keep stepping down the cn recording comments until there are no more comments
                self.current_cn = self.starting_cn
                yield scrapy.Request(
                    url=self.base_url.format(cn=self.current_cn),
                    cookies=self.cookies,
                    callback=self.parse
                )

    @staticmethod
    def has_correct_content_type(response) -> bool:
        content_type = conv.to_str(response.headers[b"content-type"])
        if "application/x-javascript" not in content_type:
            if "text/html" in content_type:
                print("We got a blank response, concluding scrape")
                return False

            print("We got an unexpected response, aborting scrape")
            return False

        return True
    
    @staticmethod
    def response_long_enough(response) -> bool:
        return len(response.body) > 5000