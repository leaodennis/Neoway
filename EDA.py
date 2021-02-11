import sweetviz as sv
import pandas as pd
import xgboost as xgb

train = pd.read_csv('~/Neoway/data/pds_train.csv', sep=";")
train
report=sv.analyze(train)
report.show_html()
