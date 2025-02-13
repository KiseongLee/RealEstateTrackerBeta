import requests
import json
import pprint
from config import cookies, headers  # config.py에서 쿠키와 헤더 가져오기
from params_list import params_list  # params_list.py에서 params_list 가져오기


def fetch_cortars(params):
    response = requests.get('https://new.land.naver.com/api/cortars', params=params, cookies=cookies, headers=headers)
    if response.status_code == 200:
        try:
            response_data = response.json()
            pprint.pprint(response_data)  # Debug: Print the entire response

            if 'cortarVertexLists' in response_data:
                cortars_info = {
                    "cortarVertexLists": response_data['cortarVertexLists'],
                    "cortarNo": response_data.get('cortarNo', ''),
                    "cortarName": response_data.get('cortarName', ''),
                    "cityName": response_data.get('cityName', ''),
                    "divisionName": response_data.get('divisionName', ''),
                    "sectorName": response_data.get('sectorName', ''),
                    "cityNo": response_data.get('cityNo', ''),
                    "divisionNo": response_data.get('divisionNo', ''),
                    "sectorNo": response_data.get('sectorNo', ''),
                    "cortarType": response_data.get('cortarType', ''),
                    "centerLat": response_data.get('centerLat', 0),
                    "centerLon": response_data.get('centerLon', 0),
                    "cortarZoom": response_data.get('cortarZoom', 0)
                }
                return cortars_info
            else:
                print("The expected key is not found in the response.")
                return None
        except json.JSONDecodeError:
            print("Failed to parse JSON response.")
            return None
    else:
        print(f"Failed to fetch cortars. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    all_cortars_info = {}

    for i, params in enumerate(params_list):
        cortars_info = fetch_cortars(params)
        if cortars_info:
            cortar_name = f"{cortars_info.get('divisionName', f'Unknown_{i}')} {cortars_info.get('cortarName', f'Unknown_{i}')}"
            all_cortars_info[cortar_name] = cortars_info
            print(f"Cortars for {cortar_name} have been collected and added to the dictionary.")
            pprint.pprint(cortars_info)  # Pretty-print the cortars for testing
        else:
            print(f"No cortars data collected for params set {i}.")

    if all_cortars_info:
        with open('all_cortars.json', 'w', encoding='utf-8') as file:
            json.dump(all_cortars_info, file, ensure_ascii=False, indent=4)
        print("All cortars have been collected and saved to all_cortars.json")
    else:
        print("No cortars data collected.")