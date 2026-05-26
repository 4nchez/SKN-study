import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

flights = sns.load_dataset('flights')
#  1949년부터 1960년까지 매달 국제 항공 승객 수를 기록한 데이터
print(flights.info())
'''
<class 'pandas.DataFrame'>
RangeIndex: 144 entries, 0 to 143
Data columns (total 3 columns):
 #   Column      Non-Null Count  Dtype   
---  ------      --------------  -----   
 0   year        144 non-null    int64   
 1   month       144 non-null    category
 2   passengers  144 non-null    int64   
dtypes: category(1), int64(2)
memory usage: 2.9 KB
None
'''
print(flights.head())

def test1():
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='year', y='passengers', data=flights)
                 
    plt.title('Number of Passengers Over Time')
    plt.xlabel('Year')
    plt.ylabel('Number of Passengers')
    plt.show( )

def test2():
    # print('test2 ---------------------')
    flights = sns.load_dataset('flights')
    # print(flights.head())
    # 'year'와 'month' 열을 문자열로 변환 후 결합
    flights['year'] = flights['year'].astype(str)
    flights['month'] = flights['month'].astype(str)
    # 새로운 'date' 열 생성
    flights['date'] = pd.to_datetime(flights['year'] + '-' + flights['month'])
    # date 순으로 정렬
    flights = flights.sort_values('date')

    plt.figure(figsize=(12, 6))
    sns.lineplot(x='date', y='passengers', data=flights)
    plt.title('Monthly Number of Passengers Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Passengers')
    plt.show( )

def test3():
    '''
    히트맵(Heatmap) : 데이터를 색상으로 표현해서 시각화한 그래프
    - 변수 간의 상관관계를 색으로 시각화함
    - 2차원 데이터를 나타내는 데 사용함
    '''
    flights = sns.load_dataset('flights')

    # 'year'와 'month'로 그룹화하여 'passengers' 값 합계 계산
    flights_grouped = flights.groupby(['year', 'month']).sum( ).unstack(level=0)

    # 히트맵 생성
    plt.figure(figsize=(12, 8))
    sns.heatmap(flights_grouped['passengers'], annot=True, fmt="d", cmap="YlGnBu", linewidths=0.5)
    plt.show( )

if __name__ == '__main__':
    # test1()
    # test2()
    test3()