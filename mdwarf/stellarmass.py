from sklearn.model_selection import train_test_split 
import numpy as np
import pandas as pd
import xgboost as xgb

df = pd.read_csv("jdli_imf.csv")

train_X, test_X, train_y, test_y = train_test_split(
    np.array(df[['Ksmag', 'logTe']]), 
    par_md_df['Mini'].values, 
    test_size = 0.25, random_state = 123
)



param = {"booster":"gbtree", "max_depth":100,
         "min_child_weight":5.5
         "gpu_id":0, 
        } 

model_MS = xgb.train(params = param, 
                  dtrain = train_dmatrix, 
                  evals=[(train_dmatrix, 'Train'), (test_dmatrix, 'Valid')],
                  num_boost_round = 10)

y_pred = model_MS.predict(test_dmatrix)

model_MS.save_model('par_to_MASS.json')
