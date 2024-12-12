import streamlit as st
import pandas as pd
import plotly.express as px

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

# 국가 선택
selected_countries = st.multiselect(
    "비교할 국가를 선택하세요:", df["Country"].unique(), default=["South Korea"]
)
st.subheader(f"선택된 국가의 2023년 월별 기후 데이터")

# 선택된 국가의 데이터 필터링
country_data = monthly_df[monthly_df["Country"].isin(selected_countries)]

if country_data.empty:
    st.write("선택한 국가에 대한 데이터가 없습니다.")
else:
    # x축에 "국가-월" 형식 추가
    country_data["Country-Month"] = country_data["Country"] + " - " + country_data["Month"]

    # 기온 비교 그래프
    fig_temp = px.line(
        country_data,
        x="Month",
        y="Temperature (°C)",
        color="Country",  # 나라별로 색상을 다르게 설정
        title="선택된 국가들의 월별 평균 기온 비교",
        labels={"Temperature (°C)": "평균 기온 (°C)", "Country": "국가"},
        markers=True,
    )
    fig_temp.update_yaxes(range=[-50, 50])  # Y축 고정 (-50°C ~ 50°C)
    st.plotly_chart(fig_temp)

    # 강수량 비교 그래프 (막대를 더 얇게 설정하고, 옆으로 배치)
    fig_precip = px.bar(
        country_data,
        x="Country-Month",  # x축을 "국가-월" 형식으로 설정
        y="Precipitation (mm)",
        color="Country",  # 나라별로 색상을 다르게 설정
        title="선택된 국가들의 월별 강수량 비교",
        labels={"Precipitation (mm)": "강수량 (mm)", "Country-Month": "국가-월"},
        barmode="group",  # 막대 그래프를 옆으로 배치
    )
    fig_precip.update_yaxes(range=[0, 600])  # Y축 고정 (0mm ~ 600mm)
    fig_precip.update_traces(width=0.1)  # 막대 두께 절반으로 조정
    st.plotly_chart(fig_precip)

