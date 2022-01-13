instructions


+ JUPYTER LAB

1. Download the COSC2789_Group_Project zipped project folder. Unzip it by double-clicking on it.

2. In the terminal, navigate to the directory containing the project and install these packages and libraries

```
pip install -r requirements.txt
```

3. Enter the newly created directory using `cd COSC2789_Group_Project/notebooks/` and start the Jupyter Lab.

```
jupyter lab
```

You can now access Jupyter's web interface by clicking the link that shows up on the terminal or by
visiting http://localhost:8888 on your browser.

4. Click on Assignment3.ipynb in the browser tab. This will open up my main file in the Jupyter Lab.



+  DASH

1. In the terminal, navigate to the directory containing the dash using `cd ./web_app/dash`

2. Start the dash local host by writing the following command line:

```
python app.py
```

3. You can now access Dash's web interface by clicking the link that shows up on the terminal or by visiting http://127.0.0.1:8050/ on your browser.

4. In case you want to have a new dataset, you need to input it into the assignment3.ipynb and run all the cells

5. After running the notebook, there will be an update csv file call `cleaned_data.csv` in Dash folder

6. You can repeat step 1



+ STREAMLIT machine learning visualization and prediction deployment

1. In teh terminal, navigate to the directory containing the streamlit using `cd ./web_app/streamlit`

2. Start the streamlit local host by writing the following command line:

```
streamlit run app.py
```

3. You can now access Streamlit's web interface by clicking the link that shows up on the terminal or by visiting http://localhost:8501 or it will automatically pop up the website on your browser.

4. In case you want to have a new dataset, you need to input it into the assignment3.ipynb and run all the cells

5. After running the notebook, there will be an update csv file call `cleaned_data.csv` in data folder

6. You can repeat step 1


python version 3.8.8
OS : windows