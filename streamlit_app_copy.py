# streamlit_app.py
import streamlit as st
import json
import pandas as pd

# Streamlit 페이지 설정
st.set_page_config(page_title="Real Estate Listings Viewer", layout="wide")
st.title("Real Estate Listings for Multiple Districts")
st.markdown("This page fetches and displays real estate listings for multiple districts using the Naver Real Estate API.")

# Load complex details from the JSON file
with open('complex_details_by_district.json', 'r', encoding='utf-8') as file:
    complex_details_by_district = json.load(file)

# Function to display details for a selected district
def display_district_details(district_name):
    district_data = complex_details_by_district.get(district_name, [])
    if district_data:
        df = pd.DataFrame(district_data)

        # 선택한 구의 데이터를 DataFrame으로 변환하여 표시
        df_display = df[["articleNo", "articleName", "realEstateTypeName", "tradeTypeName", "floorInfo",
                        "dealOrWarrantPrc", "areaName", "direction", "articleConfirmYmd", "articleFeatureDesc",
                        "tagList", "buildingName", "sameAddrMaxPrc", "sameAddrMinPrc", "realtorName", "sameAddrCnt"]]
        
        # DataFrame을 Streamlit에 표시
        st.write(f"### Real Estate Listings for {district_name}")
        st.dataframe(df_display)
    else:
        st.write(f"No data available for {district_name}.")

# Select box for choosing a district
district_names = list(complex_details_by_district.keys())
selected_district = st.selectbox("Select a district:", district_names)

# Display details for the selected district
if selected_district:
    display_district_details(selected_district)
else:
    st.write("Please select a district to view the listings.")