from scrapy.http import HtmlResponse
from scrapy.selector import Selector

def all_comments(body: HtmlResponse) -> list:
    return body.xpath("//div[contains(@class, 'userContentWrapper')]").extract()

def get_if_exists(selector, xpath: str) -> str:
    content = selector.xpath(xpath).extract()
    if len(content) > 0:
        return content[0]
    
    return "N/A"

def get_name(selector) -> str:
    private_name = get_if_exists(selector, "//h5//span[contains(@class, '_39_n')]/text()")
    if private_name == "N/A":
        return get_if_exists(selector, "//h5//a/text()")
    
    return private_name

def comment_data(comment: str) -> dict:
    selector = HtmlResponse(url="", body=comment, encoding="utf-8")
    return {
        "link": get_if_exists(selector, "//h5//a/@href"),
        "name": get_name(selector),
        "comment": get_if_exists(selector, "//p"),
        "timestamp": get_if_exists(selector, "//span[contains(@class, 'timestampContent')]/text()"),
    }

def first_user(body: HtmlResponse) -> str:
    return body.xpath("//div[contains(@class, 'userContentWrapper')]//h5//span[@class='fwb fcg']//a/text()").extract()[0]