import requests
import json
import multiprocessing
import time

def getJsonHomesByPage(page):
  url = 'https://api.qasa.se/graphql'
  offset = page * 50
  query = """
    query HomeSearchQuery($offset: Int, $limit: Int, $platform: PlatformEnum, $order: HomeSearchOrderEnum, $orderBy: HomeSearchOrderByEnum, $searchParams: HomeSearchParamsInput!) {
      homeSearch(
        platform: $platform
        searchParams: $searchParams
        order: $order
        orderBy: $orderBy
      ) {
        filterHomesOffset(offset: $offset, limit: $limit) {
          pagesCount
          totalCount
          hasNextPage
          hasPreviousPage
          nodes {
            id
            firsthand
            rent
            tenantBaseFee
            title
            minimumPricePerNight
            maximumPricePerNight
            averagePricePerNight
            favoriteMarkedByUser
            landlord {
              uid
              companyName
              premium
              professional
              profilePicture {
                url
                __typename
              }
              proPilot
              __typename
            }
            user {
              uid
              proAgent
              __typename
            }
            location {
              id
              latitude
              longitude
              route
              locality
              sublocality
              streetNumber
              __typename
            }
            links {
              locale
              url
              __typename
            }
            description
            roomCount
            traits {
              type
              __typename
            }
            qasaGuaranteeCost
            seniorHome
            shared
            squareMeters
            studentHome
            type
            duration {
              createdAt
              endOptimal
              endUfn
              id
              startAsap
              startOptimal
              updatedAt
              __typename
            }
            corporateHome
            uploads {
              id
              url
              type
              title
              metadata {
                primary
                order
                __typename
              }
              __typename
            }
            numberOfHomes
            minRent
            maxRent
            minRoomCount
            maxRoomCount
            minSquareMeters
            maxSquareMeters
            rentalType
            tenantCount
            bedCount
            bedroomCount
            __typename
          }
          __typename
        }
        __typename
      }
    }
  """
  variables = f"""
      {{
    "limit": 50,
    "platform": "blocket",
    "searchParams": {{
      "areaIdentifier": [],
      "rentalType": [
        "long_term"
      ]
    }},
    "offset": {offset},
    "order": "DESCENDING",
    "orderBy": "PUBLISHED_AT"
    }}
  """
  response = requests.post(url=url, json={"variables": variables, "query": query})
  response_status_code = response.status_code
  while response_status_code != 200:
    print('response.status_code:', response_status_code, 'requests try again!')
    print('response.status_code:', response_status_code, 'requests try again!')
    response = requests.post(url=url, json={"variables": variables, "query": query})
  return response.json()

def getFormattedListOfHomesByPage(page):
  print("Page #", page + 1)
  homesData = getJsonHomesByPage(page)['data']
  formattedListOfHomes = []
  i = 1
  for node in homesData['homeSearch']['filterHomesOffset']['nodes']:
    home = {      
      "external_link": f"https://bostad.blocket.se/p2/sv/home/{node['id']}",
      "external_id": node['id'],
      "city": node['location']['locality'], 
      "address": node['location']['route'] + ' ' + node['location']['streetNumber'] + ', ' +node['location']['locality'],
      "title": node['title'],
      "latitude": node['location']['latitude'],
      "longitude": node['location']['longitude'],
      "description": node['description'],
      "property_type": node['type'],
      "room_count": node['roomCount'],
      "square_meters": node['squareMeters'],
      "available_date": str(node['duration']['startOptimal']).split('T')[0],
      "rent": node['rent'],
      "agency_fee": node['tenantBaseFee'],
      "deposit": node['qasaGuaranteeCost']
    }
    for trait in node['traits']:
      home[f"{trait['type']}"] = True
    home["images"] = [image['url'] for image in node['uploads']]
    home["position"] = page * 50 + i
    formattedListOfHomes.append(home)
    i += 1
  return formattedListOfHomes

if __name__ == '__main__':
  start_time = time.time()

  final_list_of_homes = []

  pagesCount = getJsonHomesByPage(0)['data']['homeSearch']['filterHomesOffset']['pagesCount']
  print("pagesCount = ", pagesCount)

  # Multiprocessing (faster)
  processing_pool = multiprocessing.Pool() 
  list_of_home_lists = processing_pool.map(getFormattedListOfHomesByPage, range(0, pagesCount))

  # Сonsequentially (slower, for debug)
  # list_of_home_lists = []
  # for i in range(0, pagesCount):
  #   list_of_home_lists.append(getFormattedListOfHomesByPage(i))

  for home_list in list_of_home_lists:
    for home in home_list:
      final_list_of_homes.append(home)

  with open('data.json', 'w', encoding='utf8') as json_file:
    json.dump(final_list_of_homes, json_file, indent=2, ensure_ascii=False)

  print("--- %s seconds ---" % (time.time() - start_time))
