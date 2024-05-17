import os
import time
import six.moves.cPickle as pickle
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import autosklearn.regression

def train_autosklearn_models(X, y, max_train_secs_per_output=120, memory_limit=1024 * 100):
    X = np.array(X)
    y = np.array(y)
    
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)

    # Train autosklearn model for each output variable
    model_paths = []
    for i in range(np.shape(y_train)[1]):
        model = autosklearn.regression.AutoSklearnRegressor(time_left_for_this_task=max_train_secs_per_output, memory_limit=memory_limit)
        model.fit(X_train, y_train[:, i])
        model_path = f'/tmp/automlmoo_models/out{i}_{time.strftime("%Y%m%d-%H%M%S")}.dump'
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)

        model_paths.append(model_path)

        print(model.leaderboard())

        test_predictions = model.predict(X_test)
        print(f'Test RMSE: {np.sqrt(mean_squared_error(y_test[:, i], test_predictions))}, R-squared: {r2_score(y_test[:, i], test_predictions)}')

    return model_paths