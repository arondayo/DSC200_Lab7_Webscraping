# part 2 imports
import csv
from bs4 import BeautifulSoup as bSoup
import requests as rq, time

# part 3 imports
from selenium import webdriver
import pandas as pd


# ===== Part 2 =====

#store the URL for later use
url = "https://en.wikipedia.org/wiki/List_of_college_athletic_programs_in_Kentucky"

#sleep to avoid overwhelming the server
time.sleep(5)

#send a request to the page for the content
response = rq.get(url)

#make sure the request was successful
if response.status_code == 200:
    #using Beautiful Soup, parse the content
    soup = bSoup(response.text, 'html.parser')

    #find the tables containing the relevant data based on their HTML class
    tables = soup.find_all('table', {'class': 'wikitable'})

    # list container for college data
    colleges = []
    headers = []

    #loop through each table to collect data
    for table in tables:
        #sleep between processing tables to be more respectful to the server
        time.sleep(5)

        #get the header row by finding the <th> elements
        headers = [th.get_text(strip=True) for th in table.find_all('th')]

        #extract data rows but do not include the header row
        for row in table.find_all('tr')[1:]:
            cells = row.find_all('td')
            #check if the row has data cells
            if len(cells) > 0:
                row_data = []

                for cell in cells:
                    cell_text = cell.get_text(strip=True)
                    row_data.append(cell_text)

                colleges.append(row_data)

    #write all of the data to a CSV file
    csv_data = 'data/group_1_task2.csv'
    with open(csv_data, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        writer.writerows(colleges)

    print("The data has been saved into data/group1_task2.csv")

#else in case the request is denied
else:
    print("Failed to download the data")

# ===== Part 3 =====

# from https://catalog.data.gov/dataset?q=&sort=views_recent+desc
# gather the first 5 pages' data and write them to a csv file
# Gather the following for each entry:
#   dataset_name, source, description, csv_link, rdf_link, json_link, xml_link, zip_link, html_link, view_count

headers = ['dataset_name', 'source', 'description', 'csv_link', 'rdf_link', 'json_link', 'xml_link', 'zip_link', 'html_link', 'view_count']
rows = []

for page in range(1, 6):
    url = f'https://catalog.data.gov/dataset/?q=&sort=views_recent+desc&page={page}'
    # response = rq.get(url) # this cannot retrieve 'recent views' element because it's populated with js
    # selenium must be used instead

    driver = webdriver.Chrome()
    driver.get(url)
    # driver.implicitly_wait(0)
    time.sleep(1.5) # this is needed to let the webpage retrieve the data for the 'recent views' element

    soup = bSoup(driver.page_source, 'html.parser')

    for entry in soup.find_all('div', class_='dataset-content'):
        links_ul = entry.find('ul', class_='dataset-resources unstyled') # finds the ul element containing the <a href>s
        if not links_ul:
            extracted_links = [None, None, None, None, None, None] # if there are no links of desire fill with None
        else:
            a_csv = links_ul.find_all('a', {'data-format': 'csv'}) # finds all the <a> tags marked with the data format we want
            a_rdf = links_ul.find_all('a', {'data-format': 'rdf'})
            a_json = links_ul.find_all('a', {'data-format': 'json'})
            a_xml = links_ul.find_all('a', {'data-format': 'xml'})
            a_zip = links_ul.find_all('a', {'data-format': 'zip'})
            a_html = links_ul.find_all('a', {'data-format': 'html'})

            a_list = [a_csv, a_rdf, a_json, a_xml, a_zip, a_html]
            extracted_links = []
            for x in a_list: # places None if absent, the lone value if only 1 exists, the entire list if >1
                if not x:
                    extracted_links.append(None)
                else:
                    buffer = []
                    for item in x:
                        buffer.append(item.get('href'))
                    if len(buffer) == 1:
                        extracted_links.append(buffer[0])
                    else:
                        extracted_links.append(buffer)

        row = [
            entry.find('h3', class_='dataset-heading').find('a').text,
            entry.find('p', class_='dataset-organization').text[:-2], # [:-2] strips the ending " —" off the end
            entry.find('div', class_='notes').find('div').text,
            extracted_links[0],
            extracted_links[1],
            extracted_links[2],
            extracted_links[3],
            extracted_links[4],
            extracted_links[5],
            entry.find('span', class_='recent-views recent-views-datagov').get('title')
        ]

        rows.append(row)
    driver.close()

df = pd.DataFrame(rows, columns=headers)
print("[=============== PART 3 ===============]")
print("========== Info ==========")
print(df.info())
print("========== Shape ==========")
print(df.shape)

df.to_csv('data/group_1_task3.csv', index=False)