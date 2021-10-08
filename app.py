import json
from bs4 import BeautifulSoup
import requests

def scrapeWeather(url):
    #Downloading source code of web page
    req = requests.get(url, 'html.parser')
    content = req.text

    #Extracting the relevant weather info from web page
    soup = BeautifulSoup(content, 'lxml')
    info = soup.find_all(class_='weather-item')
    dict={}
    for block in info:
        children = block.findChildren('div' , recursive=True)
        for child in children:
            if child.contents:
                weatherData = child.contents[0]
                weatherData = weatherData.replace("[", "")
                weatherData = weatherData.replace("]", "")
                weatherData = weatherData.encode("ascii", "ignore") #Removing non-ASCII characters
                weatherData = weatherData.decode()
                dict[child.attrs['class'][0]]=weatherData

    #Packaging weather data into JSON format
    json_object = json.dumps(dict, indent = 4) 
    return json_object

if __name__ == "__main__":
    url = 'https://air-quality.com/place/india/gurugram/d2853e61?lang=en&standard=aqi_us'
    print(scrapeWeather(url))