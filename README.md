[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=Python+scraper+rental+property)](https://github.com/Romuch1not1first)
## About
This is a Python script that scrapes data from a website using GraphQL and multiprocessing, and saves the results to a JSON file.

The script first defines a function getJsonHomesByPage(page) that takes a page number as input and returns a JSON object containing data about homes listed on the website. The function sends a POST request to the website's GraphQL endpoint with a query that specifies the search criteria and the fields to be returned. The function uses the requests library to send the request, and retries the request if the status code is not 200 (OK).

The script also defines a function getFormattedListOfHomesByPage(page) that takes a page number as input, calls getJsonHomesByPage(page) to get the data, and processes the data to create a list of dictionaries, where each dictionary represents a home listing and contains information about the property such as the external link, external ID, address, latitude, longitude, description, property type, room count, square meters, available date, rent, agency fee, deposit, and images.

The script then uses multiprocessing to call getFormattedListOfHomesByPage(page) for each page of the search results in parallel, and collects the lists of home dictionaries into a single list called final_list_of_homes.

Finally, the script saves the final_list_of_homes as a JSON file called data.json.

Note that this script is specific to a particular website and search criteria, and may need to be modified for other websites or search criteria.

## How to installation this project
To install and run this project, you can follow these steps:

1. Clone the project from the GitHub repository to your local machine:
bash

`git clone https://github.com/alexbrovkin/qasa-blocket-homes.git`

2. Install the required dependencies. You can use pip to install the dependencies from the requirements.txt file:

`pip install -r requirements.txt`

3. Run the script by running the following command:

`python main.py`

This will run the script and generate the data.json file containing the scraped data. You can customize the search parameters by editing the variables in the getJsonHomesByPage() function in the main.py file.

Note: This project requires Python 3.6 or later to be installed on your machine.
