import json
from bs4 import BeautifulSoup
import requests

def preprocess(inputString):
    inputString = inputString.replace("[", "")
    inputString = inputString.replace("]", "")
    inputString = inputString.encode("ascii", "ignore") #Removing non-ASCII characters
    inputString = inputString.decode()
    return inputString

def scrapeWeather(url):
    #Downloading source code of web page
    req = requests.get(url, 'html.parser')
    content = req.text
    content = content.replace("<!--","")
    content = content.replace("-->","") #Removing comments from HTML

    #Extracting the relevant weather and pollution info from web page
    soup = BeautifulSoup(content, 'lxml')
    dict={}
    info = soup.find(class_='indexValue')
    dict['AQI'] = info.contents[0] #Scraping AQI value

    info = soup.find_all(class_='pollutant-item odd') #Looping over listed pollutants and recording them
    for block in info:
        children = block.findChildren('div' , recursive=True)
        pollutantName=(preprocess(children[0].contents[0]))
        pollutantValue=(preprocess(children[2].contents[0]))
        dict[pollutantName] = pollutantValue
            
    info = soup.find_all(class_='weather-item') #Looping for listed weather data and recording them
    for block in info:
        children = block.findChildren('div' , recursive=True)
        for child in children:
            if child.contents:
                weatherData = child.contents[0]
                weatherData = preprocess(weatherData)
                dict[child.attrs['class'][0]]=weatherData

    #Packaging weather data into JSON format
    json_object = json.dumps(dict, indent = 4) 
    return json_object

if __name__ == "__main__":
    url = 'https://air-quality.com/place/india/gurugram/d2853e61?lang=en&standard=aqi_us'
    print(scrapeWeather(url))