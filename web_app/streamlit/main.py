import streamlit as st
import pandas as pd
import numpy as np
import pickle

from category_encoders import OneHotEncoder, OrdinalEncoder
from sklearn.ensemble import RandomForestClassifier
import warnings
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=DataConversionWarning)

st.write("""
# Hanoi Housing Market: Predict **House Price Ranges** Using Classification Technique
Data [Vietnam Housing Dataset (Hanoi)](https://www.kaggle.com/ladcva/vietnam-housing-dataset-hanoi) 
obtained from the [Alo Nhà Đất](https://alonhadat.com.vn) 
that was crawled in August 2020 by [Le Anh Duc](https://www.kaggle.com/ladcva).
""")

st.sidebar.header('User Input Features')

st.sidebar.markdown("""
[Example CSV input file](https://raw.githubusercontent.com/tnathu-ai/COSC2789_Group_Project/main/data/interim/cleaned_data.csv?token=GHSAT0AAAAAABQOFASFFQJ6R55ETCSOLNP2YPF677Q)
""")

# Collects user input features into dataframe
uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    def user_input_features():
        house_type = st.sidebar.selectbox('House_type', ('BYROAD', 'STREET_HOUSE', 'TOWNHOUSE', 'VILLA'))
        legal_documents = st.sidebar.selectbox('Legal_documents', ('AVAILABLE', 'WAITING', 'OTHERS'))
        length = st.sidebar.slider('Length', 32.1, 59.6, 43.9)
        width = st.sidebar.slider('Width', 13.1, 21.5, 17.2)
        area = st.sidebar.slider('Area', 172.0, 231.0, 201.0)
        data = {'House_type': house_type,
                'Length': length,
                'Width': width,
                'Area': area,
                'Legal_documents': legal_documents}
        features = pd.DataFrame(data, index=[0])
        return features


    input_df = user_input_features()

# Combines user input features with entire penguins dataset
# This will be useful for the encoding phase
penguins_raw = pd.read_csv('cleaned_data.csv')
penguins = penguins_raw.drop(columns=['Price_range'])
df = pd.concat([input_df, penguins], axis=0)
# Drop columns
df.drop(columns=['Ward', 'Day_Of_Week', 'Price', 'Street'], inplace=True)
# drop na rows
df = df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)


# ENCODING

# label encoding
# create a function to encoding the value
def to_label_encoder(df, column, category):
    oe = OrdinalEncoder()
    # get the column and encoding it into dataframe
    data = oe.fit_transform(df[[column]])
    # create the dataframe base on data and the value will be integer
    encode_df = pd.DataFrame(data=data, columns=[column], dtype=int)
    # add the encoding dataframe back to the dataframe
    df[column] = encode_df.values


# create a function to encoding the categorical value
def to_one_hot_encoder(df, column_name):
    # we will set the drop to be if_binary so that we can delete an encoded column if that column have a binary
    # categorical value such as true/false, yes/no
    ohe = OneHotEncoder(handle_unknown='error')

    # get the column and encoding it into dataframe
    data = ohe.fit_transform(df[[column_name]])

    # create the dataframe base on data and the value will be integer
    encode_df = pd.DataFrame(data=data, columns=ohe.get_feature_names([column_name]), dtype=int)

    # add the encoding dataframe back to the dataframe
    df.reset_index(inplace=True, drop=True)
    df = pd.concat([df, encode_df], axis=1)

    # remove the original column
    df.drop([column_name], inplace=True, axis=1)

    return df


# df = to_one_hot_encoder(df, 'District')
# df = to_one_hot_encoder(df, 'House_type')
# df = to_one_hot_encoder(df, 'Legal_documents')

encode = ['District', 'House_type', 'Legal_documents']

for col in encode:
    dummy = pd.get_dummies(df[col], prefix=col)
    df = pd.concat([df, dummy], axis=1)
    del df[col]

lst_No = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'GREATER_THAN_10']
to_label_encoder(df, 'No_bedroom', lst_No)
to_label_encoder(df, 'No_floor', lst_No)

df = df[:1]  # Selects only the first row (the user input data)

# Displays the user input features
st.subheader('User Input features')

if uploaded_file is not None:
    st.write(df)
else:
    st.write('Awaiting CSV file to be uploaded. Currently using example input parameters (shown below).')
    st.write(df)

# Reads in saved classification model
load_clf = pickle.load(open('penguins_clf.pkl', 'rb'))

# Apply model to make predictions
prediction = load_clf.predict(df)
prediction_proba = load_clf.predict_proba(df)

st.subheader('Prediction')
penguins_species = np.array(['1-60', '61-70', '71-80', '81-90', '91-100', '101-200', '201-300', '301-1000'])
st.write(penguins_species[prediction])

st.subheader('Prediction Probability')
st.write(prediction_proba)