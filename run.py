from core.model import *
from core.evaluation import *

import json
import xgboost as xgb
from sklearn.grid_search import GridSearchCV

train_file_path = './dataset/A_stock_daily/train.csv'
test_file_path = './dataset/A_stock_daily/test.csv'
configs = json.load(open('config.json', 'r'))





def main():

    df_train = pd.read_csv(train_file_path)
    x_train = df_train[configs['factor_feature_extract'][:-1]]
    y_train = df_train[configs['factor_feature_extract'][-1]]
    print('训练目标值分布：')
    print(y_train.value_counts())

    df_test = pd.read_csv(test_file_path)
    x_test = df_test[configs['factor_feature_extract'][:-1]]
    y_test = df_test[configs['factor_feature_extract'][-1]]

    other_params = configs['model_params']['other_params']
    cv_params = configs['model_params']['cv_params']

    model = xgb.XGBClassifier(**other_params)
    optimized_gbm = GridSearchCV(estimator=model, param_grid=cv_params, scoring='roc_auc', cv=5, verbose=1, n_jobs=4)
    optimized_gbm.fit(x_train, y_train)
    evaluate_result = optimized_gbm.grid_scores_
    print('每轮迭代运行结果:{0}'.format(evaluate_result))
    print('参数的最佳取值：{0}'.format(optimized_gbm.best_params_))
    print('最佳模型得分:{0}'.format(optimized_gbm.best_score_))



    #importance_of_features(model.fit(x_train, y_train))





if __name__ == '__main__':
    main()