import streamlit as st
import pandas as pd
import numpy as np
import pickle

from category_encoders import OneHotEncoder, OrdinalEncoder
import warnings
from sklearn.exceptions import DataConversionWarning
from sklearn.metrics import plot_confusion_matrix

warnings.filterwarnings(action='ignore', category=DataConversionWarning)
st.set_option('deprecation.showPyplotGlobalUse', False)



def run_ml_app():
    st.sidebar.header('User Input Features')

    # Collects user input features into dataframe
    def user_input_features():
        house_type = st.sidebar.selectbox('House_type', ('BYROAD', 'STREET_HOUSE', 'TOWNHOUSE', 'VILLA'))
        legal_documents = st.sidebar.selectbox('Legal_documents', ('AVAILABLE', 'WAITING', 'OTHERS'))
        no_floor = st.sidebar.selectbox('No_floor',
                                        ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'GREATER_THAN_10'))
        no_bedroom = st.sidebar.selectbox('No_bedroom',
                                          ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'GREATER_THAN_10'))
        month = st.sidebar.selectbox('Month', ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'))
        day_of_week = st.sidebar.selectbox('Day_of_Week', (
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'))
        district = st.sidebar.selectbox('District', (
            'CẦU GIẤY', 'THANH XUÂN', 'HAI BÀ TRƯNG', 'TÂY HỒ', 'ĐỐNG ĐA', 'HÀ ĐÔNG', 'HUYỆN THANH TRÌ', 'HOÀNG MAI',
            'LONG BIÊN', 'HOÀN KIẾM', 'NAM TỪ LIÊM', 'BA ĐÌNH', 'HUYỆN HOÀI ĐỨC', 'BẮC TỪ LIÊM', 'HUYỆN ĐAN PHƯỢNG',
            'HUYỆN THANH OAI', 'HUYỆN SÓC SƠN'
                               'HUYỆN GIA LÂM', 'HUYỆN CHƯƠNG MỸ', 'HUYỆN ĐÔNG ANH', 'HUYỆN THƯỜNG TÍN',
            'THỊ XÃ SƠN TÂY',
            'HUYỆN MÊ LINH', 'HUYỆN THẠCH THẤT', 'HUYỆN QUỐC OAI',
            'HUYỆN PHÚC THỌ', 'HUYỆN PHÚ XUYÊN', 'HUYỆN BA VÌ', 'HUYỆN MỸ ĐỨC'))

        area = st.sidebar.slider('Area', 1.0, 40.0, 111411.0)
        width = st.sidebar.slider('Width', 1.0, 4.0, 423432.0)
        length = st.sidebar.slider('Length', 1.0, 10.0, 900000.0)
        data = {'House_type': house_type,
                'Length': length,
                'Width': width,
                'Area': area,
                'Legal_documents': legal_documents,
                'No_floor': no_floor,
                'No_bedroom': no_bedroom,
                'Month': month,
                'Day_Of_Week': day_of_week,
                'District': district}
        features = pd.DataFrame(data, index=[0])

    input_df = user_input_features()

    # Combines user input features with entire df dataset
    # This will be useful for the encoding phase
    df_raw = pd.read_csv('data/cleaned_data.csv')

    df_drop_target = df_raw.drop(columns=['Price_range'])
    df = pd.concat([input_df, df_drop_target], axis=0)
    # Drop columns
    df.drop(columns=['Street'], inplace=True)
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
        encode_df = pd.DataFrame(data=data, columns=ohe.get_feature_names(), dtype=int)

        # add the encoding dataframe back to the dataframe
        df.reset_index(inplace=True, drop=True)
        df = pd.concat([df, encode_df], axis=1)

        # remove the original column
        df.drop([column_name], inplace=True, axis=1)

        return df

    encode = ['District', 'House_type', 'Legal_documents', 'Ward', 'Day_Of_Week']

    for col in encode:
        dummy = pd.get_dummies(df[col], prefix=col)
        df = pd.concat([df, dummy], axis=1)
        del df[col]

    lst_No = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'GREATER_THAN_10']
    to_label_encoder(df, 'No_bedroom', lst_No)
    to_label_encoder(df, 'No_floor', lst_No)

    data = df[:1]  # Selects only the first row (the user input data)

    # Displays the user input features
    st.subheader('User Input features')

    st.write('Awaiting CSV file to be uploaded. Currently using example input parameters (shown below).')
    st.write(data)

    # print(df.Price_range.value_counts())
    # Separating X and y
    # X = df.drop('Price_range', axis=1)
    # Y = df_raw['Price_range']
    # # print(Y.value_counts())
    # # Build logistic regression load_clf
    # clf = LogisticRegression()
    # clf.fit(X, Y)
    #
    # # Saving the load_clf
    # import pickle
    #
    # pickle.dump(clf, open('logisticdf.pkl', 'wb'))

    # Reads in saved classification model
    load_clf = pickle.load(open('models/logisticdf.pkl', 'rb'))

    # Apply model to make predictions
    prediction = load_clf.predict(df)
    prediction_proba = load_clf.predict_proba(df)

    class_names = ['1-60', '61-70', '71-80', '81-90', '91-100', '101-200', '201-300', '301-1000']

    st.subheader('Prediction Price Range of your House')
    df_price_ranges = np.array(class_names)
    st.write(df_price_ranges[prediction])

    st.subheader('Prediction Probability for each Price Range')
    st.write(prediction_proba)

    st.subheader("Confusion Matrix")
    plot_confusion_matrix(load_clf, df, prediction)
    st.pyplot()
