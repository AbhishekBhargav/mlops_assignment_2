# Required Libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
#import autosklearn.classification
from sklearn.model_selection import train_test_split
#from sklearn.metrics import accuracy_score, classification_reportp

# Load Dataset (Example: Titanic Dataset from Kaggle)
data = pd.read_csv("C:\\Users\\Deepak J Bhat\\Downloads\\train.csv")

#Data Preprocessing
# Handle missing values
numerical_features = ['Age', 'Fare']
categorical_features = ['Sex', 'Embarked']  

# Numerical Preprocessing Pipeline
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())])

# Categorical Preprocessing Pipeline
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

# Combine Both Preprocessing Pipelines
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)])


#This script performs:
#Missing value imputation using SimpleImputer
#Scaling numeric features using StandardScaler
#Encoding categorical variables using OneHotEncoder
# Apply Preprocessing
X = data.drop('Survived', axis=1)  # Replace 'Target' with your actual target column
y = data['Survived']
print(X.shape)
# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("training completed successfully")
print(X_train.shape)
# Fit and transform the training data
X_train = preprocessor.fit_transform(X_train)
X_test = preprocessor.transform(X_test)
print(f'Shape of X_test: {X_test.shape}')
print(f'Shape of y_test: {X_train.shape}')
'''
import shap
import h2o
from h2o.automl import H2OAutoML
h2o.init()
# Convert numpy arrays to pandas DataFrames
X_train_df = pd.DataFrame(X_train, columns=[f'feature_{i}' for i in range(X_train.shape[1])])
y_train_df = pd.Series(y_train, name='Survived')

X_test_df = pd.DataFrame(X_test, columns=[f'feature_{i}' for i in range(X_test.shape[1])])
y_test_df = pd.Series(y_test, name='Survived')
print(len(y_test_df))
print(len(X_test_df))
# Concatenate X and y for training and testing
train_df = pd.concat([X_train_df, y_train_df], axis=1)
# Convert pandas DataFrames to H2OFrames
train_h2o = h2o.H2OFrame(train_df)
test_h2o = h2o.H2OFrame(X_test_df)
print(len(test_h2o))
# Set the response column (target) as the target
response_column = 'Survived'
train_h2o[response_column] = train_h2o[response_column].asfactor()
#test_h2o[response_column] = test_h2o[response_column].asfactor()

# Initialize H2O AutoML
aml = H2OAutoML(
    max_runtime_secs=60,  # Total time for AutoML (6 minutes)
    seed=42
)

# Train AutoML
aml.train(y=response_column, training_frame=train_h2o)

# Predict on the test set
y_pred_h2o = aml.predict(test_h2o)
print(len(y_pred_h2o))
y_pred_df = y_pred_h2o.as_data_frame()  # Convert to pandas DataFrame for compatibility
y_pred=y_pred_df.iloc[:, 0].values
print(len(y_pred))
# Ensure the length of y_pred matches y_test
#if len(y_pred) != len(y_test):
    #raise ValueError(f"Length of predictions ({len(y_pred)}) does not match length of true values ({len(y_test)})")

# Calculate accuracy and display classification report
accuracy = accuracy_score(y_test, y_pred)
print(f'H2O AutoML Best Model Accuracy: {accuracy}')
print('Classification Report:')
print(classification_report(y_test, y_pred))


# Display the best model found by H2O AutoML
print("\nH2O AutoML Best Model:")
print(aml.leader)

# Convert the best model to an SHAP explainer
best_model = aml.leader
explainer = shap.Explainer(best_model)

# Get SHAP values for the test set
shap_values = explainer(test_h2o)

# Visualize the SHAP values
shap.summary_plot(shap_values, X_test_df)

'''
# Ensure that X_test is a DataFrame with proper feature names
if isinstance(X_test, np.ndarray):
    X_test = pd.DataFrame(X_test, columns=[f'feature_{i}' for i in range(X_test.shape[1])])

import shap
import matplotlib.pyplot as plt
from tpot import TPOTClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Assuming you already have X_train, X_test, y_train, y_test

# Initialize TPOT classifier
tpot = TPOTClassifier(
    generations=2,  # Number of generations to run
    population_size=20,  # Number of pipelines to test in each generation
    verbosity=2,  # Level of verbosity (2 shows more details)
    random_state=42
)

# Train TPOT
tpot.fit(X_train, y_train)
tpot.export('tpot_best_model.py')
# Predict on the test set
y_pred = tpot.predict(X_test)

# Calculate accuracy and display classification report
accuracy = accuracy_score(y_test, y_pred)
print(f'TPOT Best Model Accuracy: {accuracy}')
print('Classification Report:')
print(classification_report(y_test, y_pred))

# To display the best pipeline found by TPOT
print("\nTPOT Best Pipeline:")
print(tpot.fitted_pipeline_)

# Display all non-dominated pipelines tried by TPOT
print("\nAll Non-Dominated Pipelines Tried by TPOT:")
for pipeline in tpot.pareto_front_fitted_pipelines_.keys():
    print(f'Pipeline: {pipeline}')

# ==================================
# SHAP EXPLANATIONS
# ==================================

import lime
import lime.lime_tabular
import matplotlib.pyplot as plt
print(X_train.shape[1])
# Initialize the LIME explainer
class_names=['Not Survived','Survived']
explainer = lime.lime_tabular.LimeTabularExplainer(
    X_train,  # Pass X_train as NumPy array
    feature_names=[f'feature_{i}' for i in range(X_train.shape[1])],  # Give custom feature names
    class_names=['Not Survived','Survived'],  # Modify based on your class names
    mode='classification'
)
'''
# Choose an instance to explain (e.g., the first row in X_test)
i = 0  # You can change this to any instance in the test set
exp = explainer.explain_instance(
    X_test.iloc[i].values,     # The data instance to explain
    tpot.predict_proba,    # The model’s prediction probabilities
    num_features=11            # The number of features to show in the explanation
)
'''
# Get explanation for a specific instance
i = 0  # index of the instance to explain
instance =  X_test.iloc[i].values
# Generate explanations for all classes
for i in range(len(class_names)):
    exp = explainer.explain_instance(instance, tpot.predict_proba, num_features=10, top_labels=len(class_names))
    fig = exp.as_pyplot_figure(label=i)
    plt.title(f'Local explanation for class {class_names[i]}')
    plt.show()
# Print and visualize the explanation
#exp.show_in_notebook(show_all=True)
#exp.as_pyplot_figure()
#plt.show()