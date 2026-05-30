# path: ./test_matplotlib/matplotlib_test4.py
# pandas DataFrame 과 시각화 연계 처리 테스트 스크립트

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def test_csv_load(csv_path) -> pd.DataFrame:
    '함수 실행 시 읽을 csv 파일 경로를 전달받아서, csv 파일의 데이터를 읽어서 DataFrame 을 리턴하는 함수'
    df = pd.read_csv(csv_path)
    print(df.head())   # 위쪽 5개 출력 확인
    print(df.info())   # 데이터프레임 구조 확인
    '''
    <class 'pandas.DataFrame'>
    RangeIndex: 10 entries, 0 to 9
    Data columns (total 6 columns):
    #   Column        Non-Null Count  Dtype  
    ---  ------        --------------  -----  
    0   id            10 non-null     int64  
    1   age           10 non-null     int64  
    2   salary        10 non-null     int64  
    3   score         10 non-null     float64
    4   height        10 non-null     int64  
    5   age_category  10 non-null     str    
    dtypes: float64(1), int64(4), str(1)
    memory usage: 612.0 bytes
    None
    '''
    return df
# ----------------------------------------

def get_numeric_columns(df):
    'DataFrame 을 전달받아서, DataFrame 에서 수치형 컬럼만 추출해서 리턴하는 함수'
    numeric_cols = df.select_dtypes(include='number').columns
    print('Numeric columns : ', list(numeric_cols))
    return numeric_cols
# -----------------------------------------------------------------

def test_dataframe_hist_subplot(df):
    '수치형 컬럼 갯수 만큼 히스토그램 subplot 자동 생성하는 함수'
    numeric_cols = get_numeric_columns(df)
    col_cnt = len(numeric_cols)  # 5개

    fig, axes = plt.subplots(col_cnt, 1, figsize=(6, 4 * col_cnt))

    if col_cnt == 1:
        axes = [axes]

    for ax, col in zip(axes, numeric_cols):
        ax.hist(df[col], bins=10)
        ax.set_title(f'{col} Histogram')
        ax.set_xlabel(col)
        ax.set_ylabel('Count')

    plt.tight_layout()
    plt.show()
# ----------------------------------------------------------------------    

def test_dataframe_boxplot_subplot(df):
    '수치형 컬럼 갯수만큼 boxplot 여러 개를 subplot 으로 자동 생성하는 함수'
    numeric_cols = get_numeric_columns(df)
    col_cnt = len(numeric_cols)

    fig, axes = plt.subplots(1, col_cnt, figsize=(5 * col_cnt, 4))

    if col_cnt == 1:
        axes = [axes]

    for ax, col in zip(axes, numeric_cols):
        ax.boxplot(df[col])
        ax.set_title(f'{col} Boxplot')
        ax.set_ylabel(col)

    plt.tight_layout()
    plt.show()
# -----------------------------------------------    

def test_dataframe_groupby_subplot(df, category_col):
    '범주형(categorical) 컬럼 기준 숫자데이터 컬럼 평균에 대한 bar plot 생성 함수'
    numeric_cols = get_numeric_columns(df)
    grouped = df.groupby(category_col)[numeric_cols].mean()
    
    grouped.plot(kind='bar', figsize=(8, 4), title=f'Average by {category_col}')
    plt.ylabel('Mean Value')
    plt.show()
# -----------------------------------------------------------------    


if __name__ == '__main__':
    # 현재 py 파일 기준 경로 생성
    BASE_DIR = Path(__file__).resolve().parent  # 현재 파일이 있는 폴더 경로
    # print(BASE_DIR)

    csv_path = BASE_DIR.parent / 'data' / 'sample.csv' # 현재 py 의 위치를 기준으로 대상 파일까지의 경로 지정 (상대경로)
    # print(csv_path)

    df = test_csv_load(csv_path)
    # print(df)
    # print(type(df))

    # get_numeric_columns(df)

    # test_dataframe_hist_subplot(df)
    # test_dataframe_boxplot_subplot(df)

    # 범주형(categorical) 컬럼이 있는 경우만 실행함
    test_dataframe_groupby_subplot(df, 'age_category')


