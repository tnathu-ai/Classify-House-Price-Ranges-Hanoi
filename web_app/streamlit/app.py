import streamlit as st
import streamlit.components.v1 as stc
from eda_app import run_eda_app
from ml_app import run_ml_app

html_temp = """
		<div style="background-color:pink;padding:10px;border-radius:10px">
		<h1 style="color:black;text-align:center;">House Price Prediction Web App</h1>
		<h4 style="color:black;text-align:center;">Multiclass Classification</h4>
		</div>
		"""


def main():
    stc.html(html_temp)

    menu = ["Home", "EDA", "ML", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Multiclass Classification Problem")
        st.write("""
			### Data Exploration: Analyze House Price in Hanoi
			The aim of the project is to build a machine learning model to predict and classify the sale price ranges of homes based on different explanatory variables describing aspects of residential houses.
			#### Datasource
				- https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data
			#### App Content
				- EDA Section: Exploratory Data Analysis of Data
				- ML Section: ML Predictor App
				""")

    elif choice == "EDA":
        run_eda_app()
    elif choice == "ML":
        run_ml_app()
    else:
        st.subheader("About")
        st.text("Group 10 Project - COSC2789")
        st.text("Practical Data Science")
        st.text("Jan, 2022")


if __name__ == '__main__':
    main()
