import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 경로
csv_file = "climate.csv"

# 데이터 로드 함수
@st.cache_data
def load_data():
    return pd.read_csv(csv_file)

df = load_data()

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
st.plotly_chart(fig_map)

# 선택한 국가와 추천된 국가들 간 비교
st.subheader("기준 국가와 추천 국가 간 비교")
st.write("초기에는 모든 나라가 표시되며, 추가로 비교할 국가를 선택할 수도 있습니다.")

# 초기 설정값으로 모든 나라 표시
compare_countries = st.multiselect(
    "비교할 국가를 선택하세요:", df["Country"].tolist(), default=df["Country"].tolist()
)

compare_data = df[df["Country"].isin(compare_countries)]

# 기온 비교 시각화
fig_temp_compare = px.bar(
    compare_data,
    x="Country",
    y="Average Temperature (°C)",
    color="Climate in Capital",
    color_discrete_map=climate_colors,
    title="여러 나라들의 평균 기온 비교",
    labels={"Average Temperature (°C)": "평균 기온 (°C)"},
)
st.plotly_chart(fig_temp_compare)

# 강수량 비교 시각화
fig_precip_compare = px.bar(
    compare_data,
    x="Country",
    y="Average Precipitation (mm)",
    color="Climate in Capital",
    color_discrete_map=climate_colors,
    title="여러 나라들의 평균 강수량 비교",
    labels={"Average Precipitation (mm)": "평균 강수량 (mm)"},
)
st.plotly_chart(fig_precip_compare)