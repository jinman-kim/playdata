import requests
import re
import pandas as pd
from bs4 import BeautifulSoup as BS

cu_url = "https://cu.bgfretail.com/store/list_Ajax.do"
payload = {"pageIndex" : "1",
"listType" : "",
"jumpoCode" : "",
"jumpoLotto" : "",
"jumpoToto" : "",
"jumpoCash" : "",
"jumpoHour" : "",
"jumpoCafe" : "",
"jumpoDelivery" : "",
"jumpoBakery" : "",
"jumpoFry" : "",
"jumpoMultiDevice" : "",
"jumpoPosCash" : "",
"jumpoBattery" : "",
"jumpoAdderss" : "",
"jumpoSido" : "경기도",
"jumpoGugun" : "가평군",
"jumpodong" : "가평읍",
"user_id" : "",
"jumpoName" : "",}

r = requests.post(cu_url, data=payload)
bs = BS(r.text)
tmp = bs.find('div', class_='detail_store').findAll('tr')[1]
p = re.compile('sevice[0-9]{2} on')
p2 = re.compile('_([0-9a-zA-Z]+)\.png')

# 제공하는 서비스 확인 (영업시간, 배송 ,커피 등등)
# service = []
# for x in tmp.findAll('li',p):
#     service.append(p2.findall(str(x))[0])
# print(service)

store = pd.read_html(r.text)[0]

# # dataframe 에 series 추가
# store['a'] = [1,2,3,4,5]
# print(store)
# # Series 제거 , axis (축) 명시 필요
# store.drop('a', axis=1,inplace=True)
# print(store)

service_t = []
for y in bs.find('div', class_='detail_store').findAll('tr')[1:]:
    service_t.append([p2.findall(str(x))[0] for x in y.findAll('li',p)])

# 서비스 column 추가
store['서비스'] = service_t

phone = re.compile('[0-9]{2,3}-[0-9]{3,4}-[0,9]{3,4}')
store['연락처'] = store['매장명 / 연락처'].apply(lambda x : phone.findall(x)[0] if len(phone.findall(x)) > 0 else None)

store_p = re.compile("[가-힣]+점")
store['매장명'] = store['매장명 / 연락처'].apply(lambda x : store_p.findall(x)[0])

store.drop('매장명 / 연락처', axis=1, inplace=True)
store.rename(columns={'주소 / 매장 유형 및 서비스' : '주소'}, inplace=True)
# print(store.columns)

city = "https://cu.bgfretail.com/store/GugunList.do"
city_pay = {"pageIndex" : "1",
"listType" : "",
"jumpoCode" : "",
"jumpoLotto" : "",
"jumpoToto" : "",
"jumpoCash" : "",
"jumpoHour" : "",
"jumpoCafe" : "",
"jumpoDelivery" : "",
"jumpoBakery" : "",
"jumpoFry" : "",
"jumpoMultiDevice" : "",
"jumpoPosCash" : "",
"jumpoBattery" : "",
"jumpoAdderss" : "",
"jumpodong" : "",
"user_id" : "",
"sido" : "서울특별시",
"Gugun" : "",
"jumpoName" : "",}
dong = "https://cu.bgfretail.com/store/DongList.do"
dong_pay = {"pageIndex": "1",
"listType": "",
"jumpoCode": "",
"jumpoLotto": "",
"jumpoToto": "",
"jumpoCash": "",
"jumpoHour": "",
"jumpoCafe": "",
"jumpoDelivery": "",
"jumpoBakery": "",
"jumpoFry": "",
"jumpoMultiDevice": "",
"jumpoPosCash": "",
"jumpoBattery": "",
"jumpoAdderss": "",
"jumpoSido": "경기도",
"jumpoGugun": "가평군",
"jumpodong": "",
"user_id": "",
"sido": "경기도",
"Gugun": "가평군",
"jumpoName": "",}
gugun = [x['CODE_NAME'] for x in requests.post(city, city_pay).json()['GugunList']]

cu_url = "https://cu.bgfretail.com/store/list.do?category=store"
city = [x.text for x in BS(requests.get(cu_url).text,features='lxml').find("div", class_="search_wrap")\
    .findAll("option")][1:-2]
df = pd.read_pickle('./5store.pkl')

# row 이름 다 볼 수 있게
pd.set_option('display.max_rows',None)
a = df['address'].apply(lambda x : x.split()[0]).value_counts()
gy = df[df['address'].str.find('서울') ==0]['address'].apply(lambda x : x.split()[0]).value_counts()
df = df[~df[['brand', 'shopName']].duplicated()].copy()
df['address'] = df['address'].apply(lambda x : x.strip())

# 도시 -> 시 맵핑
# print(city)
df.loc[df['address'].str.find('경기') == 0, '시'] = '경기도'
df.loc[df['address'].str.find('서울') == 0, '시'] = '서울특별시'
df.loc[(df['address'].str.find('경남') == 0) |(df['address'].str.find('경상남도') == 0 ) , '시'] = ' 경상남도'
df.loc[(df['address'].str.find("부산") == 0), '시'] = '부산광역시'
df.loc[(df['address'].str.find("대전") == 0), '시'] = '대전광역시'
df.loc[(df['address'].str.find("광주") == 0), '시'] = '광주광역시'
df.loc[(df['address'].str.find("대구") == 0), '시'] = '대구광역시'
df.loc[(df['address'].str.find("울산") == 0), '시'] = '울산광역시'
df.loc[(df['address'].str.find("인천") == 0), '시'] = '인천광역시'
df.loc[(df['address'].str.find("강원") == 0), '시'] = '강원도'
df.loc[(df['address'].str.find("세종") == 0), '시'] = '세종특별자치시'
df.loc[(df['address'].str.find("제주") == 0), '시'] = '제주특별자치도'
df.loc[(df['address'].str.find("경북") == 0) |
        (df['address'].str.find("경상북도") == 0), '시'] = '경상북도'
df.loc[(df['address'].str.find("전북") == 0) |
        (df['address'].str.find("전라북도") == 0), '시'] = '전라북도'
df.loc[(df['address'].str.find("전남") == 0) |
        (df['address'].str.find("전라남도") == 0), '시'] = '전라남도'
df.loc[(df['address'].str.find("충북") == 0) |
        (df['address'].str.find("충청북도") == 0), '시'] = '충청북도'
df.loc[(df['address'].str.find("충남") == 0) |
        (df['address'].str.find("충청남도") == 0), '시'] = '충청남도'
df.loc[(df['address'].str.find("경남") == 0) |
        (df['address'].str.find("경상남도") == 0), '시'] = '경상남도'
# print(df[~df['shopName'].duplicated()].shape)

a = df['시'].value_counts().sum()

#inplace -> 대체하겠다: 별도의 copy 생성 없이 테이블 대체
#reset_index-> concat 하여 합성한 row들의 index를 0~n개 까지 초기화해줌
df.reset_index(drop=True,inplace=True)

# 주소 형식 예외처리
# print(df[df['시'].isnull()])
df.loc[24549, "address"] = "서울시 서대문구 충정로7 구세군빌딩1층"
df.loc[24549, '시'] = '서울특별시'
df.loc[(df['address'].str.find("창원") == 0), '시'] = '경상남도'
df.loc[30712, '시'] = '경기도'
df.loc[33001, '시'] = '부산광역시'
df.loc[33723, '시'] = '충청남도'
df.loc[33985, '시'] = '충청남도'
rate_region = df['시'].value_counts(normalize=True)

# print(rate_region)

stat_url = "https://jumin.mois.go.kr/ageStatMonth.do"
pay = {"tableChart": "T",
        "sltOrgType": "1",
        "sltOrgLvl1": "A",
        "sltOrgLvl2": "A",
        "sltUndefType": "",
        "nowYear": "2023",
        "searchYearMonth": "year",
        "searchYearStart": "2022",
        "searchMonthStart": "12",
        "searchYearEnd": "2022",
        "searchMonthEnd": "12",
        "sum": "sum",
        "gender": "gender",
        "sltOrderType": "1",
        "sltOrderValue": "ASC",
        "sltArgTypes": "10",
        "sltArgTypeA": "0",
        "sltArgTypeB": "100",}
r = requests.post(stat_url, data=pay)
# 3 paragraph  , index=0,1,2 , index=2 is population info
korea = pd.read_html(r.text)[2]
# 3 element in korea.columns , ( a, b, c) , 'a'  is YYYYMMDD
korea.columns = [x[0] for x in korea.columns]

# '시'로 indexing , 번호는 1번부터 시작하며 , 0번:시 , 1번:인구수로 데이터프레임 생성
population = korea.iloc[1:,[0,1]]

# '시' 별 편의점 데이터프레임 생성
convenience = pd.DataFrame(df['시'].value_counts())
print(convenience)
# population의 인덱스를 행정기관 (ex: 서울특별시 , 부산광역시 ,경기도) 로 인덱싱
population.set_index('행정기관', inplace=True)

# left join, '시'를 기준으로 left join ,  인구수 대비 편의점의 비율 구하기 전 작업
# pcr = People Convenience Rate (인구대비 편의점 비율)
pcr = pd.merge(population,convenience,left_index=True, right_index=True,how='left')

# Column명 설정
pcr.columns = ['인구수','편의점수']
pcr['비율'] =  round(pcr['인구수'] / pcr['편의점수'],1)
pcr.sort_values(by=['비율'], ascending=False)
seoul = df.query("시 == '서울특별시'").copy()
seoul['구'] = seoul['address'].apply(lambda x : x.split()[1])
seoul.loc[seoul['구'] == '상가002A동B09호', '구'] = '송파구'
seoul.loc[seoul['구'] == '서울시립대로', '구'] = '동대문구'
seoul_2 = seoul.groupby(['구', 'brand'], as_index=False)[['shopName']].count()
seoul_2.sort_values(by=['shopName'], ascending=False).groupby(['구']).nth(-1)
df.to_pickle('./convenience.pkl')