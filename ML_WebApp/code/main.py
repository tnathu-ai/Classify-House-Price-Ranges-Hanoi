from os import read
from flask import Flask, request, render_template
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pandas as pd
from modelbuilding import logistic, dtree, randomforest, svc, knn

app = Flask(__name__)


# reading the data from csv file
def readdata():
    df = pd.read_csv("cleaned_data.csv")
    # Drop columns
    df.drop(columns=['Area', 'Width', 'Length'], inplace=True)

    return df


# groupby with status col

def getdict(colname):
    df = readdata()
    return dict(df.groupby([colname])['Price_range'].count())


# ENCODING

# label encoding
def labelencoding(df):
    encoder = LabelEncoder()
    data = df.copy()
    getmappings = {}
    # select non-numeric columns
    data_string = data.select_dtypes(include='string')
    for col in data_string.columns.to_list():
        data[col] = encoder.fit_transform(data[col])

        # get the mappings of the encoded dataframe
        getmappings[col] = dict(zip(encoder.classes_, encoder.transform(encoder.classes_)))
    print(data.columns.to_list())

    return getmappings, data


@app.route("/", methods=["GET", "POST"])
def hello_world():
    getmappings, data = labelencoding(readdata())

    if request.method == "POST":
        mydict = request.form
        District = mydict['District']
        House_type = mydict['House_type']
        Legal_documents = mydict['Legal_documents']
        No_bedroom = mydict['No_bedroom']
        No_bedroom = mydict['No_floor']
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

        classmapper = {0: 'Accurate', 1: 'Good',
                       2: 'Unaccurate', 3: 'VeryGood'}
        algorithm = algomapper[algo]
        accuracy, recall, precision, f1score, model = algorithm

        inputparam = [['District',
                       'House_type',
                       'Legal_documents',
                       'No_bedroom',
                       'No_floor',
                       'Month']]

        predict = model.predict(inputparam)
        predictedclass = classmapper[predict[0]]

        return render_template('index.html', predictedclass=predictedclass, display=True,
                               accuracy=round(accuracy * 100, 2), precision=precision, showtemplate=True,
                               valuecount=valuecount, value=mapper[value], mapper=valuecount)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
