# Webscraping / Webcrawling Lab

This lab utilizes requests and selenium to scrape the html from webpages and have them parsed via BeautifulSoup4.

Final file for submission: `group_1_Lab_7_Webscraping.py`
## Part 1

Evaluation of several websites for their ability to be scraped. 
## Part 2 

Scraping of one of the evaluated websites featured in part 1.
## Part 3

Scraping of the first 5 pages of: https://catalog.data.gov/dataset/?q=&sort=views_recent+desc

The target content is:
`['dataset_name', 'source', 'description', 'csv_link', 'rdf_link', 'json_link', 'xml_link', 'zip_link', 'html_link', 'view_count']`

`Selenium` is needed as the view count is not able to be extracted with `requests` as its populated with JS and injected after the webpage has already loaded.