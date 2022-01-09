from os import read

import numpy as np
from flask import Flask, request, render_template
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
import pandas as pd
from modelbuilding import logistic, dtree, randomforest, svc, knn

app = Flask(__name__)


# reading the data from csv file
def readdata():
    df = pd.read_csv("cleaned_data.csv")
    # Drop columns
    df.drop(columns=['Area', 'Width', 'Length', 'Ward', 'Day_Of_Week', 'Street', 'Price'], inplace=True)
    df = df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

    return df


# groupby with status col

def getdict(colname):
    df = readdata()
    return dict(df.groupby([colname])['Price_range'].count())


# ENCODING

# label encoding
# create a function to encoding the value
def to_label_encoder(df, column, category):
    oe = OrdinalEncoder(categories=[category])
    # get the column and encoding it into dataframe
    data = oe.fit_transform(df[[column]])
    # create the dataframe base on data and the value will be integer
    encode_df = pd.DataFrame(data=data, columns=[column], dtype=int)
    # add the encoding dataframe back to the dataframe
    df[column] = encode_df.values


# create a function to encoding the categorical value
def to_one_hot_encoder(df, column_name):
    # we will set the drop to be if_binary so that we can delete an encoded column if that column have a binary cateogircal value such as true/false, yes/no
    ohe = OneHotEncoder(sparse=False, handle_unknown='error', drop='if_binary')

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


@app.route("/", methods=["GET", "POST"])
def hello_world():
    df = to_one_hot_encoder(readdata(), 'District')
    df = to_one_hot_encoder(df, 'House_type')
    df = to_one_hot_encoder(df, 'Legal_documents')

    lst_No = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'GREATER_THAN_10']

    to_label_encoder(df, 'No_bedroom', lst_No)
    to_label_encoder(df, 'No_floor', lst_No)

    # lst_Price_range = ['1-60', '61-70', '71-80', '81-90', '91-100', '101-200', '201-300', '301-1000']
    #
    # to_label_encoder(df, 'Price_range', lst_Price_range)
    df = df.reset_index()
    data = df.copy()
    # print(data)
    # data = data.reindex(
    #     columns=['District', 'House_type', 'Legal_documents', 'No_bedroom', 'No_floor', 'Month', 'Price_range'])

    # print(data.info())

    if request.method == "POST":
        mydict = request.form
        District = mydict['District']
        House_type = mydict['House_type']
        Legal_documents = mydict['Legal_documents']
        No_bedroom = mydict['No_bedroom']
        No_floor = mydict['No_floor']
        Month = mydict['Month']
        algo = mydict['algo']

        value = mydict['feature']

        values = ['District',
                  'House_type',
                  'Legal_documents',
                  'No_bedroom',
                  'No_floor',
                  'Month']

        keys = ['District',
                'House_type',
                'Legal_documents',
                'No_bedroom',
                'No_floor',
                'Month',
                'Price_range']

        mapper = dict(zip(keys, values))

        valuecount = getdict(value)

        # Selection of Algorithm

        algomapper = {'rf': randomforest(
            data), 'dt': dtree(data), 'svc': svc(data)}

        classmapper = {0: '1-60', 1: '61-70',
                       2: '71-80', 3: '81-90', 4: '91-100', 5: '101-200', 6: '201-300', 7: '301-1000'}
        algorithm = algomapper[algo]
        accuracy, recall, precision, f1score, model = algorithm

        inputparam = [[District,
                       House_type,
                       Legal_documents,
                       No_bedroom,
                       No_floor,
                       Month]]

        predict = model.predict(inputparam)
        predictedclass = classmapper[predict[0]]

        return render_template('index.html', predictedclass=predictedclass, display=True,
                               accuracy=round(accuracy * 100, 2), precision=precision, showtemplate=True,
                               valuecount=valuecount, value=mapper[value], mapper=valuecount)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
