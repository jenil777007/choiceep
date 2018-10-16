import bs4
from urllib.request import Request, urlopen as uReq
from bs4 import BeautifulSoup as soup

BASE_URL = 'https://www.flipkart.com'

url = 'https://www.flipkart.com/search?q=mobile'


def make_request_and_return_raw_html(request_url):
    request_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:54.0) Gecko/20100101 Firefox/54.0'}
    request = Request(request_url, headers=request_headers)
    client = uReq(request)
    raw_html = client.read()
    client.close()
    return raw_html


soupContent = soup(make_request_and_return_raw_html(url), "html.parser")

productsWrapper = soupContent.findAll("div", {"class": "_1HmYoV _35HD7C col-10-12"})

products = productsWrapper[0].findAll("div", {"class": "bhgxx2 col-12-12"})

for index, product in enumerate(products):
    if index == 0:
        continue
    if index > 9:
        break
    productLink = product.findAll("a", {"class": "_31qSD5"})  # type: object

    rawContentFetchedFromProductLink = soup(make_request_and_return_raw_html(BASE_URL + productLink[0]["href"]), "html.parser")
    productDetailsWrapper = rawContentFetchedFromProductLink.findAll("div", {"class": "_1HmYoV _35HD7C col-8-12"})
    offersAndRulesSpans = productDetailsWrapper[0].findAll("span", {"class": "_7g_MLT row"})

    for idx, span in enumerate(offersAndRulesSpans):
        if span.li.span.text == "Bank Offer":
            print("offer")
            offerString = span.li.span.findNext('span').contents[0]
            print(offerString)
