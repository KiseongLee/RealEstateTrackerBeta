# collect_complex_details.py
import requests
import json
import pprint
from config import cookies, headers  # config.py에서 쿠키와 헤더 가져오기

# Load marker IDs from the JSON file
with open('all_marker_ids.json', 'r', encoding='utf-8') as file:
    all_markers_data = json.load(file)

def fetch_complex_details(complex_no, page):
    detail_url = f'https://new.land.naver.com/api/articles/complex/{complex_no}?realEstateType=APT%3AABYG%3AJGC%3APRE&tradeType=&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears=&recentlyBuildYears=&minHouseHoldCount=&maxHouseHoldCount=&showArticle=false&sameAddressGroup=true&minMaintenanceCost=&maxMaintenanceCost=&priceType=RETAIL&directions=&page={page}&complexNo={complex_no}&buildingNos=&areaNos=&type=list&order=prc'
    
    response = requests.get(detail_url, cookies=cookies, headers=headers)
    if response.status_code == 200:
        return response.json().get("articleList", [])
    else:
        return []
    
def group_data_by_district(complex_details_by_area):
    grouped_data = {}
    for area_name, details_list in complex_details_by_area.items():
        district_name = area_name.split()[0]  # 구 이름을 추출합니다
        pprint.pprint(district_name)
        if district_name not in grouped_data:
            grouped_data[district_name] = []
        grouped_data[district_name].extend(details_list)
    return grouped_data

if __name__ == "__main__":
    complex_details_by_area = {}

    # Iterate over each area and fetch complex details by pages
    for area_name, marker_ids in all_markers_data.items():
        area_complex_details = []

        for complex_no in marker_ids:
            for page in range(1, 234):  # Assume a reasonable maximum number of pages
                details = fetch_complex_details(complex_no, page)
                if details:
                    area_complex_details.extend(details)
                    print(f"Successfully retrieved data for complex {complex_no}, area {area_name}, page {page}. Number of articles: {len(details)}")
                else:
                    print(f"No more articles for complex {complex_no} at page {page}.")
                    break  # No more data on subsequent pages

        complex_details_by_area[area_name] = area_complex_details
        print(f"Details collected for area: {area_name}")
        
    # Group data by district
    complex_details_by_district = group_data_by_district(complex_details_by_area)
    
    # Save complex details to a JSON file
    with open('complex_details_by_district.json', 'w', encoding='utf-8') as file:
        json.dump(complex_details_by_district, file, ensure_ascii=False, indent=4)

    print("Complex details have been grouped by district and saved to complex_details_by_district.json")