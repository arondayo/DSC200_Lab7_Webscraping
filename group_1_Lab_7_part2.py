#import libraries to scrape, parse, and store data into a csv
from bs4 import BeautifulSoup
import csv
import requests
#import time to help the scraper scrape responsibly
import time

#store the URL for later use
url = "https://en.wikipedia.org/wiki/List_of_college_athletic_programs_in_Kentucky"

#sleep to avoid overwhelming the server
time.sleep(5)

#send a request to the page for the content
response = requests.get(url)

#make sure the request was successful
if response.status_code == 200:
    #using Beautiful Soup, parse the content
    soup = BeautifulSoup(response.text, 'html.parser')

    #find the tables containing the relevant data based on their HTML class
    tables = soup.find_all('table', class_="wikitable sortable")

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
    csv_data = 'college_data.csv'
    with open(csv_data, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        writer.writerows(colleges)

    print("The data has been saved into college_data.csv")

#else in case the request is denied
else:
    print("Failed to download the data")