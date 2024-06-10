import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_rotten_tomatoes_score(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Pull critic score from RT HTML page
    score_tag = soup.find('rt-button', slot='criticsScore').get_text(strip=True)
    if score_tag:
        score = score_tag #.get_text(strip=True)
        return score
    else:
        return 'Score not found'

#Write results to sheet
def update_google_sheet(data, sheet):
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            sheet.update_cell(i+1, j+1, val)

def main():
    # Read URLs from text file
    with open('urls.txt', 'r') as file:
        urls = file.readlines()

    # Strip any extra whitespace characters from URLs
    urls = [url.strip() for url in urls]

    # Initialize data list for Google Sheets
    data = []

    for url in urls:
        movie_name = url.split('/')[-1].replace('_', ' ').title()
        score = get_rotten_tomatoes_score(url)
        data.append([movie_name, score])

    # Test print data
    # print(data)

    # Google Sheets setup
    credentials_file = 'rtscores.json'
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Rotten Tomatoes Scores").sheet1

    # Update the Google Sheet with the scraped data
    update_google_sheet(data, sheet)
    print(f'Updated Google Sheet with the following data: {data}')

if __name__ == '__main__':
    main()
