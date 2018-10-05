import json
from scrapy.http import HtmlResponse

def to_str(byte_string: bytes) -> str:
    return byte_string.decode("utf-8")

def to_json(response_body: bytes) -> dict:
    return json.loads(response_body[9:].decode('utf-8'))

def body_html(response_body: bytes) -> HtmlResponse:
    return HtmlResponse(
        url="",
        body=to_json(response_body)["domops"][0][3]["__html"],
        encoding="utf-8"
    ) 


    # return HtmlResponse(url="", body=to_json(response_body)["domops"][0][3]["__html"], encoding="utf-8") 
