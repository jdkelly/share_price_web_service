import requests
from bs4 import BeautifulSoup


def scrape_page(url):
    """
    Scrape web data from webpage and return Beautiful Soup object
    """
    request = requests.get(url)

    # Check that get request is successful
    if '<Response [200]>' not in str(request):
        return 'Get request failed: ' + str(request)

    # Parse using BS4
    return BeautifulSoup(request.text, 'html.parser')

