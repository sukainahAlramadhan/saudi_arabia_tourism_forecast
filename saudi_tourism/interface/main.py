# interface/main.py ➤ Optional: Main entry to run the full pipeline (prep → model → evaluate).
from saudi_tourism.model.auto_tbats_model import AutoTBATS_train_spends_I, AutoTBATS_train_visitor_i
from saudi_tourism.model.prophet_model import prophet_train_spends_d, prophet_train_visitor_d


if __name__=='__main__':
   print(AutoTBATS_train_visitor_i('AutoTBATS'))

   print(AutoTBATS_train_spends_I('AutoTBATS'))

   print(prophet_train_visitor_d('prophet'))

   print(prophet_train_spends_d('prophet'))
