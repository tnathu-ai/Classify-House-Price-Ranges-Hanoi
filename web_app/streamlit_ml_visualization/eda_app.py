import streamlit as st
import pandas as pd

# Data Viz Pkgs
import matplotlib.pyplot as plt
import matplotlib
from pandas import read_csv

matplotlib.use('Agg')
import seaborn as sns
import plotly.express as px


@st.cache
def load_data(data):
    df = pd.read_csv(data)
    return df


def run_eda_app():
    st.subheader("EDA Section")
    # df = load_data("data/diabetes_data_upload.csv")
    df = load_data("data/cleaned_data.csv")
    # df = load_data("data/freqdist_of_age_data.csv")

    submenu = st.sidebar.selectbox("SubMenu", ["Descriptive", "Plots"])
    if submenu == "Descriptive":

        st.dataframe(df)

        # with st.expander("Data Types Summary"):
        #     st.dataframe(df.dtypes)

        with st.expander("Descriptive Summary"):
            st.dataframe(df.describe())

        with st.expander("House_type Distribution"):
            st.dataframe(df['House_type'].value_counts())

        with st.expander("Price_range Distribution"):
            st.dataframe(df['Price_range'].value_counts())
    else:
        st.subheader("Plots")

        # Layouts
        col1, col2 = st.columns([2, 1])
        with col1:
            with st.expander("Dist Plot of House_type"):
                # fig = plt.figure()
                # sns.countplot(df['House_type'])
                # st.pyplot(fig)

                gen_df = df['House_type'].value_counts().to_frame()
                gen_df = gen_df.reset_index()
                gen_df.columns = ['House_type Type', 'Counts']
                # st.dataframe(gen_df)
                p01 = px.pie(gen_df, names='House_type Type', values='Counts')
                st.plotly_chart(p01, use_container_width=True)

            with st.expander("Dist Plot of Price_range"):
                fig = plt.figure()
                sns.countplot(df['Price_range'])
                st.pyplot(fig)

        with col2:
            with st.expander("House_type Distribution"):
                st.dataframe(df['House_type'].value_counts())

            with st.expander("Price_range Distribution"):
                st.dataframe(df['Price_range'].value_counts())

        with st.expander("Correlation Plot"):
            corr_matrix = df.corr()
            fig = plt.figure(figsize=(20, 10))
            sns.heatmap(corr_matrix, annot=True)
            st.pyplot(fig)

            p3 = px.imshow(corr_matrix)
            st.plotly_chart(p3)
