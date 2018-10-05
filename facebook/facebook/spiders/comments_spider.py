import scrapy
from facebook.help import sel, conv, brain
from facebook import db

max_cn = 222645646350
small_step = 500000
step_size = 1500000
dub_step = 3000000
huge_step = 10000000

user_id = 100029134355964

cookies = {
    "sb": "ujE-Wx_N7mAfj_KH9zn88r05", 
    "datr": "zz-0W_wy4tVFej-dHfB_gpJG",
    "locale": "en_GB",
    "c_user": 100029134355964, 
    "xs": "19%3AVb_XML1n9Y-QhQ%3A2%3A1538694465%3A-1%3A-1",
    "pl": "n", 
    "spin": "r.4384677_b.trunk_t.1538694467_s.1_v.2_",
    "js_ver": "3198",
    "act": "1538695670528%2F0", 
    "fr": "0TBET0XuOT7D3paQC.AWW1ebrcsOrtDKsAVTgWDUiEeuQ.BbPjG6.6m.AAA.0.0.Bbtrl1.AWULuFtT",
    "wd": "1212x796", 
    "presence": "EDvF3EtimeF1538703333EuserFA21B29134355964A2EstateFDt3F_5b_5dG538703333509CEchFDp_5f1B29134355964F26CC"
}

red_energy = "https://www.facebook.com/pages_reaction_units/more/?page_id=1951319155178263&cursor=%7B%22timeline_cursor%22%3A{cn}%22%2C%22timeline_section_cursor%22%3Anull%2C%22has_next_page%22%3Afalse%7D&surface=www_pages_community_tab&unit_count=8&dpr=1&fb_dtsg_ag=AdyeydpUU00A-U3uX3ZOPYZuTgN51TTB0F2yryuPX19JeQ%3AAdzEL3n8o1cIPbsishRhqtdSsuMMxSYstUGZgY5oynRPBg&__user=100029134355964&__a=1&__dyn=7AgNe-4amaUmgDxiWJGi9FxqeCwKyaF3ozzrheCHxG7Uqzob4q6oG8zFGUpxSaxuq32bG4UJoK48G5WAxamjDK7Hze3KFQ2m44aUeV94rzLwAxCuiaAz8gCwq8G9Km8yEqx61cxl0zCx2i10GfCCzVK5e9wg8lDCzopwxzoGqfw-KEK4ooAghzRGm5Apy8lwxgC3mbKbzUC26dwjUgUkBzVKey8eohxTxu4FeaDU8KU98rUC6olzaz9rx6uexfCw8Odz84GbKezHAy8uyUaoGWyXwhUky9UpxG9w&__req=7&__be=1&__pc=PHASED%3ADEFAULT&__rev=4384677&__spin_r=4384677&__spin_b=trunk&__spin_t=1538694467"

origin_energy = "https://www.facebook.com/pages_reaction_units/more/?page_id=206261246078617&cursor=%7B%22timeline_cursor%22%3A%{cn}%22%2C%22timeline_section_cursor%22%3Anull%2C%22has_next_page%22%3Afalse%7D&surface=www_pages_community_tab&unit_count=8&dpr=1&fb_dtsg_ag=AdyeydpUU00A-U3uX3ZOPYZuTgN51TTB0F2yryuPX19JeQ%3AAdzEL3n8o1cIPbsishRhqtdSsuMMxSYstUGZgY5oynRPBg&__user=100029134355964&__a=1&__dyn=7AgNe-4amaUmgDxiWJGi9FxqeCwKyaF3ozzrheCHxG7Uqzob4q6oG8zFGUpxSaxuq32bG4UJoK48G5WAxamjDK7Hze3KFQ2m44aUeV94rzLwAxCuiaAz8gCwq8G9Km8yEqx61cxl0zCx2i10GfCCzVK5e9wg8lDCzopwxzoGqfw-KEK4ooAghzRGm5Apy8lwxgC3mbKbzUC26dwjUgUkBzVKey8eohxTxu4FeaDU8KU98rUC6olzaz9rx6uexfCw8Odz84GbKezHAy8uyUaoGWyXwhUky9UpxG9w&__req=6&__be=1&__pc=PHASED%3ADEFAULT&__rev=4384677&__spin_r=4384677&__spin_b=trunk&__spin_t=1538694467"

energy_oz = "https://www.facebook.com/pages_reaction_units/more/?page_id=539309746236829&cursor=%7B%22timeline_cursor%22%3A%{cn}%22%2C%22timeline_section_cursor%22%3Anull%2C%22has_next_page%22%3Afalse%7D&surface=www_pages_community_tab&unit_count=8&dpr=1&fb_dtsg_ag&__user=100029134355964&__a=1&__req=4&__be=-1&__pc=PHASED%3ADEFAULT&__rev=4376521"


bunnings = "https://www.facebook.com/pages_reaction_units/more/?page_id=1657775594549456&cursor=%7B%22timeline_cursor%22%3A%{cn}%22%2C%22timeline_section_cursor%22%3Anull%2C%22has_next_page%22%3Afalse%7D&surface=www_pages_community_tab&unit_count=8&dpr=1&__user=100029134355964&fb_dtsg_ag&__user=0&__a=1&__req=4&__be=-1&__pc=PHASED%3ADEFAULT&__rev=4376521"


page_url = "https://www.facebook.com/pages_reaction_units/more/?page_id=1951319155178263&cursor=%7B%22timeline_cursor%22%3A%{cn}%22%2C%22timeline_section_cursor%22%3Anull%2C%22has_next_page%22%3Afalse%7D&surface=www_pages_community_tab&unit_count=8&dpr=1&__user=100029134355964&__a=1&__req=7&__be=1&__pc=PHASED%3ADEFAULT&__rev=4384677&__spin_r=4384677&__spin_b=trunk&__spin_t=1538694467"


class QuotesSpider(scrapy.Spider):
    name = "comments"

    def __init__(self):
        self.db = db.db()
        self.prev_highest_cn = self.db.get_highest_cn()
        self.brain = brain.brain()

    def start_requests(self):
        # Find a good starting comment number
        yield scrapy.Request(
            url=page_url.format(cn=max_cn), 
            cookies=cookies,
            callback=self.find_starting_cn
        )

    def parse(self, response):
        if QuotesSpider.has_correct_content_type(response):
            comments_to_save = []
            for comment in sel.all_comments(conv.body_html(response.body)):
                comment_data = sel.comment_data(comment)
                if not self.brain.is_duplicate(comment_data):
                    comments_to_save.append(comment_data)

            self.current_cn -= self.brain.step()
            yield scrapy.Request(
                url=page_url.format(cn=self.current_cn),
                cookies=cookies,
                callback=self.parse
            )

            for comment in comments_to_save:
                self.db.save_comment(comment)

    def find_starting_cn(self, response):
        if QuotesSpider.has_correct_content_type(response):
            self.starting_cn = self.prev_highest_cn
            self.higher_cn = self.starting_cn + dub_step
            self.first_user = sel.first_user(conv.body_html(response.body))
            yield scrapy.Request(
                url=page_url.format(cn=self.higher_cn),
                cookies=cookies,
                callback=self.check_higher_cn
            )

    def check_higher_cn(self, response):
        # keep stepping upwards until the first name remains the same (at which point we've reached the cn for the first comment 
        if QuotesSpider.has_correct_content_type(response):
            new_first_user = sel.first_user(conv.body_html(response.body))
            if new_first_user != self.first_user:
                self.first_user = new_first_user
                self.starting_cn = self.higher_cn
                self.higher_cn = self.starting_cn + dub_step
                yield scrapy.Request(
                    url=page_url.format(cn=self.higher_cn),
                    cookies=cookies,
                    callback=self.check_higher_cn
                )
            else:
                if self.prev_highest_cn != self.starting_cn:
                    print("New highest observed comment number: {}".format(self.starting_cn))
                    self.db.update_highest_cn(self.starting_cn)

                # Keep stepping down the cn recording comments until there are no more comments
                self.current_cn = self.starting_cn
                yield scrapy.Request(
                    url=page_url.format(cn=self.current_cn),
                    cookies=cookies,
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