#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# # Classification Task (Titanic Dataset)

# In[2]:

# In[3]:


def preprocess_dataset(preprocess_df, target_variable):
    
    df = preprocess_df.copy()
    
    column_null_values = {}
    for column in df.columns:
        if(column == target_variable):
            continue
        null_values = df[column].isnull().sum()
        column_null_values[column] = null_values
    # print(column_null_values)
    
    column_rows_to_drop = []
    
    preprocessing_report = {}
    
    preprocessing_report[target_variable] = "Target Variable"
    
    # Dealing with Null Values
    for column, null_values in column_null_values.items():
        if(column == target_variable):
            continue
        if(df[column].isnull().sum() == 0):
            preprocessing_report[column] = "No Null Values Present"
        elif(df[column].isnull().sum() <= 10 and df.shape[0] >= 100):
            column_rows_to_drop.append(column)
            preprocessing_report[column] = "Drop Rows Having Null Values for Column " + column
        elif(df[column].dtype == 'int64' or df[column].dtype == 'float64'):
            df.fillna({column: df[column].median()}, inplace = True)
            preprocessing_report[column] = "Fill Null Values for Column " + column + " to Median Value: " + str(df[column].median())
        elif(df[column].dtype == 'object'):
            df.fillna({column: df[column].mode()[0].split()[0]}, inplace = True)
            preprocessing_report[column] = "Fill Null Values for Column " + column + " to Mode Value: " + str(df[column].mode()[0].split()[0])
    
    df.dropna(subset = column_rows_to_drop, inplace = True)
    
    # Converting Categorical Variables to Numbers
    
    one_hot_encoding_transform = []
    standard_scaler_transform = []
    
    for column in df.columns:
        if(column == target_variable):
            continue
        if(df[column].nunique() <= 7 and df[column].dtype == 'object'):
            one_hot_encoding_transform.append(column)
        elif(df[column].dtype == 'int64' or df[column].dtype == 'float64'):
            standard_scaler_transform.append(column)
    
    # One Hot Encoding Transformation
    
    if(len(one_hot_encoding_transform) >= 1):
        df = pd.get_dummies(df, columns = one_hot_encoding_transform, drop_first = True)
        
    for column in one_hot_encoding_transform:
        preprocessing_report[column] += " + Perform One Hot Encoding for Column " + column
        
    # Standard Scaler Transformation
    
    if(len(standard_scaler_transform) >= 1):
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        df[standard_scaler_transform] = scaler.fit_transform(df[standard_scaler_transform])
        
    for column in standard_scaler_transform:
        preprocessing_report[column] += " + Perform Standard Scaler Transform for Column " + column
    
    print("\n--DATAFRAME PREPROCESSING REPORT--\n")
    
    for column, report in preprocessing_report.items():
        print("Column \"{}\" Report: ".format(column))
        print(report + "\n")
            
    return df
            
    
# result_df = preprocess_dataset(titanic_df, "Survived")
# result_df


# In[4]:


def feature_selection(feature_df, target_variable):
    
    # Important - Handle Feature Selection Better
    
    # Handling only Numerical Features Currently
    
    df = feature_df.copy()
    
    feature_report = {}
    
    final_features = []
    numerical_features = []
    object_features = []
    
    numerical_df = df.select_dtypes(include=['number'])

    corr = numerical_df.corr()
    correlation_with_target = corr[target_variable].abs().sort_values(ascending=False)

    # print(correlation_with_target)
    
    counter = 1

    for title, corr_value in correlation_with_target.items():
        if(counter >= 10):
            break
        if(title != target_variable):
            numerical_features.append(title)
            counter = counter + 1
            feature_report[title] = "Column " + title + " is considered as a Feature"
            col_corr_with_target = df[title].corr(df[target_variable])
            feature_report[title] += " + Correlation of Column " + title + " with Target Variable is " + str(col_corr_with_target)
    
    final_features = numerical_features + object_features
    
    print("\n--DATAFRAME FEATURE SELECTION REPORT--\n")
    
    for column, report in feature_report.items():
        print("Column \"{}\" Report: ".format(column))
        print(report + "\n")
        
    return final_features

# numerical_features = feature_selection(result_df, "Survived")
# print(numerical_features)


# In[5]:


# model_time_taken_result_list = {}


# In[6]:


def model_implementations(model_df, target_variable, features_list):
    
    df = model_df.copy()
    
    # Importing Date Time for Run Time Calculations
    import time
    from datetime import datetime
    
    # Importing our Metrics
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error
    from sklearn.metrics import accuracy_score
    
    # Importing our Models
    from sklearn.linear_model import LinearRegression
    from sklearn.linear_model import LogisticRegression
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    # from sklearn.ensemble import GradientBoostingClassifier
    
    models_list = {}
    
    linear_regression_model = LinearRegression()
    models_list["Linear Regression"] = linear_regression_model
    
    if(model_df[target_variable].nunique() <= 15):
        logistic_regression_model = LogisticRegression(max_iter = 1000)
        models_list["Logistic Regression"] = logistic_regression_model
    
    decision_tree_model = DecisionTreeClassifier()
    models_list["Decision Tree"] = decision_tree_model
    
    random_forest_model = RandomForestClassifier()
    models_list["Random Forest"] = random_forest_model
    
    # gradient_boost_model = GradientBoostingClassifier()
    # models_list["Gradient Boost"] = gradient_boost_model
    
    complete_model_results_list = {}
    complete_model_predictions = {}
    # complete_model_predictions_list = []
    # check_model_names = []
    # complete_model_y_test_values = []
    
    for model_name, model in models_list.items():
        
        # print("\n\n\n\n-----Currently on Model: " + model_name + "-----\n\n\n\n")
        
        model_results_list = []
        model_predictions = []
        # model_y_test_values = []
        
        start_time = time.time()
        
        for i in range(len(features_list)):
            for j in range(i, len(features_list)):
                final_features = []
                for k in range(i, j + 1):
                    if(df[features_list[k]].dtype == 'int64' or df[features_list[k]].dtype == 'float64'):
                        final_features.append(features_list[k])
                
                # print("Features: " + str(final_features))
                    
                X = df[final_features]
                y = df[target_variable]
                
                # print(X.shape, y.shape)
                    
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
                    
                model.fit(X_train, y_train)
                    
                predictions = model.predict(X_test)
                    
                mse_model = mean_squared_error(predictions, y_test)
                
                # model_y_test_values.append(y_test)
                model_results_list.append((final_features, mse_model))
                model_predictions.append(model_predictions)
        
        # end_time = time.time()
        
        # runtime = end_time - start_time
        
        # model_time_taken_result_list[model_name] = runtime
        
        complete_model_results_list[model_name] = model_results_list
        complete_model_predictions[model_name] = model_predictions
        # complete_model_predictions_list.append(model_predictions)
        # check_model_names.append(model_name)
        # complete_model_y_test_values.append(model_y_test_values)
        
    cnt = 0
    
    stacked_models_cnt = 0
    
    # print("\n\n\n\n\nBeginning Stacking of Model\n\n\n\n\n")
    
    stacking_model_start_time = datetime.now()
        
    for first_model_name, first_model in models_list.items():
        cnt = cnt + 1
        print("\n\n\n\n----Current Counter: " + str(cnt) + "----\n\n\n\n")
        for second_model_name, second_model in models_list.items():
            if(first_model_name != second_model_name):
                for third_model_name, third_model in models_list.items():
                    if(first_model_name != third_model_name and second_model_name != third_model_name):
                        start_time = time.time()
                        stacked_models_cnt = stacked_models_cnt + 1
                        stacked_model_name = "Stacking Models " + first_model_name + " and " + second_model_name + " + Using a Meta Model called " + third_model_name
                        stacked_model_results_list = []
                        for i in range(len(features_list)):
                            for j in range(i, len(features_list)):
                                stacked_final_features = []
                                for k in range(i, j + 1):
                                    if(df[features_list[k]].dtype == 'int64' or df[features_list[k]].dtype == 'float64'):
                                        stacked_final_features.append(features_list[k])
                                # print("Model 1: " + first_model_name + "\n" + "Model 2: " + second_model_name + "\n" + "Model 3: " + third_model_name)
                                # print("Features: " + str(stacked_final_features) + "\n")
                                X = df[stacked_final_features]
                                y = df[target_variable]
                                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
                                first_model.fit(X_train, y_train)
                                second_model.fit(X_train, y_train)
                                first_model_predictions = first_model.predict(X_test)
                                second_model_predictions = second_model.predict(X_test)
                                stacked_predictions = np.column_stack((first_model_predictions, second_model_predictions))
                                third_model.fit(stacked_predictions, y_test)
                                final_predictions = third_model.predict(stacked_predictions)
                                mse_stacked_model = mean_squared_error(final_predictions, y_test)
                                stacked_model_results_list.append((stacked_final_features, mse_stacked_model))
                        
                        end_time = time.time()
                        
                        runtime = end_time - start_time
                        
                        # model_time_taken_result_list[stacked_model_name] = runtime
                        
                        complete_model_results_list[stacked_model_name] = stacked_model_results_list
                        
                        
    stacking_model_end_time = datetime.now()
    stacking_model_avg_time = (stacking_model_end_time - stacking_model_start_time) / stacked_models_cnt
    
    
                                
    print("Average Time Taken for Stacked Models To Run with all Possible Permutations of Features: " + str(stacking_model_avg_time))                     
                                
                                
                                 
                        
    
    """
    for i in range(len(complete_model_predictions_list)):
        for j in range(len(complete_model_predictions_list[i])):
            index_map = {}
            for k in range(len(complete_model_predictions_list)):
                if(i != k and (k not in index_map)):
                    index_map[k] = 1
                    stacking_features = np.column_stack(complete_model_predictions_list[i][j], complete_model_prediction_list[k][j])
                    for l in range(len(complete_model_predictions_list)):
                        if(l != i and l != k):
    """
                            
    
                            
    
        
    # print("\n\n\n")
    
    model_names = []

    for model_name, report in complete_model_results_list.items():
        print("Report for Model: " + model_name + "\n")
        print("\n" + str(report) + "\n\n")
        
        model_names.append(model_name)
        
    result_df = pd.DataFrame(columns = model_names)
        
    for model_name, report in complete_model_results_list.items():
        result_df[model_name] = report
        
    return result_df

# final_report_result = model_implementations(result_df, "Survived", numerical_features)


# In[7]:


# model_time_taken_result_list


# In[16]:


def plot_time_result(model_time_taken_dict):
    model_name_list = list(model_time_taken_dict.keys())
    model_name_time_taken = list(model_time_taken_dict.values())
    
    plt.figure(figsize = (100, 60))
    
    plt.bar(model_name_list, model_name_time_taken)
    
    plt.xlabel('Model Name', fontsize = 135)
    plt.ylabel('Model Runtime on all Features Permuation in Seconds', fontsize = 135)
    plt.xticks(rotation = 90)
    
    plt.title("Model Runtime Report", fontsize = 150)
    
    plt.show()
    
# plot_time_result(model_time_taken_result_list)


# In[17]:


# final_report_result


# In[18]:


# final_report_result.shape


# In[29]:


def display_best_result(final_report_result):
    
    import sys
    
    df = final_report_result.copy()
    
    best_results_summary = {}
    best_results_summary_features = []
    best_results_summary_value = []
    
    column_counter = 0
    
    for column_name, column in df.items():
        best_performing_value = sys.maxsize
        best_performing_value_list = []
        for cell in column:
            cell_list, cell_value = cell
            if(cell_value < best_performing_value):
                best_performing_value = cell_value
                best_performing_value_list = cell_list
        
        best_results_summary_features.append(best_performing_value_list)
        best_results_summary_value.append(best_performing_value)
        best_results_summary_key = column_name + " + Features: " + str(best_results_summary_features[column_counter])
        best_results_summary[best_results_summary_key] = best_results_summary_value[column_counter]
        
        column_counter = column_counter + 1
        
    # for best_results_summary_x, best_results_summary_y in best_results_summary.items():
        # print(best_results_summary_x + ": " + str(best_results_summary_y) + "\n")
        
    x_axis_values = list(best_results_summary.keys())
    y_axis_values = list(best_results_summary.values())
    
    plt.figure(figsize = (100, 60))
    plt.bar(x_axis_values, y_axis_values, color = "skyblue")
    plt.xlabel("Models and the Best Features Permutation Used", fontsize = 140)
    plt.ylabel("Best MSE Results", fontsize = 140)
    plt.title("Best MSE Results for Every Model and Features Combination - Regression Task", fontsize = 160)
    plt.xticks(rotation = 90)
    plt.tight_layout()
    plt.show()
    
    return best_results_summary