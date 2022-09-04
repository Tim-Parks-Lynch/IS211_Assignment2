import argparse
import requests
import logging
from datetime import datetime


def logger_creator(logger_name, output_file, message):
    # Create custom logger
    logger = logging.getLogger(logger_name)

    # Create handler
    # stream_handler = logging.StreamHandler() # outputs to console
    file_handler = logging.FileHandler(output_file)

    # Set level
    # stream_handler.setLevel(logging.ERROR)
    file_handler.setLevel(logging.ERROR)

    # Checks if handlers already exist, if so clears them
    # Christ on a cracker, remember this for the future, stops multiples of the same error being logged
    if logger.hasHandlers():
        logger.handlers.clear()

    # logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    logger.error(message)


def download_data(url):
    """Downloads the data"""
    response = requests.get(url)
    return response.text


def process_data(file_content):
    user_data = {}
    row = file_content.split("\n")

    # Compensates for the 0th index holding the column titles
    # and for the last index being an empty string when pulled in
    # and for the destructuring not having enough values
    line_num = 0
    for line in row[1:-1]:
        try:
            id, name, birthday = line.split(",")
            line_num += 1
            birthday_conversion = datetime.strptime(birthday, "%d/%m/%Y")
            user_data[id] = (name, birthday_conversion)
        except ValueError:
            message = f"Error processing line #{line_num} for ID #{id}"
            logger_creator("assignment2", "errors.log", message)
            continue

    return user_data


def display_person(id, personData):
    id = str(id)

    try:
        name = personData[id][0]
        birthday = personData[id][1].strftime("%Y-%m-%d")

        if personData[id]:
            print(f"Person #{id} is {name} with a birthday of {birthday}")
    except KeyError:
        print(f"No user found for id # {id}")


def main(url):
    print(f"Running main with URL = {url}...")
    csv_data = download_data(args.url)
    person_data = process_data(csv_data)

    while True:
        user_input = input("ID of person you are looking for : ")

        if user_input <= "0":
            print("Exiting program")
            break
        else:
            display_person(user_input, person_data)


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url", help="URL to the datafile", type=str, required=True
    )
    args = parser.parse_args()
    main(args.url)
