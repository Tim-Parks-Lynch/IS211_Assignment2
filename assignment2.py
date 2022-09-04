import argparse
import requests
import csv
import logging
import datetime

def downloadData(url):
    """Downloads the data"""
    response = requests.get(url)
    return response.text

def processData(file_content):
    user_data = {}
    row = file_content.split("\n")

    try:
        for line in row[1:]:
            id, name, birthday = line.split(",")
            user_data[id] = (name, birthday)
    except:
        user_data[id] = "Dang something went wrong"
    
    print(user_data)
    print("-----------")
    print(user_data['16'])

def displayPerson(id, personData):
    pass

def main(url):
    print(f"Running main with URL = {url}...")


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
    url = args.url
    response = downloadData(url)
    processData(response)