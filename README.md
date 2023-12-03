# 빅데이터처리 프로젝트

<br>

## 주제

### 기상개황과 모기 발생 지표의 관계 분석

<br>

# 데이터 수집

## 사용할 데이터

- #### 서울특별시 기상개황 통계 <a href="https://data.seoul.go.kr/dataList/414/S/2/datasetView.do">(Link)</a>
  - 기상청에서 제공하는 서울시 기상개황을 제공하는 일반ㆍ보고통계
- #### 서울특별시 모기예보제 정보 <a href="https://data.seoul.go.kr/dataList/OA-13285/S/1/datasetView.do">(Link)</a>
  - 모기발생 상황을 지수화하여 모기발생 단계별 시민행동요령을 알려주는 일일 모기발생 예보서비스

<br>

## 데이터 수집 방법

- #### 서울 열린데이터 광장 <a href="https://data.seoul.go.kr/">(Link)</a> 에서 CSV 파일로 다운로드

<br>

## 분석할 내용

- #### 기상개황 데이터와 모기지수 데이터를 활용하여 다음의 결과를 확인할 수 있습니다.
  ##### 1. 기상 변수와 모기 지수 간의 상관관계
  ##### 2. 계절별 수변부, 주거지, 공원의 모기 지수의 변화
  ##### 3. 월별 모기 지수의 변화
  ##### 4. 평균기온에 따른 모기 지수의 변화
  ##### 5. 강수량에 따른 모기 지수의 변화
  ##### 6. 평균습도에 따른 모기 지수의 변화

<br>

## 파일 목록

- `seoul_temp.csv` : 서울특별시 기상개황 통계
- `mosquito_occu.csv` : 서울특별시 모기예보제 정보
- `mosquito_incidence_index.ipynb` : 관계 분석 코드 (Colab)
- `mosquito_incidence_index.py` : 관계 분석 코드 (Python)

<br>

## 데이터 미리보기

### <div align="center">서울특별시 기상개황 통계 <a href="https://docs.google.com/spreadsheets/d/1ockVGMMUngqKGpQ1gtf4Eg43aoOU1FADBNWvxIHSk1I/edit?usp=sharing">&lt;구글 스프레드 시트&gt;</a></div>

<div align="center">
	<img src="https://github.com/dhwngjs01/3-2_Big_Data_Processing/assets/38345593/0598682d-d491-41f1-90ac-6ec4b8492a68"/>
</div>

### <div align="center">서울특별시 모기예보제 정보 <a href="https://docs.google.com/spreadsheets/d/1iTeiEdD4j0ms1VXecbB-GdFki1pj-YMoU8L6P_EdRaU/edit?usp=sharing">&lt;구글 스프레드 시트&gt;</a></div>

<div align="center">
	<img width="400" src="https://github.com/dhwngjs01/3-2_Big_Data_Processing/assets/38345593/edf9f58c-81ae-4d74-ba4c-49b5daa383bc"/>
</div>

<br>

# 코드 설명

- 해당 설명은 Colab 기준으로 설명합니다.

### 폰트 설치

```python
!sudo apt-get install -y fonts-nanum
!sudo fc-cache -fv
!rm ~/.cache/matplotlib -rf

import os
os.kill(os.getpid(), 9)
```

- 폰트를 따로 설치해야 나중에 그래프에서 한글이 안깨져서 보입니다. 꼭 설치하도록 합시다.

<br>

## 데이터 가공/정제

- #### 기상개황 데이터 전처리
  - 열에 대한 부연설명이 첫번째 행에 있었기 때문에 제외하고 나머지 행들로 재정의합니다.
  - `2021-02-01` 이전 데이터는 모기지수 데이터가 이상한 부분이 있어서 이전 날짜는 제외하고 선택합니다.
  - 결측치는 제거합니다.
  - `df_weather['최심신적설']` 열에 데이터가 없으면 `-` 라서 나중에 숫자로 형변환 해줘야하니 `0`으로 바꿔줍니다.
  - 모기지수 데이터에서 월별로 데이터를 병합할꺼라서 `df_weather['월']` 데이터도 추출해줍니다.

```python
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
```

<div align="center">
	<img src="https://github.com/dhwngjs01/3-2_Big_Data_Processing/assets/38345593/6be6a6af-429e-49ca-af49-68f2ae7ee2c1" />
</div>

<br>

- #### 모기지수 데이터 전처리
  - 기상개황 데이터에서 월별로 병합할꺼라서 `df_mosquito['월']` 데이터도 추출합니다.
  - `2021-02-01` 이전 데이터는 이상한 값들이 있어서 이전 날짜는 제외하고 선택합니다.
  - 결측치는 제거합니다.

```python
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
```

<div align="center">
	<img src="https://github.com/dhwngjs01/3-2_Big_Data_Processing/assets/38345593/99087cc8-90d3-4f91-adff-0c438065dc90" />
</div>

<br>
 
- #### 기상 개황 데이터와 모기 지수 데이터를 월(Month)의 시점을 기준으로 병합
	- 월(Month) 기준 평균데이터로 병합해줍니다.
	- 나중에 계절 데이터로 계절별 모기 지수도 구할꺼라서 ```merged_df['월']``` 기준으로 계절을 나눠줍니다.
	- 가독성을 위해 열 순서를 재정의합니다.
```python
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

````

<div align="center">
	<img src="https://github.com/dhwngjs01/3-2_Big_Data_Processing/assets/38345593/a20939f4-26df-40e8-9085-a0a66c3577c1" />
</div>



## 시각화
### 1. 전체 변수에 대한 상관관계 분석
- 기상개황과 모기지수의 전체 변수에 대한 상관관계 히트맵을 보기위해 작성한 코드입니다.
- 계절의 상관관계도 분석하기 위해서 계절 데이터를 원-핫 인코딩합니다.
```python
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
````

<div align="center">
	<img src="https://github.com/dhwngjs01/3-2_Big_Data_Processing/assets/38345593/78d90688-0134-4aa7-9156-3d774be31c2f" />
</div>

<br>

### 2. 기상 변수와 모기지수 간의 0.8 이상 상관관계 행렬

```python
# 0.8 이상의 상관관계를 가진 항목만 필터링
high_corr_matrix = correlation_matrix[correlation_matrix.abs() >= 0.8]

# 시각화
plt.figure(figsize=(15, 10))
sns.heatmap(high_corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('기상 변수와 모기 지수 간의 0.8 이상 상관관계 행렬')
plt.show()
```

<div align="center">
	<img src="https://github.com/dhwngjs01/3-2_Big_Data_Processing/assets/38345593/1a70abf9-1f43-41b7-852e-49c3f0115234" />
</div>

<br>

### 3. 계절별 모기 지수 평균 계산

```python
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
```

<div align="center">
	<img src="https://github.com/dhwngjs01/3-2_Big_Data_Processing/assets/38345593/feabfc9d-93b7-4283-b5d4-a69e88c98c85" />
</div>

<br>

### 4. 월별 모기 지수의 변화

```python
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
```

<div align="center">
	<img src="https://github.com/dhwngjs01/3-2_Big_Data_Processing/assets/38345593/a1bde45e-574e-4910-b4b7-dc57abcb4363" />
</div>

<br>

### 5. 평균기온에 따른 모기 지수의 변화

```python
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
```

<div align="center">
	<img src="https://github.com/dhwngjs01/3-2_Big_Data_Processing/assets/38345593/55bd5348-7063-469b-a651-f14a5bb7e529" />
</div>

<br>

### 6. 강수량에 따른 모기 지수의 변화

```python
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
```

<div align="center">
	<img src="https://github.com/dhwngjs01/3-2_Big_Data_Processing/assets/38345593/45d2f8d0-c3e8-4615-91b5-7996bf6aeb64" />
</div>

<br>

### 7. 평균습도에 따른 모기 지수의 변화

```python
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
```

<div align="center">
	<img src="https://github.com/dhwngjs01/3-2_Big_Data_Processing/assets/38345593/fae73aaf-9cec-4fa8-a987-eb8951b5d82d" />
</div>

<br>

## 결론

- #### 기상개황과 모기지수는 아래 항목들과 밀접한 관련이 있다.

1. 기온
2. 강수량
3. 습도
4. 기압
5. 이슬점온도
6. 운량
7. 적설량
8. 겨울
9. 기압

- #### 5월 중순부터 주거지보다 공원에 모기가 더 많아진다.
- #### 6월 ~ 9월까지는 강 근처에 가면 모기가 무조건 있다.
- #### 주거지는 7월에 모기가 가장 많이 발견된다.
- #### 계절별 모기는 여름 -> 가을 -> 봄 -> 겨울 순으로 많다.
- #### 기온이 섭씨 8도부터 모기 활동량이 급상승 한다.
