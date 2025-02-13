import requests
import json
import pprint
from config import cookies, headers  # config.py에서 쿠키와 헤더 가져오기


def calculate_bounds(vertices):
    lons = [point[1] for point in vertices]
    lats = [point[0] for point in vertices]
    leftLon = min(lons)
    rightLon = max(lons)
    bottomLat = min(lats)
    topLat = max(lats)
    return leftLon, rightLon, topLat, bottomLat

def fetch_marker_ids(cortars_info):
    cortarNo = cortars_info.get('cortarNo')
    cortarZoom = cortars_info.get('cortarZoom')
    cortarVertexLists = cortars_info.get('cortarVertexLists', [[]])

    # Calculate the bounds (leftLon, rightLon, topLat, bottomLat)
    if cortarVertexLists and cortarVertexLists[0]:
        leftLon, rightLon, topLat, bottomLat = calculate_bounds(cortarVertexLists[0])
    else:
        print(f"Invalid cortarVertexLists data for cortarNo: {cortarNo}")
        return None

    params = {
        'cortarNo': cortarNo,
        'zoom': cortarZoom,
        'priceType': 'RETAIL',
        'markerId': '',
        'markerType': '',
        'selectedComplexNo': '',
        'selectedComplexBuildingNo': '',
        'fakeComplexMarker': '',
        'realEstateType': 'APT',
        'tradeType': 'A1',
        'tag': '%3A%3A%3A%3A%3A%3A%3A%3A',
        'rentPriceMin': 0,
        'rentPriceMax': 900000000,
        'priceMin': 0,
        'priceMax': 900000000,
        'areaMin': 0,
        'areaMax': 900000000,
        'oldBuildYears': '',
        'recentlyBuildYears': '',
        'minHouseHoldCount': 300,
        'maxHouseHoldCount': '',
        'showArticle': 'false',
        'sameAddressGroup': 'false',
        'minMaintenanceCost': '',
        'maxMaintenanceCost': '',
        'directions': '',
        'leftLon': leftLon,
        'rightLon': rightLon,
        'topLat': topLat,
        'bottomLat': bottomLat,
        'isPresale': 'false'
    }

    response = requests.get(
        'https://new.land.naver.com/api/complexes/single-markers/2.0',
        params=params,
        cookies=cookies,
        headers=headers
    )

    print(f"Fetching marker IDs for cortarNo: {cortarNo} - HTTP status code: {response.status_code}")

    if response.status_code == 200:
        try:
            response_data = response.json()
            pprint.pprint(response_data)  # 응답 데이터 전체를 출력하여 구조 확인

            # markerId 값 추출
            marker_ids = [item.get('markerId') for item in response_data if 'markerId' in item]

            if marker_ids:
                return marker_ids
            else:
                print(f"No marker IDs found in the response for cortarNo: {cortarNo}.")
                return None
        except json.JSONDecodeError:
            print(f"Failed to parse JSON response for cortarNo: {cortarNo}.")
            return None
    else:
        print(f"Failed to fetch marker IDs for cortarNo: {cortarNo}. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    with open('all_cortars.json', 'r', encoding='utf-8') as file:
        cortars_data = json.load(file)

    all_marker_ids = {}

    for cortar_name, cortars_info in cortars_data.items():
        cortar_no = cortars_info.get('cortarNo')
        if cortar_no:
            marker_ids = fetch_marker_ids(cortars_info)
            if marker_ids:
                all_marker_ids[cortar_name] = marker_ids
                print(f"Marker IDs for cortarNo {cortar_no} ({cortar_name}): {marker_ids}")
            else:
                print(f"No marker IDs found for cortarNo {cortar_no} ({cortar_name})")
        else:
            print(f"No cortarNo found for {cortar_name}")

    if all_marker_ids:
        with open('all_marker_ids.json', 'w', encoding='utf-8') as file:
            json.dump(all_marker_ids, file, ensure_ascii=False, indent=4)
        print("All marker IDs have been collected and saved to all_marker_ids.json")
    else:
        print("No marker IDs were collected.")