from lxml import etree
from facebook import db

# def write_likers_file(driver):
#     f = open("likers.html", "a")
#     f.write(driver.page_source)
#     f.close()

def save_likers(html, page_name: str, page_id: int):
    database = db.db()
    supplier_id = database.save_supplier(page_name, page_id)
    tree = etree.HTML(html)

    results = tree.xpath("//div[@data-testid='browse-result-content']")
    for result in results:
        database.save_like(
        {
            "name" : result.xpath(".//a[@class='_32mo']/@href")[0],
            "link" : result.xpath(".//a[@class='_32mo']/span/text()")[0],
        }, supplier_id)
    
    print("Saving complete")