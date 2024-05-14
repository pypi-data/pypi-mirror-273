import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dropout
from tensorflow.keras.utils import to_categorical

from sklearn.metrics import classification_report,confusion_matrix #For model evaluation metrics
from sklearn.model_selection import StratifiedKFold
from tensorflow.python.keras.losses import categorical_crossentropy
from sklearn.model_selection import StratifiedKFold
from sklearn import preprocessing, model_selection
from statistics import mean, stdev
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import normalize

class gcexplain():
  def shape_val(val):
    shap = val.shape
    return shap

  def epsilon():
    return np.finfo(float).eps

  def kullback_leibler_divergence(y_true, y_pred):
      y_true = np.clip(y_true, gcexplain.epsilon(), 1.0)
      y_pred = np.clip(y_pred, gcexplain.epsilon(), 1.0)
      ret_val = np.sum(y_true * np.log(y_true / y_pred), axis=-1)
      return ret_val

  def stop_gradient(val):
          return val
  def get_loss_val(loss_function, y_true, y_pred):
      ret_val = loss_function(y_true, y_pred)

      if len(gcexplain.shape_val(ret_val)) == 2 and gcexplain.shape_val(ret_val)[-1] == 1:
          # Value returned by __loss_function__ should be of shape (num_samples,)
          ret_val = np.squeeze(ret_val, axis=-1)

      if len(gcexplain.shape_val(ret_val)) == 0 or (
              gcexplain.shape_val(ret_val)[0] is not None and
              gcexplain.shape_val(y_true)[0] is not None and
              gcexplain.shape_val(ret_val)[0] != gcexplain.shape_val(y_true)[0]
      ):
          raise ValueError("Your custom loss function must return a scalar for each pair of y_pred and y_true values. "
                          "Please ensure that your loss function does not, for example, average over all samples, "
                          "as it would then return only one scalar value "
                          "independently of the number of samples passed.")

      return ret_val

  def get_delta_errors_fixed_size(y_true, all_but_one_auxiliary_outputs, error_with_all_features,
                                  loss_function, log_transform):
      delta_errors = []
      for all_but_one_auxiliary_output in all_but_one_auxiliary_outputs:
          error_without_one_feature = gcexplain.get_loss_val(
              loss_function, y_true, all_but_one_auxiliary_output
          )

          # The error without the feature is an indicator as to how potent the left-out feature is as a predictor.
          delta_error = np.maximum(error_without_one_feature - error_with_all_features, gcexplain.epsilon())
          if log_transform:
              delta_error = np.log(1 + delta_error)
          delta_errors.append(delta_error)
      delta_errors = np.stack(delta_errors, axis=-1)
      return delta_errors

  def get_delta_errors(y_true, all_but_one_auxiliary_outputs, error_with_all_features,
                      loss_function, log_transform):
      return gcexplain.get_delta_errors_fixed_size(y_true, all_but_one_auxiliary_outputs, error_with_all_features,
                                        loss_function, log_transform)


  def causal_value(y_true, auxiliary_outputs, all_but_one_auxiliary_outputs,
                            loss_function, log_transform=False):
    delta_errors = []

    error_with_all_features = gcexplain.get_loss_val(loss_function, y_true, auxiliary_outputs)
    error_without_one_feature = gcexplain.get_loss_val(loss_function, y_true, all_but_one_auxiliary_outputs)


    # The error without the feature is an indicator as to how potent the left-out feature is as a predictor.
    delta_error = np.maximum(error_without_one_feature - error_with_all_features, gcexplain.epsilon())

    delta_errors.append(delta_error)
    delta_errors = np.stack(delta_errors, axis=-1)

    shape_result = gcexplain.shape_val(delta_errors)
    if shape_result is not None and len(shape_result) > 2:
        delta_errors = np.squeeze(delta_errors, axis=-2)
    delta_errors = delta_errors.flatten()
    delta_errors /= (np.sum(delta_errors, axis=-1, keepdims=True))
    delta_errors = np.clip(delta_errors, gcexplain.epsilon(), 1.0)
    delta_errors = gcexplain.stop_gradient(delta_errors)

    return np.mean(gcexplain.kullback_leibler_divergence(error_without_one_feature, error_with_all_features))

  def run(model, data, target, n_splits, epochs, loss, categorical):

    # Split the data into X and y.
    X = data.drop(columns=target)
    y = data[target]
    selected_feature = X.columns

    dfc = pd.DataFrame(columns=['features', 'accuracy', 'loss_x', 'causal_value'])

    # Get the input dimensions for the model.
    input_dim = len(X.columns) -1

    model_config = model.get_config()
    model_config["layers"][0]["config"]["batch_input_shape"] = (None, input_dim)

    model_without_feature = model.__class__.from_config(model_config, custom_objects={})
    model_without_feature.compile(loss = model._compile_config.config['loss'] , optimizer = model._compile_config.config['optimizer'] , metrics = model._compile_config.config['metrics'])


    # Using StratifiedKfold to the the data into chunks.
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    lst_accu_stratified = []
    loss_agg = []
    count = 0

    # For every chunck every feature will be run.
    for train_index, test_index in skf.split(X, y):
      X_arr = np.array(X)
      x_train_fold, x_test_fold = X_arr[train_index], X_arr[test_index]
      print(count)
      count +=1

      if categorical == True:
        y_cat = to_categorical(y)
        y_train_fold, y_test_fold = y_cat[train_index], y_cat[test_index]
      else:
        y_train_fold, y_test_fold = y[train_index], y[test_index]

      model.layers[0]._batch_input_shape = (None, input_dim)

      history = model.fit(x_train_fold, y_train_fold, validation_data=(x_test_fold, y_test_fold), epochs = epochs, verbose=0)

      full = model.predict(x_test_fold)

      for i in selected_feature:
          print(i)
          X_drop = X.drop(columns=[i])
          X_arr2 = np.array(X_drop)
          x_train, x_test = X_arr2[train_index], X_arr2[test_index]

          history = model_without_feature.fit(x_train, y_train_fold, validation_data=(x_test, y_test_fold), epochs = epochs,  verbose=0)
          not_full= model_without_feature.predict(x_test)

          causal = gcexplain.causal_value(y_test_fold.reshape(full.shape), full, not_full, loss)
          di = {'features':i, 'accuracy': history.history['accuracy'][-1], 'loss_x':history.history['loss'], 'causal_value': causal}
          dfc = pd.concat([dfc, pd.DataFrame([di])], ignore_index=True)

    # Creating the output
    dfc = dfc.groupby(['features'])[['accuracy', 'causal_value']].mean().reset_index()
    dfc['causal_value'] = normalize([dfc['causal_value'].to_list()])[0]

    return dfc.reset_index(drop=True)



