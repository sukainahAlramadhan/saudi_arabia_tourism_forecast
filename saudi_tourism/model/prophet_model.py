import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
from hijri_converter import convert


from saudi_tourism.data.prepare import prepare_data_demostic


def make_saudi_holidays(start_hijri_year=1436, end_hijri_year=1445):

    eid_alfitr = []
    eid_aladha = []
    national_day = []
    founding_day = []
    riyadh_season = []
    jeddah_season = []
    mid_year_break = []
    end_year_break = []

    # عيد الفطر
    for year in range(start_hijri_year, end_hijri_year + 1):
        date = convert.Hijri(year, 10, 1).to_gregorian()
        eid_alfitr.append({'holiday': 'eid_alfitr', 'ds': pd.to_datetime(date.isoformat()),
                           'lower_window': 0, 'upper_window': 3})

    # عيد الأضحى
    for year in range(start_hijri_year, end_hijri_year + 1):
        date = convert.Hijri(year, 12, 10).to_gregorian()
        eid_aladha.append({'holiday': 'eid_aladha', 'ds': pd.to_datetime(date.isoformat()),
                           'lower_window': 0, 'upper_window': 3})

    # اليوم الوطني
    for year in range(2015, 2024):
        national_day.append({'holiday': 'national_day', 'ds': pd.to_datetime(f'{year}-09-23'),
                             'lower_window': 0, 'upper_window': 1})

    # يوم التأسيس
    for year in range(2022, 2024):
        founding_day.append({'holiday': 'founding_day', 'ds': pd.to_datetime(f'{year}-02-22'),
                             'lower_window': 0, 'upper_window': 1})

    # موسم الرياض
    for year in range(2019, 2024):
        riyadh_season.append({'holiday': 'riyadh_season_start', 'ds': pd.to_datetime(f'{year}-10-01'),
                              'lower_window': 0, 'upper_window': 45})

    # موسم جدة
    for year in range(2019, 2024):
        jeddah_season.append({'holiday': 'jeddah_season_start', 'ds': pd.to_datetime(f'{year}-06-01'),
                              'lower_window': 0, 'upper_window': 45})

    # إجازة منتصف العام (يناير تقريبًا)
    for year in range(2015, 2024):
        mid_year_break.append({'holiday': 'mid_year_break', 'ds': pd.to_datetime(f'{year}-01-01'),
                               'lower_window': 0, 'upper_window': 15})

    # إجازة نهاية العام الدراسي (يونيو تقريبًا)
    for year in range(2015, 2024):
        end_year_break.append({'holiday': 'end_year_break', 'ds': pd.to_datetime(f'{year}-06-15'),
                               'lower_window': 0, 'upper_window': 20})

    # دمج جميع الإجازات
    holidays_df = pd.DataFrame(
        eid_alfitr + eid_aladha + national_day + founding_day + riyadh_season + jeddah_season + mid_year_break + end_year_break
    )
    return holidays_df


def prophet_train_visitor_d(model='prophet'):
        """
        Load and prepare the domestic tourism data.
        """
        # Load and prepare the dataset
        df_d = prepare_data_demostic()

        # Extract specific columns for modeling
        visitor_num_d = pd.DataFrame(df_d['number of visitor'])
        spend_d = pd.DataFrame(df_d['Tourists Spending'])

        # Let's keep the last 20% of the values out for testing purposes
        train_size = 0.9
        visitor_num_d_index = round(train_size*visitor_num_d.shape[0])

        ## VISITOR DATA
        visitor_num_d_train = visitor_num_d.iloc[:visitor_num_d_index]
        visitor_num_d_test = visitor_num_d.iloc[visitor_num_d_index:]

        if model=='baseline':
            ## predict the # visitors of prevus month as the # visitors of next month
            visitor_num_d_y_pred = visitor_num_d_test.shift(1).dropna()
            visitor_num_d_y_true = visitor_num_d_test[1:]

            visitor_num_d_base_accuracy = mean_absolute_percentage_error(visitor_num_d_y_true, visitor_num_d_y_pred)
            print(f"baseline model mape for visitor_num : {visitor_num_d_base_accuracy}")
            return visitor_num_d_base_accuracy

        elif model=='prophet':
            ## prepare data for prophet TRAIN
            visitor_num_d_prophet_train = visitor_num_d_train.reset_index().rename(columns={
            'Date': 'ds',
            'number of visitor': 'y'})
            ## prepare data for prophet TEST
            visitor_num_d_prophet_test = visitor_num_d_test.reset_index().rename(columns={
            'Date': 'ds',
            'number of visitor': 'y'})

            # Fit the model
            #prophet = Prophet()
            saudi_holidays = make_saudi_holidays()
            prophet = Prophet(
            seasonality_mode='multiplicative',
                yearly_seasonality=True,
                holidays=saudi_holidays,
                holidays_prior_scale=3,
                changepoint_prior_scale=0.05,
                changepoint_range=0.85
            )
            prophet.fit(visitor_num_d_prophet_train)

            # Prepare the future DataFrame (dates) for prediction
            future = visitor_num_d_prophet_test[['ds']]  # Just the dates from your test set
            preds = prophet.predict(future)  # Get predictions

            # Calculate accuracy using MAPE
            y_true = visitor_num_d_prophet_test['y'].values
            y_pred = preds['yhat'].values

            visitor_num_d_prophet_accuracy = mean_absolute_percentage_error(y_true, y_pred)
            print(f"Prophet MAPE for visitor_num: {visitor_num_d_prophet_accuracy:.2%}")


            return visitor_num_d_prophet_accuracy

            ## WITH DIFFERENT SPLIT SIZE:
            ## lower is better
            # 0.9 >> MAPE: 8.41%

            #-------------------------------------------------
            # without pramete change (Prophet MAPE for visitor_num: 8.47%)
            # after firist Prameter ---> 8.36 %
            # after holday ---->7.84%
            #Prophet MAPE for visitor_num: 7.79%
            #RMSE for visitors: 684.80
print("✅train_visitor DONE ")

def prophet_train_spends_d(model='prophet'):
        """
        Load and prepare the domestic tourism data.
        """
        # Load and prepare the dataset
        df_d = prepare_data_demostic()
        # Extract specific columns for modeling
        spend_d = pd.DataFrame(df_d['Tourists Spending'])



        ## SPENDS DATA
        train_size = 0.9
        spends_d_index = round(train_size*spend_d.shape[0])

        spends_d_train = spend_d.iloc[:spends_d_index]
        spends_d_test = spend_d.iloc[spends_d_index:]

        if model=='baseline':

            spends_d_y_pred = spends_d_test.shift(1).dropna()
            spends_d_y_true = spends_d_test[1:]
            spends_d_base_accuracy = mean_absolute_percentage_error(spends_d_y_true, spends_d_y_pred)
            print(f"baseline model mape for spends: {spends_d_base_accuracy}")

            return spends_d_base_accuracy

        elif model=='prophet':
            ## prepare data for prophet TRAIN
            spends_d_prophet_train = spends_d_train.reset_index().rename(columns={
                'Date': 'ds',
                'Tourists Spending': 'y'
            })


            ## prepare data for prophet TEST
            spends_d_prophet_test = spends_d_test.reset_index().rename(columns={
                'Date': 'ds',
                'Tourists Spending': 'y'
            })

            # Fit the model
           # Fit the model
            #prophet = Prophet()

            prophet = Prophet()

            prophet.fit(spends_d_prophet_train)

            # Prepare the future DataFrame (dates) for prediction
            future = spends_d_prophet_test[['ds']]  # Just the dates from your test set
            preds = prophet.predict(future)  # Get predictions

            # Calculate accuracy using MAPE
            y_true = spends_d_prophet_test['y'].values
            y_pred = preds['yhat'].values




            spends_d_prophet_accuracy = mean_absolute_percentage_error(y_true, y_pred)
            print(f"Prophet MAPE for spends: {spends_d_prophet_accuracy:.2%}")




            ## WITH DIFFERENT SPLIT SIZE:
            # 0.9 >> MAPE: 10.97%
            # without Prameter :
            #MAPE for spends: 10.64%
            #RMSE for spends: 1444.94
            return spends_d_prophet_accuracy

print("✅ train_spends DONE ")
