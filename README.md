# book-to-scrape-using-bs4
To scraping data from http://books.toscrape.com/

## Task
Browse through the following fake on-line bookstore: http://books.toscrape.com/. This website is meant for toying with scraping.

The goal of the task is to create an end-to-end flow that scrapes the website for data on books, and then transform the scraped data so that the final CSV file contains only books that have at least a four-star rating and Price (incl. tax) under £20.

## Sample record
Below is a sample record from the JSON file if the Scraper is implemented correctly:
```json
{
	"UPC": "a897fe39b1053632",
	"Product Type": "Books",
	"Price (excl. tax)": "Â£51.77",
	"Price (incl. tax)": "Â£51.77",
	"Tax": "Â£0.00",
	"Availability": "In stock (22 available)",
	"Number of reviews": "0",
	"Description": "It's hard to imagine a world without A Light in the Attic.",
	"Rating": "Three",
	"Title": "A Light in the Attic"
}
```

## Getting started
```bash
python main.py
```