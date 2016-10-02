"""
This parameter file contains all the tuned parameters for Doc2Vec and BOW with
Gradient Boosting Tree (GBT) and Random Forest (RF)
"""

# common parmeters
test_portion = 0.1  # the portion of the data we want to isolate for testing
drop_middle_thrid = False  # whether we want to drop the middle 1/3 of the data
seed = 1            # seed for shuffling the data


# Frist we specify the name of trained model:
doc2Vec_file = "final_statement_vectors_300_final.csv"
verb_file = "final_BOW_FEATURES_VERB_v5.csv"        # BOW
adv_file = "final_BOW_FEATURES_ADV_v6.csv"          # BOW
adj_file = "final_BOW_FEATURES_ADJ_v3.csv"          # BOW
cons_file = "final_BOW_FEATURES_CONSTRAINTS_v4.csv" # BOW


# the benchmark paramters for both GBT and RF is a 3-quarter-lagged momentum
# strategy
predictors_bm = ['ROE_t-1', 'excess_ROE_t-1', 'ROE_change_t-1',
       'ROE_excess_change_t-1', 'ROE_t-2', 'excess_ROE_t-2',
       'ROE_change_t-2', 'ROE_excess_change_t-2', 'ROE_t-3',
       'excess_ROE_t-3', 'ROE_change_t-3', 'ROE_excess_change_t-3',
       'Label_top', 'Label_bottom', 'is_q1', 'is_q2', 'is_q3', 'is_q4']

# the prediction variable is the signs of the changes of excess ROE on
# top of the SP 500 ROE
y = 'ROE_excess_change_sign'

#############################################
# Belows are the tuned BM parameters
#############################################

GBT_bm_params = {'init': None,
     'learning_rate': 0.026674999999999997,
     'loss': 'deviance',
     'max_depth': 5,
     'max_features': 9,
     'max_leaf_nodes': None,
     'min_samples_leaf': 30,
     'min_samples_split': 1000,
     'min_weight_fraction_leaf': 0.0,
     'n_estimators': 1200,
     'presort': 'auto',
     'random_state': 10,
     'subsample': 0.85,
     'verbose': 0,
     'warm_start': False}


# logistic regression
LM_bm_params = {'C': 0.01,
     'class_weight': None,
     'dual': False,
     'fit_intercept': True,
     'intercept_scaling': 1,
     'max_iter': 100,
     'multi_class': 'ovr',
     'n_jobs': 1,
     'penalty': 'l2',
     'random_state': None,
     'solver': 'liblinear',
     'tol': 0.0001,
     'verbose': 0,
     'warm_start': False}

#############################################
# Belows are the tuned GBT parameters
#############################################

GBT_Doc2Vec_params = {'init': None,
     'learning_rate': 0.026674999999999997,
     'loss': 'deviance',
     'max_depth': 5,
     'max_features': 27,
     'max_leaf_nodes': None,
     'min_samples_leaf': 50,
     'min_samples_split': 1600,
     'min_weight_fraction_leaf': 0.0,
     'n_estimators': 600,
     'presort': 'auto',
     'random_state': 10,
     'subsample': 0.9,
     'verbose': 0,
     'warm_start': False}


GBT_adv_params = {'init': None,
     'learning_rate': 0.026674999999999997,
     'loss': 'deviance',
     'max_depth': 11,
     'max_features': 25,
     'max_leaf_nodes': None,
     'min_samples_leaf': 70,
     'min_samples_split': 1800,
     'min_weight_fraction_leaf': 0.0,
     'n_estimators': 1200,
     'presort': 'auto',
     'random_state': 10,
     'subsample': 0.9,
     'verbose': 0,
     'warm_start': False}


GBT_adj_params = {'init': None,
     'learning_rate': 0.026674999999999997,
     'loss': 'deviance',
     'max_depth': 9,
     'max_features': 23,
     'max_leaf_nodes': None,
     'min_samples_leaf': 30,
     'min_samples_split': 1600,
     'min_weight_fraction_leaf': 0.0,
     'n_estimators': 600,
     'presort': 'auto',
     'random_state': 10,
     'subsample': 0.8,
     'verbose': 0,
     'warm_start': False}


GBT_verb_params = {'init': None,
     'learning_rate': 0.026674999999999997,
     'loss': 'deviance',
     'max_depth': 7,
     'max_features': 25,
     'max_leaf_nodes': None,
     'min_samples_leaf': 60,
     'min_samples_split': 1000,
     'min_weight_fraction_leaf': 0.0,
     'n_estimators': 1600,
     'presort': 'auto',
     'random_state': 10,
     'subsample': 0.9,
     'verbose': 0,
     'warm_start': False}


GBT_cons_params = {'init': None,
     'learning_rate': 0.026674999999999997,
     'loss': 'deviance',
     'max_depth': 11,
     'max_features': 25,
     'max_leaf_nodes': None,
     'min_samples_leaf': 70,
     'min_samples_split': 1600,
     'min_weight_fraction_leaf': 0.0,
     'n_estimators': 2000,
     'presort': 'auto',
     'random_state': 10,
     'subsample': 0.8,
     'verbose': 0,
     'warm_start': False}

#############################################
# Belows are the tuned RF parameters
#############################################


RF_Doc2Vec_params = {'bootstrap': True,
     'class_weight': None,
     'criterion': 'entropy',
     'max_depth': 20,
     'max_features': 90,
     'max_leaf_nodes': None,
     'min_samples_leaf': 30,
     'min_samples_split': 21.344,
     'min_weight_fraction_leaf': 0.0,
     'n_estimators': 150,
     'n_jobs': -1,
     'oob_score': False,
     'random_state': 10,
     'verbose': 0,
     'warm_start': False}


RF_bm_params = {'bootstrap': True,
      'class_weight': None,
      'criterion': 'gini',
      'max_depth': None,
      'max_features': 18,
      'max_leaf_nodes': None,
      'min_samples_leaf': 1,
      'min_samples_split': 2,
      'min_weight_fraction_leaf': 0.0,
      'n_estimators': 100,
      'n_jobs': 1,
      'oob_score': False,
      'random_state': 10,
      'verbose': 0,
      'warm_start': False}



RF_adv_params = {'bootstrap': True,
      'class_weight': None,
      'criterion': 'entropy',
      'max_depth': 20,
      'max_features': 95,
      'max_leaf_nodes': None,
      'min_samples_leaf': 30,
      'min_samples_split': 23.005,
      'min_weight_fraction_leaf': 0.0,
      'n_estimators': 150,
      'n_jobs': -1,
      'oob_score': True,
      'random_state': 10,
      'verbose': 0,
      'warm_start': False}

