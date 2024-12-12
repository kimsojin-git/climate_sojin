import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정 (제목 변경)
st.set_page_config(page_title="세계여행의 기초, 기후 알아보기 🌍✈️", layout="wide")

# CSV 파일 경로
climate_csv = "climate.csv"
monthly_csv = "monthly.csv"

# 데이터 로드 함수
@st.cache_data
def load_data():
    return pd.read_csv(climate_csv)

@st.cache_data
def load_monthly_data():
    return pd.read_csv(monthly_csv)

df = load_data()
monthly_df = load_monthly_data()

# 쾨펜 기후 구분에 따른 색깔 지정
climate_colors = {
    "Tropical": "red",
    "Dry": "yellow",
    "Temperate": "green",
    "Cold": "skyblue",
    "Polar": "blue",
    "Highland": "gray",
}

# Streamlit 제목
st.title("세계여행의 기초, 기후 알아보기 🌍✈️")
st.write("세계의 다양한 기후 환경을 살펴보고, 데이터를 통해 비교해보세요!")

# 지도 시각화: 수도 위치를 쾨펜 기후 구분에 따라 색상 적용
st.subheader("세계 지도 속에서 찾아봐요 🌎")
fig_map = px.scatter_geo(
    df,
    locations="Country",
    locationmode="country names",
    hover_name="Capital",
    color="Climate in Capital",
    color_discrete_map=climate_colors,
    title="국가별 수도 위치 및 기후 분류",
)
fig_map.update_traces(marker=dict(size=10))
st.plotly_chart(fig_map, use_container_width=True)
