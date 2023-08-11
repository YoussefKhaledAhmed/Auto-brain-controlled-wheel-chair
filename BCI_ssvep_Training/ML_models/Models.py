from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import numpy as np
import pickle


import matplotlib.pyplot as plt
# from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


class ML_models:
    def Train_without_tuning(self , x_train , y_train , x_test , y_test , path , name , models_names:list = ["logistic" , "SVC" , "DT" , "RF"]):
        models = []
        for i in models_names:
            if i == "logistic":
                models.append(OneVsRestClassifier(LogisticRegression()))
            elif i == "SVC":
                models.append(OneVsRestClassifier(SVC()))
            elif i == "DT":
                models.append(DecisionTreeClassifier())
            else:
                models.append(RandomForestClassifier())
        print("this before tuning the models using GridSearchCV:\n")
        for model in models:
            model.fit(x_train, y_train)
            train_score = model.score(x_train, y_train)
            valid_score = model.score(x_test, y_test)
            if model.__class__.__name__ == "OneVsRestClassifier":
                print(f"Class {model.estimator.__class__.__name__}:")
            else:
                print(f"Class {model.__class__.__name__}:")
            print(f"    train: {train_score}\n    valid: {valid_score}\n")

        self.save_MLModel(model , path=path , name= name)

# Logistic regression
    # Train
    def train_LogisticRegression_with_GridSearchCV(self , x_train , y_train, path , userName):
        param_grid = {
            'C': [10, 100, 1000],
            'penalty': ['l2'],
            'solver': ['liblinear'],
            'max_iter': [1000, 10000]
        }

        model = LogisticRegression()
        LogisticRegression_grid_search = GridSearchCV(model, param_grid, cv=5, return_train_score=True)
        LogisticRegression_grid_search.fit(x_train, y_train)

        # Get the best parameters found by GridSearchCV
        best_params = LogisticRegression_grid_search.best_params_

        # Create a DecisionTreeClassifier object with the best parameters
        best_model = LogisticRegression(**best_params)

        # Fit the best model to the training data
        best_model.fit(x_train, y_train)

        self.save_MLModel(best_model, path=path, name="LogisticRegression_" + userName)
        return best_model

    #expect
    def expect_LogisticRegression_with_GridSearchCV(self , x ,path , userName):
        model = self.load_MLModel(path , "LogisticRegression_" + userName)
        predictions = model.predict(x)
        print("predictions\n",predictions)
        # Get the predicted class labels
        predicted_class_labels_index = np.argmax(predictions, axis=0)
        true_labels = [7.5 , 8.57 , 10 , 12]
        return true_labels[predictions[predicted_class_labels_index]]

# SVC
    #Train
    def train_SVC_with_GridSearchCV(self ,  x_train , y_train , path , userName):
        param_grid = {'C': [.001, .002, .003, .01, .1, 1, 2, 3, 4, 5, 6, 7, 8, 10, 100, 1000],
                       'gamma': [1e-1, 1e-2, 1e-3, 1e-4],
                       'kernel': ['poly'],
                       'degree': [1, 2, 3]
                       }

        model = SVC()
        SVC_grid_search = GridSearchCV(model, param_grid, cv=5, return_train_score=True)
        SVC_grid_search.fit(x_train, y_train)

        # Get the best parameters found by GridSearchCV
        best_params = SVC_grid_search.best_params_

        # Create a DecisionTreeClassifier object with the best parameters
        best_model = SVC(**best_params)

        # Fit the best model to the training data
        best_model.fit(x_train, y_train)

        self.save_MLModel(best_model , path = path , name = "SVC_" + userName)

        return best_model

    #expect
    def expect_SVC_with_GridSearchCV(self , x ,path , userName):
        model = self.load_MLModel(path , "SVC_" + userName)
        predictions = model.predict(x)
        # Get the predicted class labels
        predicted_class_labels = np.argmax(predictions, axis=0)
        return predicted_class_labels

# Random Forest
    #Train
    def train_RandomForest_with_GridSearchCV(self , x_train , y_train , path , userName):
        param_grid = {
            'max_depth': [50, 80],
            'max_features': [2, 3, 5],
            'min_samples_leaf': [2, 5],
            'min_samples_split': [8, 12],
            'n_estimators': [100, 300]
        }

        model = RandomForestClassifier()

        RF_grid_search = GridSearchCV(model, param_grid, cv=5, return_train_score=True)
        RF_grid_search.fit(x_train, y_train)

        # Get the best parameters found by GridSearchCV
        best_params = RF_grid_search.best_params_

        # Create a DecisionTreeClassifier object with the best parameters
        best_model = RandomForestClassifier(**best_params)

        # Fit the best model to the training data
        best_model.fit(x_train, y_train)

        self.save_MLModel(best_model , path = path , name = "RF_" + userName)

        return best_model

    #expect
    def expect_RF_with_GridSearchCV(self , x ,path , userName):
        model = self.load_MLModel(path , "RF_" + userName)
        predictions = model.predict(x)
        # Get the predicted class labels
        predicted_class_labels = np.argmax(predictions, axis=1)
        return predicted_class_labels

# Decision Tree
    #Train
    def train_DecisionTree_with_GridSearchCV(self ,  x_train , y_train , path , userName):
        param_grid = {
            "max_depth": [1, 5, 10, 20, 30, 40, 50],
            "min_samples_leaf": [1, 2, 3, 5, 10, 20, 30, 40],
            "max_leaf_nodes": [2, 10, 20, 30, 40, 50, 60]
        }

        model = DecisionTreeClassifier()
        DecisionTree_grid_search = GridSearchCV(model, param_grid, cv=5, return_train_score=True)
        DecisionTree_grid_search.fit(x_train, y_train)

        # Get the best parameters found by GridSearchCV
        best_params = DecisionTree_grid_search.best_params_

        # Create a DecisionTreeClassifier object with the best parameters
        best_model = DecisionTreeClassifier(**best_params)

        # Fit the best model to the training data
        best_model.fit(x_train, y_train)

        self.save_MLModel(best_model , path=path, name="DecisionTree_" + userName)

        return best_model

    #expect
    def expect_DecisionTree_with_GridSearchCV(self , x ,path , userName):
        model = self.load_MLModel(path , "DecisionTree_" + userName)
        predictions = model.predict(x)
        # Get the predicted class labels
        predicted_class_labels = np.argmax(predictions, axis=1)
        return predicted_class_labels

    def train_XGBoost_with_GridSearchCV(self ,  x_train , y_train , userName):
        param_grid = {
            'n_estimators': [100, 1000, 10000],
            'learning_rate': [0.01, 0.001, 0.0001],
            'max_depth': [3, 6, 9],
            'min_child_weight': [1, 3, 5],
            'gamma': [0, 0.01, 0.1],
            'subsample': [0.7, 0.8, 0.9],
            'colsample_bytree': [0.7, 0.8, 0.9],
            'objective': ['binary:logistic'],
            'eval_metric': ['accuracy'],
            'n_jobs': -1
        }
        raise Exception("not completely implemented yet")

    def train_PipleLineSVM_with_GridSearchCV(self ,  x_train , y_train , userName):
        raise Exception("not completely implemented yet")

    @staticmethod
    def save_MLModel(model , path , name):
        pickle.dump(model, open(path + name + ".sav", 'wb'))

    @staticmethod
    def load_MLModel(path , name):
        return pickle.load(open(path + name + ".sav", 'rb'))

def ConfusionMatrix(model , x_test , y_test):
    class_names = ["7.5", "8.57", "10", "12"]
    # Plot non-normalized confusion matrix
    titles_options = [("Confusion matrix, without normalization", None),
                      ("Normalized confusion matrix", 'true')]
    for title, normalize in titles_options:
        disp = plot_confusion_matrix(model, x_test, y_test,
                                     display_labels=class_names,
                                     cmap=plt.cm.Blues,
                                     normalize=normalize)
        disp.ax_.set_title(title)

        print(title)
        print(disp.confusion_matrix)

    plt.show()

    y_pred = model.predict(x_test)

    # Finding precision and recall
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy   :", accuracy)
    precision = precision_score(y_test, y_pred, average='macro')
    print("Precision :", precision)
    recall = recall_score(y_test, y_pred, average='macro')
    print("Recall    :", recall)
    F1_score = f1_score(y_test, y_pred, average='macro')
    print("F1-score  :", F1_score)
