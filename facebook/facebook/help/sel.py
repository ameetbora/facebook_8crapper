from scrapy.http import HtmlResponse
from scrapy.selector import Selector

def all_comments(body: HtmlResponse) -> list:
    return body.xpath("//div[contains(@class, 'userContentWrapper')]").extract()

def get_if_exists(selector, xpath: str) -> str:
    content = selector.xpath(xpath).extract()
    if len(content) > 0:
        return content[0]
    
    return "N/A"

def get_int_if_exists(selector, xpath: str) -> int:
    content = selector.xpath(xpath).extract()
    if len(content) > 0:
        return int(content[0])
    
    return 0

def get_comment_number(selector) -> int:
    content = selector.xpath("//a[@data-comment-prelude-ref]/text()").extract()
    if len(content) > 0:
        return int(content[0].split(" ")[0])
    
    return 0

def get_name(selector) -> str:
    private_name = get_if_exists(selector, "//span[@class='fwb fcg']//span[contains(@class, '_39_n')]/text()")
    if private_name == "N/A":
        return get_if_exists(selector, "//span[@class='fwb fcg']//a/text()")
    
    return private_name

def comment_data(comment: str) -> dict:
    selector = HtmlResponse(url="", body=comment, encoding="utf-8")
    return {
        "link": get_if_exists(selector, "//span[@class='fwb fcg']//a/@href"),
        "name": get_name(selector),
        "comment": get_if_exists(selector, "//p/text()"),
        "timestamp": get_int_if_exists(selector, "//span[contains(@class, 'timestampContent')]/parent::abbr/@data-utime"),
        # "reacts": get_int_if_exists(selector, "//span[@aria-label='See who reacted to this']/following-sibling::a/span/span/text()"),
        # "comment_number": get_comment_number(selector),
        # "comments_link": get_if_exists(selector, "//a[@data-comment-prelude-ref]/@href")
    }

def first_user(body: HtmlResponse) -> str:
    return body.xpath("//div[contains(@class, 'userContentWrapper')]//span[@class='fwb fcg']//a/text()").extract()[0]