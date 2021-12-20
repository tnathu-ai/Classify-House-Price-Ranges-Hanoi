# COSC2789_Group-Project

# Assignment 3: Group Project - COSC2789
Comprehensive data preparation, exploration, visualization, feature engineering, and regression modeling for a case study: 



# Data



# Objective



# Target variable

# Problem Type

# Metric:


# Key Findings:




# Application



## Future improvement:
+ I would like to try out more stacking and ensemble methods to improve the model.

## Productionization

In this step, I built a flask API endpoint that was hosted on a local webserver 

# WORKING ON YOUR LOCAL COMPUTER

python version 3.8.8

1. Install Conda
   by [following these instructions](https://conda.io/projects/conda/en/latest/user-guide/install/index.html). Add Conda
   binaries to your system `PATH`, so you can use the `conda` command on your terminal.

2. Install jupyter lab and jupyter notebook on your terminal

+ `pip install jupyterlab`
+ `pip install jupyter notebook`

### Jupyter Lab

1. Download the 3879312 zipped project folder. Unzip it by double-clicking on it.

2. In the terminal, navigate to the directory containing the project and install these packages and libraries

```
pip install -r requirements.txt
```

3. Enter the newly created directory using `cd directory-name` and start the Jupyter Lab.

```
jupyter lab

```

You can now access Jupyter's web interface by clicking the link that shows up on the terminal or by
visiting http://localhost:8888 on your browser.

4. Click on assignment2.ipynb in the browser tab. This will open up my main file in the Jupyter Lab.

### Note: If the Jupyter Notebook is not responding due to many requests

Error [(The page is not responding)](https://stackoverflow.com/questions/48615535/jupyter-notebook-takes-forever-to-open-and-then-pages-unresponsive-mathjax-i)

I had to restart the notebook; and it did not work. This is because I was printing out too much and the following
scripts resolved the issue by clear out all the output to run through the whole kernal:

1. `conda install -c conda-forge nbstripout` or `pip install nbstripout`

2. `nbstripout filename.ipynb`



## Repository Structure
```
├── dash
│   ├── app.py
│   ├── .gitignore
│   ├── Procfile
│   └── requirements.txt
├── data
│   ├── 
│   └── requirements.txt
├── images
├── README.md
├── interactive_html
│   ├── 
└── cleaning.ipynb
└── encoding.ipynb
└── EDA.ipynb
└── dash_visualization.ipynb
└── function.py
```

