import requests
import json

positions = [0]
list = []

def request_from_showcase(page):
  url = 'https://api.qasa.se/graphql'
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
      homeTemplates {
        id
        apartmentNumber
        squareMeters
        roomCount
        floor
        rent
        homeLayoutPictures {
          url
          __typename
        }
        description
        traits {
          type
          __typename
        }
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
  
  if page != '':
    offset = page * 50
  else:
    offset = 0
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
}}"""

  response = requests.post(url=url, json={"variables": variables, "query": query})
  return response.json()

pagaCount = request_from_showcase('')['data']['homeSearch']['filterHomesOffset']['pagesCount']

def under_showcase(page):
  under_showcase = request_from_showcase(page)['data']['homeSearch']['filterHomesOffset']

  dic_advertisement = {}

  for node in under_showcase['nodes']:

    dic_advertisement = {      
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
    
    for trait in node['homeTemplates'][0]['traits']:
      dic_advertisement[f"{trait['type']}"] = True

    dic_advertisement["images"] = [image['url'] for image in node['uploads']]
    
    positions[0] += 1
    dic_advertisement["position"] = positions[0]

    list.append(dic_advertisement)

  

for page in range(0, pagaCount):
  print(page)

  under_showcase(page)



with open('data.json', 'w', encoding='utf8') as json_file:
    json.dump(list, json_file, indent=2, ensure_ascii=False)