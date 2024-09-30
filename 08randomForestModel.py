import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import log_loss, brier_score_loss, roc_auc_score, confusion_matrix, mean_squared_error
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import warnings
from joblib import dump, load
uri = "mongodb+srv://xxxxxx:yyyyyy@mongoplayers.xp8lika.mongodb.net/?retryWrites=true&w=majority&appName=MongoPlayers"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['xG']
collection = db['shots']




warnings.simplefilter('ignore')

def randomForestModel(data, fields_to_train, fields_to_encode):
    print("Starting Random Forest Model")
    # Load the dataset
    data['isGoal'].fillna(False, inplace=True)
    # Preprocessing
    label_encoders = {}
    for column in fields_to_encode:
        le = LabelEncoder()
        data[column] = le.fit_transform(data[column])
        label_encoders[column] = le

    # Split the data
    print("Split data")
    print(f"Training data on {fields_to_train}")
    X = data[fields_to_train]
    y = data['isGoal']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    print("Log Loss:", log_loss(y_test, y_pred_proba))
    print("Brier Score:", brier_score_loss(y_test, y_pred_proba))
    print("ROC-AUC Score:", roc_auc_score(y_test, y_pred_proba))
    print("RMSE Score:", mean_squared_error(y_test, y_pred_proba) )

    #produce a ROC curve
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic - Random Forest')
    plt.legend(loc="lower right")
    plt.show()

    # Display confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d')
    plt.title('Confusion Matrix - Random Forest')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

    dump(model, 'rf_model.joblib')
    dump(label_encoders, 'rf_label_encoders.joblib')

# Function for single shot prediction
def predict_single_shot(model, label_encoders, shot_data, encoded_columns):

    for column in encoded_columns:
        shot_data[column] = label_encoders[column].transform([shot_data[column]])[0]
    shot_df = pd.DataFrame([shot_data])
    proba = model.predict_proba(shot_df)[:, 1]
    return proba[0]


def retrieveShots(collection, query):

    match_records = list(collection.find(query))
    print(f'{query} : {len(match_records)}')
    df = pd.DataFrame(match_records)
    return df


def estimateXG(collection, query, fields_to_encode):

    df = retrieveShots(collection, query)
    df = df[['dist', 'bodyPart', 'x', 'prevEventType', 'penalty', 'angle', 'bigChance', 'isGoal']]
    df['xG'] = 0
    encoded_columns= fields_to_encode
    model = load('rf_model.joblib')
    label_encoders = load('rf_label_encoders.joblib')

    for index, row in df.iterrows():
        single_shot_data = {
            'x': row['x'],
            'dist': row['dist'],
            'angle': row['angle'],
            'prevEventType': row['prevEventType'],
            'bodyPart': row['bodyPart']
        }
        xG = predict_single_shot(model, label_encoders, single_shot_data, encoded_columns)
        df['xG'].at[index] = xG

    print(df)

    totalXG = df['xG'].sum()
    trueGoals = df[df['isGoal'] == True].shape[0]

    print(f'xG : {totalXG}, Goals : {trueGoals}')

# Set query and fields to use in the model
# query = {'league':{'$nin':['WSL', 'League One']}}
query = {'league':{'$nin':['WSL']}}
fields_to_train = ['x', 'dist', 'angle', 'prevEventType', 'bodyPart']
fields_to_encode = ['prevEventType', 'bodyPart']

# retrieve data from MongoDB
df = retrieveShots(collection, query)

# submit data to create model
randomForestModel(df, fields_to_train, fields_to_encode)
