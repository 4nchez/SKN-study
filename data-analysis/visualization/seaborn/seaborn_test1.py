import seaborn as sns
import matplotlib.pyplot as plt
'''
2012년도 개발
Matplotlib 기반으로 개발
pandas.DataFrame 에 효과적으로 이용됨

pip install seaborn

Seaborn 데이터셋 (Dataset)
• anscombe
• car_crashes
• flights
• iris
• tips
• titanics
'''


tips = sns.load_dataset("tips")
#  식당에서 손님들이 내는 팁과 관련된 데이터
print(tips.head())
print(type(tips))   # <class 'pandas.DataFrame'>
print(tips.info())
'''
<class 'pandas.DataFrame'>
RangeIndex: 244 entries, 0 to 243
Data columns (total 7 columns):
 #   Column      Non-Null Count  Dtype   
---  ------      --------------  -----   
 0   total_bill  244 non-null    float64 
 1   tip         244 non-null    float64 
 2   sex         244 non-null    category
 3   smoker      244 non-null    category
 4   day         244 non-null    category
 5   time        244 non-null    category
 6   size        244 non-null    int64   
dtypes: category(4), float64(2), int64(1)
memory usage: 7.4 KB
None
'''

def test1():
    '''수치형 2차원 scatterplot => seaborn 의 기본임
        색(hue), 크기(size), 스타일(style), 마커의 형태(Markers) 등 변경 가능
    '''
    sns.relplot(x='total_bill', y='tip', data=tips)
    plt.show( )

def test2():
    sns.relplot(x='total_bill', y='tip',  kind='line', data=tips)
    plt.show( )

def test3():
    sns.relplot(x="total_bill", y="tip", hue="smoker", data=tips)
    plt.show( )

def test4():
    sns.pairplot(data=tips)
    # 대각선은 histogram, 그 외에는 scatter
    plt.show( )

def test5():
    sns.pairplot(tips, vars=['total_bill', 'tip', 'size', 'day'])
    plt.show( )

def test6():
    sns.pairplot(tips, y_vars=['total_bill', 'tip', 'day'], x_vars=['total_bill', 'tip'])
    plt.show( )

def test7():
    sns.pairplot(tips, vars=['total_bill', 'tip', 'size', 'day'], kind='scatter', diag_kind='hist', palette='pastel')
    plt.show( )

def test8():
    sns.pairplot(tips, kind='kde', diag_kind='hist', hue='smoker')
    plt.show( )

def test9():
    pivot_table = tips.pivot_table(values='tip', index='day', columns='time', aggfunc='mean')
    sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', linewidths=0.5)
    plt.show( )

def test10():
    selected_columns = tips[['total_bill', 'tip']]
    corr = selected_columns.corr( )
    sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.show( )


if __name__ == '__main__':
    # test1()
    # test2()
    # test3()
    # test4()
    # test5()
    # test6()
    # test7()
    # test8()
    # test9()
    test10()