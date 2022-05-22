"""
This file contains the definitions for the Scraper class as well as its child
classes.
"""

import json
import requests
import pandas as pd

from abc import abstractmethod
from src.config import config
from bs4 import BeautifulSoup


class Scraper:
    """
        A Scraper scrapes through a website and saves the required data as JSON
        files.

        Attributes
        ----------
        base_url : str
            The base URL to be scraped without additional endpoints.

        Methods
        ----------
        run()
            Scrapes through a website and saves the required data as a single
            JSON file under the data/raw/ directory.
        scrape()
            Scrapes through various pages of a website and generates the result
            as a list of dicts.
        save()
            Saves the scraped data as a JSON file under the data/raw/
            directory.
    """

    def __init__(self, base_url: str) -> None:
        """
            Instantiates a Scraper object.
        """
        self.base_url = base_url

    def run(self) -> None:
        """
            Scrapes through a website and saves the required data as a JSON
            file under the data/raw/ directory.
        """
        scraped_data = self.scrape()
        self.save(scraped_data)

    @abstractmethod
    def scrape(self) -> list[dict]:
        """
            Scrapes through various pages of a website and generates the result
            as a list of dicts.
        """
        result = []
        able_to_open = True
        page_start_with = 1

        # ?: A while loop that will keep running until the condition is met.
        while able_to_open:
            # ?: Make reequest to landing page
            page_url = f'{self.base_url}catalogue/page-{page_start_with}.html'
            res = requests.get(page_url)
            print(f'[INFO] : Page#{page_start_with} | {page_url}')
            if res.status_code == 200:
                print('[INFO] : Successful (200)')
                soup = BeautifulSoup(res.text, 'html.parser')
                for article in soup.find_all('article', {'class': 'product_pod'}):
                    image_attr = article.find('h3').find_next('a').attrs
                    product_title = image_attr["title"]
                    product_rating = article.find('p').attrs['class'][1]

                    # ?: Make request to product page
                    real_href = f'catalogue/{image_attr["href"]}' if 'catalogue' not in image_attr['href'] else image_attr['href']
                    next_url = f'{self.base_url}{real_href}'
                    print(f'>>>> [{page_start_with}] : {next_url}')
                    product_page = BeautifulSoup(requests.get(next_url).text, 'html.parser')

                    # ?: Data encapsulation
                    product_info = dict(zip([_.get_text() for _ in product_page.find('table', {'class': 'table table-striped'}).find_all('th')], [_.get_text() for _ in product_page.find('table', {'class': 'table table-striped'}).find_all('td')]))

                    # ?: Check whether description data is available or not
                    if product_page.find('div', {'id': 'product_description'}):
                        product_info['Description'] = product_page.find('div', {'id': 'product_description'}).find_next('p').text
                    else:
                        product_info['Description'] = '-'

                    product_info['Rating'] = product_rating
                    product_info['Title'] = product_title
                    print(json.dumps(product_info, indent=4, ensure_ascii=False))
                    print('-' * 150)

                    result.append(product_info) # ?: Dump records
                page_start_with += 1

            elif res.status_code == 404:
                print('[ERROR] : Error 404 page not found')
                able_to_open = False
            else:
                print('[ERROR] : Not both 200 and 404')
                able_to_open = False

        return result

    def save(self, data: list[dict]) -> None:
        """
            Saves the scraped data as a JSON file under the data/raw/
            directory.
        """
        with open(f'{config["RAW_DIRECTORY"]}/data.json', 'w') as fp:
            json.dump(data, fp, indent=4, ensure_ascii=False)


class BookScraper(Scraper):
    """
        A BookScraper is a child of Scraper that scrapes data of all the books
        listed on http://books.toscrape.com.
    """

    # def extract_book_links(self, text) -> list[str]:
    #     """
    #         This helper method takes in the content of a book-listing page (a
    #         string of html) and returns a list of urls of book-detail pages from
    #         which to scrape data.
    #     """

    # def get_product_info(self, text: str) -> dict:
    #     """
    #         This helper method takes in the content of a book-detail page (a
    #         string of html) and returns a dictionary corresponding to a record
    #         in the output JSON file.
    #     """
