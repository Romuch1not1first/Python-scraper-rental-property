# Python-scraper-rental-property
This is a Python script that scrapes data from a website using GraphQL and multiprocessing, and saves the results to a JSON file.

The script first defines a function getJsonHomesByPage(page) that takes a page number as input and returns a JSON object containing data about homes listed on the website. The function sends a POST request to the website's GraphQL endpoint with a query that specifies the search criteria and the fields to be returned. The function uses the requests library to send the request, and retries the request if the status code is not 200 (OK).

The script also defines a function getFormattedListOfHomesByPage(page) that takes a page number as input, calls getJsonHomesByPage(page) to get the data, and processes the data to create a list of dictionaries, where each dictionary represents a home listing and contains information about the property such as the external link, external ID, address, latitude, longitude, description, property type, room count, square meters, available date, rent, agency fee, deposit, and images.

The script then uses multiprocessing to call getFormattedListOfHomesByPage(page) for each page of the search results in parallel, and collects the lists of home dictionaries into a single list called final_list_of_homes.

Finally, the script saves the final_list_of_homes as a JSON file called data.json.

Note that this script is specific to a particular website and search criteria, and may need to be modified for other websites or search criteria.
