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

# 사이드바: 기준 국가 선택
st.sidebar.header("국가 비교 도구")
selected_country = st.sidebar.selectbox("기준 국가를 선택하세요:", df["Country"])

# 기준 국가 데이터 추출
reference_data = df[df["Country"] == selected_country].iloc[0]

# 기후가 비슷한 국가 추천
df["Temperature Difference"] = abs(df["Average Temperature (°C)"] - reference_data["Average Temperature (°C)"])
df["Precipitation Difference"] = abs(df["Average Precipitation (mm)"] - reference_data["Average Precipitation (mm)"])
df["Total Difference"] = df["Temperature Difference"] + df["Precipitation Difference"]

similar_countries = df.sort_values("Total Difference").head(5)  # 가장 비슷한 5개 국가
different_countries = df.sort_values("Total Difference", ascending=False).head(5)  # 가장 다른 5개 국가

st.subheader(f"'{selected_country}'와 기후가 비슷한 국가 추천")
st.table(similar_countries[["Country", "Climate in Capital", "Average Temperature (°C)", "Average Precipitation (mm)"]])

st.subheader(f"'{selected_country}'와 기후가 다른 국가 추천")
st.table(different_countries[["Country", "Climate in Capital", "Average Temperature (°C)", "Average Precipitation (mm)"]])
