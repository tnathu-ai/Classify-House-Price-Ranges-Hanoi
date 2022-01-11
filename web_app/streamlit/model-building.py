import pandas as pd
from category_encoders import OrdinalEncoder, OneHotEncoder

df = pd.read_csv('cleaned_data.csv')
# Drop columns
df.drop(columns=['Ward', 'Day_Of_Week', 'Price', 'Street'], inplace=True)
# drop na rows
df = df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

df = df.copy()
target = 'Price_range'


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


encode = ['District', 'House_type', 'Legal_documents']

for col in encode:
    dummy = pd.get_dummies(df[col], prefix=col)
    df = pd.concat([df, dummy], axis=1)
    del df[col]

# df = to_one_hot_encoder(df, 'District')
# df = to_one_hot_encoder(df, 'House_type')
# df = to_one_hot_encoder(df, 'Legal_documents')
lst_No = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'GREATER_THAN_10']
to_label_encoder(df, 'No_bedroom', lst_No)
to_label_encoder(df, 'No_floor', lst_No)

target_mapper = {0: '1-60', 1: '61-70', 2: '71-80', 3: '81-90', 4: '91-100', 5: '101-200', 6: '201-300', 7: '301-1000'}


def target_encode(val):
    return target_mapper[val]


df['Price_range'] = df['Price_range'].apply(target_encode)

# Separating X and y
X = df.drop('Price_range', axis=1)
Y = df['Price_range']

# Build random forest model
from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier()
clf.fit(X, Y)

# Saving the model
import pickle

pickle.dump(clf, open('RandomForestClassifier_clf.pkl', 'wb'))
