# evaluation/evaluate.py ➤ Contains MAPE, RMSE, ADF test for model checks.

from statsmodels.tsa.stattools import adfuller
# ADF Test
def adf_test(series, label=''):
    result = adfuller(series.dropna())
    print(f"ADF Statistic for {label}:", result[0])
    print("p-value:", result[1])
    return result

