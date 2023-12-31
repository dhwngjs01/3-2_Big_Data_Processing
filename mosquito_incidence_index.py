# -*- coding: utf-8 -*-
"""Mosquito Incidence Index

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mhms2Ub5hSblrEelkALrAQI3eYJySFov

# 기상개황과 모기 발생 지표의 관계 분석

## 기상개황 데이터와 모기지수 데이터를 활용하여 다음의 결과를 확인할 수 있습니다.
### 1. 기상 변수와 모기 지수 간의 상관관계
### 2. 계절별 수변부, 주거지, 공원의 모기 지수의 변화
### 3. 월별 모기 지수의 변화
### 4. 평균기온에 따른 모기 지수의 변화
### 5. 강수량에 따른 모기 지수의 변화
### 6. 평균습도에 따른 모기 지수의 변화

### 폰트 설치

첫 실행시 아래 코드 주석 제거후 진행  
폰트 설치되면 다시 주석 처리 후 Ctrl+F9 로 모두 실행
"""

# !sudo apt-get install -y fonts-nanum
# !sudo fc-cache -fv
# !rm ~/.cache/matplotlib -rf

# import os
# os.kill(os.getpid(), 9)

"""### 0. 폰트 설정 및 라이브러리 불러오기

### 1. 데이터 수집

#### 1.1 매번 데이터 파일 업로드하기 번거로우니 구글 드라이브 마운트하기
"""

from google.colab import drive
drive.mount('/content/drive')

"""#### 1.2 폰트설정 및 패키지 불러오기"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

plt.rc('font', family='NanumBarunGothic')
plt.rc('axes', unicode_minus=False)

"""#### 1.3 데이터 불러오기"""

# 경로 지정
# path = '/content/'
path = '/content/drive/MyDrive/Colab Notebooks/빅데이터처리/Project/data/'

# 서울시 기상개황 정보
raw_weather = pd.read_csv(path + 'seoul_temp.csv')

# 서울시 모기예보제 정보
raw_mosquito = pd.read_csv(path + 'mosquito_occu.csv', encoding='cp949')

# 복사본 만들기
df_weather = raw_weather.copy()
df_mosquito = raw_mosquito.copy()

"""#### 1.4 데이터 보기

##### 1.4.1 기상개황 데이터 보기
"""

# 기상개황
df_weather.head()

df_weather.shape

df_weather.info()

df_weather.describe()

"""##### 1.4.2 모기예보제 데이터 보기"""

# 모기예보제
df_mosquito

df_mosquito.shape

df_mosquito.info()

df_mosquito.describe()

"""#### 1.5 열 이름 변경"""

# 기상개황 csv
df_weather.rename(columns = {
    '시점' : '시점',
    '기온 (℃)' : '평균기온',
    "기온 (℃).1" : "평균최고기온",
    "기온 (℃).2" : "극점최고기온",
    "기온 (℃).3" : "평균최저기온",
    "기온 (℃).4" : "극점최저기온",
    "강수량 (mm)" : "강수량",
    "상대습도 (%)" : "평균상대습도",
    "상대습도 (%).1" : "최소상대습도",
    "평균해면기압 (hpa)" : "평균해면기압",
    "이슬점온도 (℃)" : "이슬점온도",
    "평균운량 (10%)" : "평균운량",
    "일조시간 (hr)" : "일조시간",
    "최심신적설 (㎝)" : "최심신적설",
    "바람 (m/s)" : "평균풍속",
    "바람 (m/s).1" : "최대풍속",
    "바람 (m/s).2" : "최대순간풍속"
  }, inplace = True)

# 모기예보제 csv
df_mosquito.rename(columns = {
    '모기지수 발생일' : '시점',
    '모기지수(수변부)' : '수변부',
    '모기지수(주거지)' : '주거지',
    '모기지수(공원)' : '공원',
  }, inplace = True)

df_mosquito.head()

"""### 2. 데이터 가공

#### 2.1 데이터 전처리

##### 2.1.1 기상 데이터
"""

# 기상개황 데이터 전처리

# 첫 번째 행을 제외한 나머지 행 선택
df_weather = df_weather.iloc[1:]

# 날짜로 형변환
df_weather['시점'] = pd.to_datetime(df_weather['시점'])

# 2021년 2월 1일 이후의 데이터만 선택
start_date = '2021-02-01'
df_weather = df_weather[df_weather['시점'] >= start_date]

# 결측치 처리
df_weather = df_weather.dropna()

# 최심신적설 '-' 데이터 0으로 대체
df_weather['최심신적설'] = df_weather['최심신적설'].replace('-', 0)

# 기상 데이터들의 월(Month) 데이터 추출
df_weather['월'] = df_weather['시점'].dt.month

"""##### 2.1.2 기상 데이터 확인"""

df_weather.head()

"""##### 2.1.3 모기지수 데이터"""

# 모기 예보 데이터 전처리

# 날짜로 형변환
df_mosquito['시점'] = pd.to_datetime(df_mosquito['시점'])

# 모기지수 데이터들의 월(Month) 데이터 추출
df_mosquito['월'] = df_mosquito['시점'].dt.month

# 2021년 2월 1일 이후의 데이터만 선택
start_date = '2021-02-01'
df_mosquito = df_mosquito[df_mosquito['시점'] >= start_date]

# 결측치 처리
df_mosquito = df_mosquito.dropna()

# 기상개황 데이터 형변환
df_weather['시점'] = pd.to_datetime(df_weather['시점'])
df_weather['평균기온'] = df_weather['평균기온'].astype(float)
df_weather['평균최고기온'] = df_weather['평균최고기온'].astype(float)
df_weather['극점최고기온'] = df_weather['극점최고기온'].astype(float)
df_weather['평균최저기온'] = df_weather['평균최저기온'].astype(float)
df_weather['극점최저기온'] = df_weather['극점최저기온'].astype(float)
df_weather['강수량'] = df_weather['강수량'].astype(float)
df_weather['평균상대습도'] = df_weather['평균상대습도'].astype(float)
df_weather['최소상대습도'] = df_weather['최소상대습도'].astype(float)
df_weather['평균해면기압'] = df_weather['평균해면기압'].astype(float)
df_weather['이슬점온도'] = df_weather['이슬점온도'].astype(float)
df_weather['평균운량'] = df_weather['평균운량'].astype(float)
df_weather['일조시간'] = df_weather['일조시간'].astype(float)
df_weather['최심신적설'] = df_weather['최심신적설'].astype(float)
df_weather['평균풍속'] = df_weather['평균풍속'].astype(float)
df_weather['최대풍속'] = df_weather['최대풍속'].astype(float)
df_weather['최대순간풍속'] = df_weather['최대순간풍속'].astype(float)

# 모기예보제 데이터 형변환
df_mosquito['시점'] = pd.to_datetime(df_mosquito['시점'])
df_mosquito['수변부'] = df_mosquito['수변부'].astype(float)
df_mosquito['주거지'] = df_mosquito['주거지'].astype(float)
df_mosquito['공원'] = df_mosquito['공원'].astype(float)

"""##### 2.1.4 모기지수 데이터 확인"""

df_mosquito

"""##### 2.1.5 기상 데이터와 모기 지수 데이터를 월(Month)의 시점을 기준으로 병합"""

# 기상 데이터와 모기 지수 데이터를 월(Month)의 시점을 기준으로 병합
avg_weather_df = df_weather.groupby('월').mean(numeric_only=True).reset_index()
avg_mosquito_df = df_mosquito.groupby('월').mean(numeric_only=True).reset_index()

merged_df = pd.merge(avg_weather_df, avg_mosquito_df, on=['월'], how='inner')

# 계절 구분
def get_season(month):
    if 3 <= month < 6:
        return '봄'
    elif 6 <= month < 9:
        return '여름'
    elif 9 <= month < 12:
        return '가을'
    else:
        return '겨울'

# 계절 열 생성
merged_df['계절'] = merged_df['월'].apply(get_season)

# 열 순서 재정의
selected_columns = ['월', '계절', '수변부', '주거지', '공원', '평균기온', '평균최고기온', '극점최고기온', '평균최저기온',
                    '극점최저기온', '강수량', '평균상대습도', '최소상대습도', '평균해면기압', '이슬점온도', '평균운량',
                    '일조시간', '최심신적설', '평균풍속', '최대풍속', '최대순간풍속']

# 기상 데이터프레임 재정의
merged_df = merged_df[selected_columns]

"""##### 2.1.6 병합된 데이터 보기"""

merged_df.head()

"""### 3. 상관관계 분석

#### 3.1 기상 변수와 모기 지수 간의 상관관계 분석
"""

# 기상 변수와 모기 지수 간의 상관관계 분석
# 계절을 원-핫 인코딩
season_dummies = pd.get_dummies(merged_df['계절'])

# 기존 데이터프레임과 합치기
merged_df_onehot = pd.concat([merged_df, season_dummies], axis=1)

# 상관관계 행렬 계산
correlation_matrix = merged_df_onehot.corr(numeric_only=True)

# 시각화
plt.figure(figsize=(16, 11))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('기상 변수와 모기 지수 간의 상관관계 행렬')
plt.show()

"""#### 3.2 (0.8 이상의 상관관계를 가진 항목만 필터링)"""

# 0.8 이상의 상관관계를 가진 항목만 필터링
high_corr_matrix = correlation_matrix[correlation_matrix.abs() >= 0.8]

# 시각화
plt.figure(figsize=(15, 10))
sns.heatmap(high_corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('기상 변수와 모기 지수 간의 0.8 이상 상관관계 행렬')
plt.show()

"""### 4. 시각화

#### 4.1 계절별 모기 지수 평균 계산
"""

# 계절별 모기 지수 평균 계산
avg_mosquito_by_season = merged_df.groupby('계절').agg({'수변부': 'mean', '주거지': 'mean', '공원': 'mean'}).reset_index()

# 데이터 정리 (melt)
avg_mosquito_melted = pd.melt(avg_mosquito_by_season, id_vars='계절', var_name='지수종류', value_name='평균모기지수')


# RGB 색상 설정
colors = ['blue', 'red', 'green']

# 시각화
plt.figure(figsize=(12, 8))
ax = sns.barplot(x='계절', y='평균모기지수', hue='지수종류', data=avg_mosquito_melted, palette=colors)

# 상단에 평균 값 표시
for p in ax.patches:
  ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')

plt.title('계절별 수변부, 주거지, 공원 모기 지수 평균')
plt.xlabel('계절')
plt.ylabel('평균 모기 지수')
plt.legend(title='지수종류')
plt.show()

"""#### 4.2 월별 모기 지수의 변화"""

# 월별 모기 지수의 변화
monthly_mosquito = merged_df[['월', '수변부', '주거지', '공원']]

# 그래프 크기 설정
plt.figure(figsize=(10, 5))

# 선 그래프 (수변부)
plt.plot(monthly_mosquito.index, monthly_mosquito['수변부'], label='수변부', color='blue')

# 선 그래프 (주거지)
plt.plot(monthly_mosquito.index, monthly_mosquito['주거지'], label='주거지', color='red')

# 선 그래프 (공원)
plt.plot(monthly_mosquito.index, monthly_mosquito['공원'], label='공원', color='green')

# 축 및 레이블 설정
plt.title('월별 모기 지수의 변화 (선 그래프)')
plt.xlabel('월')
plt.ylabel('평균 모기 지수')

# X 축에 월 표시
plt.xticks(monthly_mosquito.index, labels=['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'])

# 범례 설정
plt.legend()

# 그리드 추가
plt.grid(True)

# 그래프 표시
plt.show()

"""#### 4.3 평균기온에 따른 모기 지수의 변화"""

# 평균기온에 따른 모기 지수의 변화
avg_temp_mosquito = merged_df[['평균기온', '수변부', '주거지', '공원']].sort_values(by='평균기온')

# 그래프 크기 설정
plt.figure(figsize=(10, 5))

# 선 그래프 (수변부)
plt.plot(avg_temp_mosquito['평균기온'], avg_temp_mosquito['수변부'], label='수변부', color='blue')

# 선 그래프 (주거지)
plt.plot(avg_temp_mosquito['평균기온'], avg_temp_mosquito['주거지'], label='주거지', color='red')

# 선 그래프 (공원)
plt.plot(avg_temp_mosquito['평균기온'], avg_temp_mosquito['공원'], label='공원', color='green')

# 축 및 레이블 설정
plt.title('평균기온에 따른 모기 지수의 변화 (선 그래프)')
plt.xlabel('평균기온 (℃)')
plt.ylabel('모기 지수')

# 범례 설정
plt.legend()

# 그리드 추가
plt.grid(True)

# 그래프 표시
plt.show()

"""#### 4.4 강수량에 따른 모기 지수의 변화"""

# 강수량에 따른 모기 지수의 변화
avg_rainfall_df = merged_df[['강수량', '수변부', '주거지', '공원']].sort_values(by='강수량')

# 그래프 크기 설정
plt.figure(figsize=(10, 5))

# 선 그래프 (수변부)
plt.plot(avg_rainfall_df['강수량'], avg_rainfall_df['수변부'], label='수변부', color='blue')

# 선 그래프 (주거지)
plt.plot(avg_rainfall_df['강수량'], avg_rainfall_df['주거지'], label='주거지', color='red')

# 선 그래프 (공원)
plt.plot(avg_rainfall_df['강수량'], avg_rainfall_df['공원'], label='공원', color='green')

# 축 및 레이블 설정
plt.title('강수량에 따른 모기 지수의 변화 (선 그래프)')
plt.xlabel('강수량 (mm)')
plt.ylabel('모기 지수')

# 범례 설정
plt.legend()

# 그리드 추가
plt.grid(True)

# 그래프 표시
plt.show()

"""#### 4.5 평균습도에 따른 모기 지수의 변화"""

# 평균습도에 따른 모기 지수의 변화
avg_humidity_df = merged_df[['평균상대습도', '수변부', '주거지', '공원']].sort_values(by='평균상대습도')

# 그래프 크기 설정
plt.figure(figsize=(10, 5))

# 선 그래프 (수변부)
plt.plot(avg_humidity_df['평균상대습도'], avg_humidity_df['수변부'], label='수변부', color='blue')

# 선 그래프 (주거지)
plt.plot(avg_humidity_df['평균상대습도'], avg_humidity_df['주거지'], label='주거지', color='red')

# 선 그래프 (공원)
plt.plot(avg_humidity_df['평균상대습도'], avg_humidity_df['공원'], label='공원', color='green')

# 축 및 레이블 설정
plt.title('평균습도에 따른 모기 지수의 변화 (선 그래프)')
plt.xlabel('평균상대습도 (%)')
plt.ylabel('모기 지수')

# 범례 설정
plt.legend()

# 그리드 추가
plt.grid(True)

# 그래프 표시
plt.show()