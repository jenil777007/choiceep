from datetime import datetime
from urllib.request import Request, urlopen as uReq

from bs4 import BeautifulSoup as soup

from MongoClient import *

logging.basicConfig(format='%(asctime)s - %(message)s')


# url = 'https://www.flipkart.com/search?q=mobile'


# The following function is used to make various requests for different products
# @param url as a string
# @returns raw html of requested page


def make_request_and_return_raw_html(request_url):
    request_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:54.0) Gecko/20100101 Firefox/54.0'}
    request = Request(request_url, headers=request_headers)
    client = uReq(request)
    raw_html = client.read()
    client.close()
    return raw_html


for url in URLS_TO_CRAWL:
    # The initial point of crawler where different products are listed
    soupContent = soup(make_request_and_return_raw_html(url), "html.parser")
    # Selecting the right part of the html page where outer wrapper of the list is present
    productsWrapper = soupContent.findAll("div", {"class": "_1HmYoV _35HD7C col-10-12"})
    # The exact division where the list of products is located
    products = productsWrapper[0].findAll("div", {"class": "bhgxx2 col-12-12"})

    # Extract each product link from the list, fetch raw html of the product page and extract offer details
    for index, product in enumerate(products):
        if index == 0:
            continue
        if index > NO_OF_ITEMS_TO_CRAWL_THRESHOLD:
            break

        productLink = product.findAll("a", {"class": "_31qSD5"})  # type: object

        rawHtmlContentFetchedFromProductLink = soup(
            make_request_and_return_raw_html(BASE_URL_FLIPKART + productLink[0]["href"]), "html.parser")
        productDetailsWrapper = rawHtmlContentFetchedFromProductLink.findAll("div",
                                                                             {"class": "_1HmYoV _35HD7C col-8-12"})
        productCategory = productDetailsWrapper[0].findAll("div", {"class": "_1HEvv0"})[1].a.text
        offersAndRulesSpans = productDetailsWrapper[0].findAll("span", {"class": "_7g_MLT row"})

        for idx, span in enumerate(offersAndRulesSpans):
            if span.li.span.text == "Bank Offer":
                print("offer")
                offerDescription = span.li.span.findNext('span').contents[0]
                print(offerDescription)

                document = dict()
                document["siteName"] = url.split(".")[1].title()
                document["productCategory"] = productCategory
                # document["creditCardProvider"] =
                document["offerDescription"] = offerDescription

                # if document present in db with above mentioned params
                #     fetch it from db
                #     check if the date is same as today's
                #       if yes then update timestamp to systime and update it to db
                #       else insert new document
                # else
                #     insert document into the db

                foundDocuments = find_document_in_db(document)
                if foundDocuments is not None:
                    for fd in foundDocuments:
                        document["timeStamp"] = datetime.now()
                        if fd['timeStamp'].date() == document["timeStamp"].date():
                            fd['timeStamp'] = datetime.now()
                            update_timeStamp_of_document_in_db(fd)
                        else:
                            insert_document_into_db(document)
                else:
                    print("Couldn't find the document in the db -> " + str(document))

                    insert_document_into_db(document)
