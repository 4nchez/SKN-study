# ANN(Artificial Neural Network) 실습문제

# 심화 실습문제

## 실습문제 1. 상관계수(Correlation Coefficient) 분석

1. 상관계수(Correlation Coefficient)의 의미를 설명하시오.
   - 두 변수 간의 선형적 관계의 강도와 방향을 나타내는 통계적 지표
   - 한 변수가 변할 때 다른 변수가 어떤 방향으로, 얼마나 일정하게 변하는지를 규격화된 수치로 제공함
2. 상관계수 값의 범위를 작성하시오.
   - $-1 \leq r \leq 1$
3. 상관계수가 0.95인 경우 모델 성능을 평가하시오.
   - 두 변수(예: 실제값과 예측값)가 매우 강한 양의 선형 상관관계를 가지고 있음
4. 상관계수와 MSE의 차이점을 설명하시오.
   - 상관계수: 두 변수 간의 선형적 변화 경향성(패턴)을 측정
   - MSE: 실제값과 예측값 간의 절대적인 오차 크기(정확도)를 측정

---

## 실습문제 2. 과적합(Overfitting) 분석

1. 과적합(Overfitting)의 의미를 설명하시오.
   - 모델이 훈련 데이터에만 지나치게 맞춰져 새로운 실제 데이터(테스트 데이터)에 대한 예측 능력이 떨어지는 현상
2. 은닉노드를 50개 이상으로 증가시켰을 때 발생할 수 있는 문제를 설명하시오.
    - 과적합 발생: 모델의 표현력이 너무 커져 훈련 데이터의 잡음(Noise)까지 학습함
    - 연산 비용 증가: 학습해야 할 가중치(Weight) 파라미터가 급증하여 학습 속도가 느려짐
    - 경사 소실/폭발: 신경망이 깊고 복잡해지면서 역전파 과정에서 기울기가 사라지거나 과도하게 커질 수 있음
3. 과적합을 방지하는 방법을 3가지 이상 작성하시오.
    - 드롭아웃(Dropout): 학습 시 은닉층의 뉴런을 무작위로 비활성화하여 특정 뉴런에 대한 의존도를 낮춤
    - 데이터 증강(Data Augmentation): 데이터를 변형하거나 추가하여 학습 데이터의 양과 다양성을 확보함
    - 규제화(Regularization): L1(Lasso) 또는 L2(Ridge) 규제를 통해 가중치의 절대값이 너무 커지지 않도록 패널티를 부여함

---

## 실습문제 3. 하이퍼파라미터 튜닝

다음 항목을 변경하여 실험을 수행하시오.

* Epoch
* Learning Rate
* Hidden Node 수
* Hidden Layer 수
* Activation Function
```python
# 실험 조건
epochs_list = [5000, 8000, 10000]
lr_list = [0.01, 0.001, 0.003]
hidden_layers_list = [
    [5],
    [5, 5],
    [5, 3, 2]
]
activation_list = [
    'sigmoid',
    'softplus',
    'tanh',
    'relu'
]
```
### 작성 내용

실험 조건 하 최상위 성능 모델 3개 선정

| 실험번호 | Epoch | Learning Rate | Hidden Node | Activation | MSE |
|--|--|--|--|--|--|
| 실험7  |    5000 |           0.01  | 5-5        | tanh         | 0.00489233 |
| 실험43  |    8000 |           0.01  | 5-5        | tanh         | 0.0049253  |
| 실험107  |   10000 |           0.003 | 5-3-2     | tanh         | 0.00493805 |

실험 결과를 비교하고 가장 성능이 좋은 모델을 선택하시오.

실험 결과, 아래 조건의 모델에서 가장 우수한 성능을 확인함. (실험7)
* Epoch: 5000
* Learning Rate: 0.01
* Hidden Node 수: 5-5 (각 Hidden Layer당 5개)
* Hidden Layer 수: 2
* Activation Function: tanh
---

## 실습문제 4. 활성화 함수 성능 비교

다음 활성화 함수를 적용하여 성능을 비교하시오.

* Sigmoid
* Tanh
* ReLU
* Softplus

### 작성 내용

실습문제 3. 의 실험 내용을 바탕으로 가장 좋은 성능 기준으로 작성함.

| Activation Function | MSE | Correlation |
|--|--|--|
| Sigmoid                  | 0.00496159 |      0.938269 |    
| Tanh                     | 0.00489233 |      0.93877  |  
| ReLU                     | 0.00638154 |      0.920698 |
| Softplus                 | 0.00529839 |      0.933457 |

가장 좋은 성능을 보인 활성화 함수를 선택하고 이유를 설명하시오.
- Tanh는 zero-centered 출력과 부드러운 gradient 흐름 덕분에 현재 실험 환경에서 가장 안정적으로 수렴하여 가장 낮은 MSE와 높은 상관계수를 보였다.
---

## 실습문제 5. 최종 모델 평가 보고서 작성

다음 항목을 포함하여 최종 보고서를 작성하시오.


### 1. 데이터셋 설명

본 연구에서는 `concrete_stg.csv` 데이터를 활용하였다.  
해당 데이터셋은 콘크리트 배합 성분을 기반으로 압축 강도(`strength`)를 예측하는 회귀 문제로 구성되어 있다.

- 입력 변수: 콘크리트 구성 재료(시멘트, 물, 골재 등)
- 출력 변수: 콘크리트 압축 강도(`strength`)
- 문제 유형: 지도학습 기반 회귀(Regression)

본 연구의 목적은 주어진 재료 조합으로부터 콘크리트의 압축 강도를 예측하는 인공신경망 모델을 구축하고 성능을 비교 분석하는 것이다.

### 2. 정규화 방법

입력 데이터에 대해서는 Min-Max Normalization을 적용하였다.

```python
def min_max_normalize(series):
    min_value = series.min()
    max_value = series.max()

    if max_value == min_value:
        return pd.Series(np.zeros(len(series)), index=series.index)

    return (series - min_value) / (max_value - min_value)
````

#### 수식 정의

$x' = \frac{x - x_{min}}{x_{max} - x_{min}}$

#### 적용 목적

* 입력 변수 간 스케일 차이 제거
* 경사 하강법 기반 학습 안정성 확보
* 수렴 속도 개선

#### 특징

* 모든 입력값을 [0, 1] 범위로 변환
* 이상치(outlier)에 민감하게 반응
* 음수 값이 존재하지 않음

### 3. Model 1 구조 (실험 7)

* Epoch: 5000
* Learning Rate: 0.01
* Hidden Layer: 5-5
* Activation Function: Tanh
* Optimizer: Adam
* Loss Function: MSELoss

#### 네트워크 구조

입력 → Linear(5) → Tanh → Linear(5) → Tanh → Output

#### 성능

* MSE: **0.00489233**

### 4. Model 2 구조 (실험 43)

* Epoch: 8000
* Learning Rate: 0.01
* Hidden Layer: 5-5
* Activation Function: Tanh
* Optimizer: Adam
* Loss Function: MSELoss

#### 네트워크 구조

입력 → Linear(5) → Tanh → Linear(5) → Tanh → Output

#### 성능

* MSE: **0.00492530**

#### 5. Model 3 구조 (실험 107)

* Epoch: 10000
* Learning Rate: 0.003
* Hidden Layer: 5-3-2
* Activation Function: Tanh
* Optimizer: Adam
* Loss Function: MSELoss

#### 네트워크 구조

입력 → Linear(5) → Tanh → Linear(3) → Tanh → Linear(2) → Tanh → Output

#### 성능

* MSE: **0.00493805**

### 6. 손실 함수

본 연구에서는 평균제곱오차(Mean Squared Error, MSE)를 손실 함수로 사용하였다.

```python
criterion = nn.MSELoss()
```

#### 정의

$MSE = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2$

#### 특징

* 회귀 문제에 적합한 표준 손실 함수
* 오차를 제곱하여 큰 오차에 대해 높은 패널티 부여
* 모델이 평균적으로 정확한 값을 예측하도록 유도

### 7. Optimizer

본 연구에서는 Adam Optimizer를 사용하였다.

```python
optimizer = optim.Adam(model.parameters(), lr=lr)
```

#### 특징

* Momentum과 RMSProp의 결합 구조
* 개별 파라미터에 대해 적응적 학습률 적용
* 비정상적 gradient 상황에서도 안정적 수렴 가능

#### 장점

* 빠른 수렴 속도
* 하이퍼파라미터 민감도 감소
* 비선형 문제에서 안정적 성능 확보

### 8. 실험 결과 비교

| 실험번호  | Epoch | Learning Rate | Hidden Layer | Activation | MSE        |
| ----- | ----- | ------------- | ------------ | ---------- | ---------- |
| 실험7   | 5000  | 0.01          | 5-5          | Tanh       | 0.00489233 |
| 실험43  | 8000  | 0.01          | 5-5          | Tanh       | 0.00492530 |
| 실험107 | 10000 | 0.003         | 5-3-2        | Tanh       | 0.00493805 |

#### 분석 결과

* 모든 모델에서 유사한 수준의 성능이 확인됨
* Model 1이 가장 낮은 MSE를 기록함
* 네트워크가 깊어질수록 성능이 개선되지 않고 오히려 소폭 저하됨

### 9. 최종 선택 모델

#### 선정 모델: Model 1 (실험 7)

* MSE: **0.00489233**
* 구조: 5-5
* Activation: Tanh
* Epoch: 5000
* Learning Rate: 0.01

#### 선정 근거

* 최소 MSE 달성
* 구조 단순성에 따른 일반화 성능 확보
* 계산 효율 대비 성능 우수

### 10. 성능 향상 방안

#### 1) 입력 데이터 정규화 개선

* Min-Max Scaling 대신 Standardization 적용 검토 필요
* 데이터 분포 중심화(z-score normalization)로 학습 안정성 향상 가능

#### 2) 네트워크 구조 확장

* Hidden layer node 수 증가 (예: 10-10, 10-8-6)
* 표현력 증가를 통한 비선형 관계 학습 개선

#### 3) 정규화 기법 추가

* Dropout 적용을 통한 overfitting 방지
* L2 regularization을 통한 weight 제한

#### 4) 활성화 함수 확장 실험

* ReLU, LeakyReLU, ELU 등 비교 실험 필요
* 비선형 표현력 및 gradient 흐름 개선 가능성 존재

#### 5) 학습 전략 개선

* Early stopping 적용
* Learning rate scheduler 적용
* 최적 epoch 자동 탐색

### 최종 결론

본 연구에서는 콘크리트 압축강도 예측을 위해 다양한 신경망 구조를 비교 분석하였다.
그 결과, Tanh 활성화 함수와 2-layer hidden structure(5-5)를 사용한 Model 1이 가장 낮은 MSE를 기록하며 가장 우수한 성능을 보였다.

이는 본 데이터셋이 비교적 작은 규모의 회귀 문제이며, 과도하게 깊은 네트워크보다 안정적인 shallow network가 더 적합함을 시사한다.


---

### 추가 도전 과제 : 
하단에 코드셀 추가해서 코드로 작성하고, 코드를 이곳에 복사해서 제출합니다. ==============

#### 도전 과제 1

은닉층을 다음과 같이 변경하여 성능을 비교하시오.

```
hidden_layers=[10,10]
hidden_layers=[20,20]
hidden_layers=[50,50]
```
Source Code
```python
input_dim = len(feature_cols)
for hidden_layers in [[10,10], [20,20],[50,50]]:
    # Create Model
    model = ConcreteANN(
        input_dim=input_dim,
        hidden_layers=hidden_layers,
        activation='tanh'
    )

    # Train phase
    model, loss = train_model(
        model,
        X_train,
        y_train,
        epochs=5000,
        lr=lr,
        print_every=1000
    )

    # Test phase
    pred, corr, mse = evaluate_model(
        model,
        X_test,
        y_test
    )

    # Save experiment logs and evaluation metrics
    ...
```
Result
| 실험번호   | Hidden Node   |        MSE |   Correlation |
|:-----------|:--------------|-----------:|--------------:|
| 실험1      | 10-10      | 0.00504407 |      0.937051 |
| 실험2      | 20-20      | 0.00496357 |      0.941632 |
| 실험3      | 50-50      | 0.00444133 |      0.945617 |

---

#### 도전 과제 2

Dropout Layer를 추가하여 과적합을 감소시키시오.

```python
class ConcreteANN(nn.Module):
    def __init__(self, ...,
                 use_drop_out: bool = False, drop_out_raito: float = 0.1
                 ):
                 
         ...
         
         if use_drop_out:
            layers.append(nn.Dropout(drop_out_raito))

         ...

input_dim = len(feature_cols)
for hidden_layers in [[10,10], [20,20],[50,50]]:
    # Create Model
    model = ConcreteANN(
        input_dim=input_dim,
        hidden_layers=hidden_layers,
        activation='tanh',
        use_drop_out=True,
        drop_out_raito=0.1
    )
    ...
```
Result
| 실험번호   | Hidden Node   |        MSE |   Correlation |
|:-----------|:--------------|-----------:|--------------:|
| 실험1      | 10-10      | 0.00717385 |      0.908617 |
| 실험2      | 20-20      | 0.00646489 |      0.91843  |
| 실험3      | 50-50      | 0.00537196 |      0.932468 |

---

#### 도전 과제 3

Batch Normalization을 추가하여 성능 변화를 확인하시오.

```python
class ConcreteANN(nn.Module):
    def __init__(self, ...,                    
                 use_batch_norm: bool = False
                 ):
                 
         ...
         
         if use_batch_norm:
            layers.append(nn.BatchNorm1d(hidden_dim))


input_dim = len(feature_cols)
for hidden_layers in [[10,10], [20,20],[50,50]]:
    # Create Model
    model = ConcreteANN(
        input_dim=input_dim,
        hidden_layers=hidden_layers,
        activation='tanh',
        use_drop_out=True,
        drop_out_raito=0.1,
        use_batch_norm=True
    )
    ...
```
Result
| 실험번호   | Hidden Node   |        MSE |   Correlation |
|:-----------|:--------------|-----------:|--------------:|
| 실험1      | 10-10      | 0.00555061 |      0.930419 |
| 실험2      | 20-20      | 0.00479311 |      0.940507 |
| 실험3      | 50-50      | 0.00443099 |      0.948271 |

---

#### 도전 과제 4

학습 과정에서 Epoch별 Loss 그래프를 출력하고 결과를 분석하시오.

```python
input_dim = len(feature_cols)
loss_list = []
for hidden_layers in [[10,10], [20,20],[50,50]]:
    ...

    # Train phase
    model, loss = train_model(
        model,
        X_train,
        y_train,
        epochs=5000,
        lr=lr,
        print_every=1000
    )
    loss_list.append(loss)

    ...

    
experiment_names = ['experiment1(10-10)', 'experiment2(20-20)', 'experiment3(50-50)']

plt.figure(figsize=(10,6))

for i, loss in enumerate(loss_list):
    plt.plot(range(1, len(loss)+1), loss, label=experiment_names[i])

plt.xlabel('Epoch')
plt.ylabel('MSE')
plt.title('Epoch-wise MSE')
plt.legend()
plt.grid(True)
plt.show()
```

---

#### 도전 과제 5

실제값(Actual)과 예측값(Predicted)을 Scatter Plot으로 시각화하고 모델 성능을 분석하시오.
```python
input_dim = len(feature_cols)
pred_list = []
for hidden_layers in [[10,10], [20,20],[50,50]]:
    ...

    # Test phase
    pred, corr, mse = evaluate_model(
        model,
        X_test,
        y_test
    )
    pred_list_4.append(pred)

    ...


from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

y_test_cpu = y_test.cpu().numpy()

experiment_names = ['experiment1', 'experiment2', 'experiment3']

plt.figure(figsize=(6,6))
for i, preds in enumerate(pred_list):
    plt.scatter(y_test_cpu, preds, label=experiment_names[i])

plt.plot([y_test_cpu.min(), y_test_cpu.max()], [y_test_cpu.min(), y_test_cpu.max()], 'r--', lw=2)
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs Predicted Scatter Plot')
plt.legend()
plt.grid(True)
plt.show()

for i, preds in enumerate(pred_list):
    mse = mean_squared_error(y_test_cpu, preds)
    mae = mean_absolute_error(y_test_cpu, preds)
    r2 = r2_score(y_test_cpu, preds)
    print(f"{experiment_names[i]} Performance:")
    print(f"  MSE: {mse:.4f}")
    print(f"  MAE: {mae:.4f}")
    print(f"  R² Score: {r2:.4f}\n")
```
Result
```
experiment1 Performance:
  MSE: 0.0056
  MAE: 0.0557
  R² Score: 0.8650

experiment2 Performance:
  MSE: 0.0048
  MAE: 0.0502
  R² Score: 0.8834

experiment3 Performance:
  MSE: 0.0044
  MAE: 0.0460
  R² Score: 0.8922
```