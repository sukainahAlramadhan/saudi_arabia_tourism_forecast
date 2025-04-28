import pandas as pd
from darts import TimeSeries
from darts.metrics import mape
from sklearn.metrics import mean_absolute_percentage_error
import matplotlib.pyplot as plt
from darts.models import AutoTBATS

from saudi_tourism.data.prepare import prepare_data_inbound


def AutoTBATS_train_visitor_i(model='AutoTBATS'):
        """
        Load and prepare the inbound tourism data.
        """
        # Load and prepare the dataset
        df_i = prepare_data_inbound()

        # Extract specific columns for modeling
        visitor_num_i = pd.DataFrame(df_i['number of visitor'])
        spend_i = pd.DataFrame(df_i['Tourists Spending'])

        # Let's keep the last 10% of the values out for testing purposes ~ 1 year
        train_size = 0.9
        visitor_num_i_index = round(train_size*visitor_num_i.shape[0])

        ## VISITOR DATA
        visitor_num_i_train = visitor_num_i.iloc[:visitor_num_i_index]
        visitor_num_i_test = visitor_num_i.iloc[visitor_num_i_index:]

        if model=='baseline':
            ## predict the # visitors of prevus month as the # visitors of next month
            visitor_num_i_y_pred = visitor_num_i_test.shift(1).dropna()
            visitor_num_i_y_true = visitor_num_i_test[1:]

            visitor_num_i_base_accuracy = mean_absolute_percentage_error(visitor_num_i_y_true, visitor_num_i_y_pred)
            print(f"BASELINE model MAPE for VISITOR_NUM in the inbound dataset using AutoTBATS: {visitor_num_i_base_accuracy}")

            return visitor_num_i_base_accuracy

        elif model=='AutoTBATS':
            ## prepare data for prophet TRAIN
            visitor_num_i_train_series = TimeSeries.from_dataframe(visitor_num_i_train, value_cols="number of visitor")
            visitor_num_i_test_series = TimeSeries.from_dataframe(visitor_num_i_test, value_cols="number of visitor")

            # Initialize the model & the parameters only season_length because other parameters are found by AUTO since it is AutoTBATS, then Fit the model
            AutoTBATS_model = AutoTBATS(season_length=12)
            AutoTBATS_model.fit(visitor_num_i_train_series)


            # Prepare the future DataFrame (dates) for prediction
            pred = AutoTBATS_model.predict(len(visitor_num_i_test_series))
            pred.values()


            error = mape(visitor_num_i_test_series, pred)
            # print(f"MAPE: {error:.2f}%")
            # print(f"AutoTBATS MAPE for VISITOR_NUM in INBOUND DATA: {error:.2%}")


            return error

print("✅train_visitor DONE ")


def AutoTBATS_train_spends_I(model='AutoTBATS'):
        """
        Load and prepare the domestic tourism data.
        """
        # Load and prepare the dataset
        df_i = prepare_data_inbound()
        # Extract specific columns for modeling
        spend_i = pd.DataFrame(df_i['Tourists Spending'])

        ## SPENDS DATA
        train_size = 0.9
        spends_i_index = round(train_size*spend_i.shape[0])

        spends_i_train = spend_i.iloc[:spends_i_index]
        spends_i_test = spend_i.iloc[spends_i_index:]

        if model=='baseline':
            ## predict the # visitors of prevus month as the # visitors of next month
            spends_i_y_pred = spends_i_test.shift(1).dropna()
            spends_i_y_true = spends_i_test[1:]
            spends_i_base_accuracy = mean_absolute_percentage_error(spends_i_y_true, spends_i_y_pred)
            print(f"BASELINE model MAPE for SPENDS in the inbound dataset using AutoTBATS: {spends_i_base_accuracy}")

            return spends_i_base_accuracy

        elif model=='AutoTBATS':
            ## prepare data for prophet TRAIN
            spends_i_train_series = TimeSeries.from_dataframe(spends_i_train, value_cols="Tourists Spending")
            spends_i_test_series = TimeSeries.from_dataframe(spends_i_test, value_cols="Tourists Spending")

           # Fit the model
            #prophet = Prophet()

            AutoTBATS_model = AutoTBATS(season_length=6)
            AutoTBATS_model.fit(spends_i_train_series)

            # Prepare the future DataFrame (dates) for prediction
            pred = AutoTBATS_model.predict(len(spends_i_test_series))
            pred.values()

            # Calculate accuracy using MAPE
            error = mape(spends_i_test_series, pred)
            # print(f"MAPE: {error:.2f}%")
            # print(f"AutoTBATS MAPE for SPENDS in INBOUND DATA: {error:.2%}")

            return error

print("✅ train_spends DONE ")
