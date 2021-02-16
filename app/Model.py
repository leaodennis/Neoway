import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
import datetime as dt
from imblearn.over_sampling import RandomOverSampler


def preprocess_data():

    # importing the dataset
    train = pd.read_csv('~/Neoway/data/pds_train.csv', sep=";")
    test = pd.read_csv('~/Neoway/data/pds_test.csv', sep=";")

    x_train = train.drop(["cd_ramo_atividade",
                          "cd_natureza_juridica",
                          "de_ramo_atividade",
                          "nm_micro_regiao",
                          "nm_meso_regiao",
                          "sg_uf_abrangencia",
                          "dt_situacao_especial",
                          "de_validade_pgfn",
                          "de_validade_fgts",
                          "de_optante_simples"], axis=1)
    x_test = test.drop(["cd_ramo_atividade",
                        "cd_natureza_juridica",
                        "de_ramo_atividade",
                        "nm_micro_regiao",
                        "nm_meso_regiao",
                        "sg_uf_abrangencia",
                        "dt_situacao_especial",
                        "de_validade_pgfn",
                        "de_validade_fgts",
                        "de_optante_simples"], axis=1)

    # remove single level columns
    for i in x_train.select_dtypes(exclude=np.number).columns.values:
        if (x_train[i].nunique() == 1):
            x_train.drop(columns=i, inplace=True)
    for i in x_test.select_dtypes(exclude=np.number).columns.values:
        if (x_test[i].nunique() == 1):
            x_test.drop(columns=i, inplace=True)

    # remove empty columns
    x_train = x_train.dropna(axis=1, how='all')
    x_test = x_test.dropna(axis=1, how='all')

    # complete levels
    x_train.de_indicador_telefone = x_train.de_indicador_telefone.fillna(
        'Unknown')
    x_test.de_indicador_telefone = x_test.de_indicador_telefone.fillna(
        'Unknown')
    x_train.de_situacao_especial = x_train.de_situacao_especial.fillna(
        'Unknown')
    x_test.de_situacao_especial = x_test.de_situacao_especial.fillna('Unknown')

    # fill empty fields > 50% of NaN
    na_pct = x_train.isna().sum() / len(x_train)
    missing_features = na_pct[na_pct > 0.50].index
    # missing features
    missing_features_train = x_train[missing_features]
    missing_features_test = x_test[missing_features]

    x_train.drop(missing_features_train, axis=1, inplace=True)
    x_test.drop(missing_features_test, axis=1, inplace=True)

    # fill 0 in numerical empty fields
    missing_features_train.fillna(0, inplace=True)
    missing_features_test.fillna(0, inplace=True)

    # append again
    x_train = pd.concat([x_train, missing_features_train], axis=1)
    x_test = pd.concat([x_test, missing_features_test], axis=1)

    # datetime diffs
    x_train.dt_abertura = pd.to_datetime(x_train.dt_abertura)
    x_test.dt_abertura = pd.to_datetime(x_test.dt_abertura)

    x_train.dt_abertura = (x_train.dt_abertura -
                           dt.datetime.now()).dt.days.abs()
    x_test.dt_abertura = (x_test.dt_abertura -
                          dt.datetime.now()).dt.days.abs()

    x_train.dh_ultima_atualizacao = pd.to_datetime(
        x_train.dh_ultima_atualizacao)
    x_test.dh_ultima_atualizacao = pd.to_datetime(
        x_test.dh_ultima_atualizacao)

    x_train.dh_ultima_atualizacao = (
        x_train.dh_ultima_atualizacao - dt.datetime.now()).dt.days.abs()
    x_test.dh_ultima_atualizacao = (
        x_test.dh_ultima_atualizacao - dt.datetime.now()).dt.days.abs()

    x_train.dh_processamento = pd.to_datetime(x_train.dh_processamento)
    x_test.dh_processamento = pd.to_datetime(x_test.dh_processamento)

    x_train.dh_processamento = (
        x_train.dh_processamento - dt.datetime.now()).dt.days.abs()
    x_test.dh_processamento = (
        x_test.dh_processamento - dt.datetime.now()).dt.days.abs()

    x_train.dt_situacao = pd.to_datetime(x_train.dt_situacao)
    x_test.dt_situacao = pd.to_datetime(x_test.dt_situacao)

    x_train.dt_situacao = (x_train.dt_situacao -
                           dt.datetime.now()).dt.days.abs()
    x_test.dt_situacao = (x_test.dt_situacao -
                          dt.datetime.now()).dt.days.abs()

    # input 0 in renda_censitaria_2010
    x_train.renda_censitaria_2010 = x_train.renda_censitaria_2010.fillna(0)
    x_test.renda_censitaria_2010 = x_test.renda_censitaria_2010.fillna(0)

    # drop rows
    x_train.dropna(axis=0, inplace=True)
    x_test.dropna(axis=0, inplace=True)

    y_train = x_train["ind_atividade"]

    x_train = x_train.drop(["ind_atividade"], axis=1)

    # id for prediction
    test_id = x_test.id

    # drop id
    x_train = x_train.drop(["id"], axis=1)
    x_test = x_test.drop(["id"], axis=1)

    return x_train, y_train, x_test, test_id


x_train, y_train, x_test, test_id = preprocess_data()


def encode_features(over=True):

    global x_train, y_train, x_test

    if over == True:
        x_train, y_train = RandomOverSampler(
            sampling_strategy='minority').fit_resample(x_train, y_train)
        x_train = pd.get_dummies(x_train)
        x_test = pd.get_dummies(x_test)
    else:
        x_train = pd.get_dummies(x_train)
        x_test = pd.get_dummies(x_test)

    x_train, x_valid, y_train, y_valid = train_test_split(
        x_train, y_train, test_size=0.2)

    return x_train, x_valid, y_train, y_valid, x_test


x_train, x_valid, y_train, y_valid, x_test = encode_features(over=True)


space = {'max_depth': hp.quniform("max_depth", 3, 18, 1),
         'gamma': hp.uniform('gamma', 1, 9),
         'colsample_bytree': hp.uniform('colsample_bytree', 0.5, 1),
         'min_child_weight': hp.quniform('min_child_weight', 0, 10, 1),
         'scale_pos_weight': hp.quniform('scale_pos_weight', 0, 1, .05)
         }


def objective(space):

    clf = xgb.XGBClassifier(nthread=4,
                            use_label_encoder=False,
                            max_depth=int(space['max_depth']),
                            gamma=space['gamma'],
                            min_child_weight=int(space['min_child_weight']),
                            colsample_bytree=int(space['colsample_bytree']),
                            scale_pos_weight=space['scale_pos_weight'])
    clf.fit(x_train, y_train,
            eval_set=[(x_train, y_train), (x_valid, y_valid)], eval_metric="auc", verbose=False)
    pred = clf.predict(x_valid)
    accuracy = metrics.roc_auc_score(y_valid, pred)
    print("SCORE:", accuracy)

    return {'loss': 1-accuracy, 'status': STATUS_OK}


trials = Trials()

best_hyperparams = fmin(fn=objective,
                        space=space,
                        algo=tpe.suggest,
                        max_evals=100,
                        trials=trials)


print("The best hyperparameters are : ", "\n")
print(best_hyperparams)

#fine tunning
best_model = xgb.XGBClassifier(nthread=4,
                               use_label_encoder=False,
                               max_depth=int(best_hyperparams['max_depth']),
                               gamma=best_hyperparams['gamma'],
                               min_child_weight=int(
                                   best_hyperparams['min_child_weight']),
                               colsample_bytree=int(
                                   best_hyperparams['colsample_bytree']),
                               scale_pos_weight=best_hyperparams['scale_pos_weight'])
# default
best_model = xgb.XGBClassifier(nthread=4,
                               use_label_encoder=False)

best_model.fit(x_train, y_train, eval_metric="auc", verbose=False,
               eval_set=[(x_train, y_train), (x_valid, y_valid)])

y_valid_pred = best_model.predict_proba(x_valid)[:, 1]

print('Validation ROC AUC score: ', metrics.roc_auc_score(
    y_valid, (y_valid_pred >= .5).astype(int)))

# save model
best_model.save_model('best_model.model')

# prob submission
prob_submission = best_model.predict_proba(x_test)[:, 1]

# label submission
label_submission = (prob_submission >= .5).astype(int)

# save processed data
submission = pd.DataFrame({'prob': prob_submission, 'label': label_submission})

submission = pd.concat([submission, test_id], axis=1)

submission.to_csv("test.csv")

# save validation data
validation = pd.DataFrame({'truth': y_valid, 'pred': (y_valid_pred >= .5).astype(int)})

validation.to_csv("validation.csv")
