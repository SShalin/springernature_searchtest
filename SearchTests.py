from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import etree
import requests

# Load the page and run search on Stonehenge
driver = webdriver.Firefox()
base_url = "https://link.springer.com"
driver.get(base_url)
assert "Home - Springer" in driver.title
elem = driver.find_element_by_name("query")
elem.clear()
elem.send_keys("Stonehenge")
elem.send_keys(Keys.RETURN)

resultCount = driver.find_element_by_xpath('//*[@id="kb-nav--main"]/div[1]/h1').text
print(resultCount)

# Read the first ten links from search results.
d = etree.HTML(driver.page_source)
urls = []
i = 1
while i <= 10:
    try:
        href = d.xpath('//*[@id="results-list"]/li[{0}]/h2/a/@href'.format(i))
        urls.append(str(base_url + href[0]))
        i += 1
    except:
        break

urls.append('https://link.springer.com/chapter/10.1057/978-1-349-94850-5_3_invalid')


# Try loading the first ten urls to make sure the page exists and store invalid urls.
invalidUrls = []
for url in urls:
    print("Testing url " + url)
    r = requests.get(url)
    r.status_code
    if r.status_code == 404:
        invalidUrls.append(url)


if len(invalidUrls) > 0:
    print("Following urls were invalid:")
    for url in invalidUrls:
        print(url)
else:
    print("There are no invalid urls.")
driver.close()

