import os
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()


from statsmodels.tsa.seasonal import seasonal_decompose
from pylab import rcParams
rcParams['figure.figsize'] = 12,8

st.beta_set_page_config(page_title='ROC Correlation Tool',page_icon='📈')

def main():

    def set_environ():
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

   
    set_environ()

    st.title("Data Exploration and Correlation Finder Tool")
    st.info("""
            Requirements: To use this tool we need a time-series data set. 
            The dataset must contain a column named 'TimeStamp' (default when exporting from Historian)
            which contains the time stamps of each data sample.  
            The subsequent columns are the variables/tags we need to analyze.
            """)
    st.set_option('deprecation.showfileUploaderEncoding', False)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    file_ = st.file_uploader("Load .csv file")

    def check_nans(df):
        return df.isnull().sum().sum()
         

    if file_:
            
        print(file_);
        chunksize = 5000
        df_chunks = pd.read_csv(file_, index_col=0, parse_dates=True,chunksize=chunksize)
        df = pd.concat(df_chunks, ignore_index=False)
        any_nans = check_nans(df)
         
                                          
        if any_nans > 0:

            df = df.dropna(how='any')
                    
        st.markdown(f"The dataframe below has been loaded (only first 5 rows shown): ")
        st.dataframe(df.head())
        
        columns = list(df.columns)
        st.sidebar.title("Visualize Data")
        st.sidebar.text("This function allows you to plot \na Distribution Graph and Trend and \nit also provides Descriptive Statistics \nof the variable of interest")
        
        variable = st.sidebar.selectbox("Select variable to plot", columns, index=0)
        if st.sidebar.button("Click to plot data:"):
            st.write(df[variable])
            #st.subheader("This df has")
            #columns = list(df.columns)
            #st.write(df)
            st.subheader(f"{variable} Descriptive Statistics")
            st.table(df[variable].describe())

            # Plot Data
            st.header("Data Visualization")
            st.markdown("""Distribution Plot""")
            hist_plot = df[variable]
            plt.hist(hist_plot, bins=20)
            st.pyplot()

            st.markdown("""Line Chart""")
            #value = st.selectbox("Pick a column", columns, index=0)
            df[variable].plot() 
            y_max = (df[variable].max() + (df[variable].max() * 0.1))  
            y_min = (df[variable].min() - (df[variable].min() * 0.1))
            plt.ylim([y_min,y_max]) 
            st.pyplot()
            #st.line_chart(df[columns[1:]])

        # Decompose Trend
        st.sidebar.title("Decompose Data")
        st.sidebar.text("This function performs\nan ETS Decomposition\non a variable which helps see\nunderlying patterns in the data ")
        value = st.sidebar.selectbox('Select a variable', columns, index=0)
        if st.sidebar.button('Decompose'):
            st.subheader(f'{value} decomposed data')
            decomp = seasonal_decompose(df[value], model='add', freq=365)
            decomp.plot()
            st.pyplot() 

        # Find Correlations
        st.sidebar.title("Find Correlations")
        st.sidebar.text("This function calculates\nCorrelation Coeffcients and\nplots a Correlation Matrix")
        if st.sidebar.button("Run Correlation Calc"):
                    
            df_corr = df.corr()
            st.header('Correlation Matrix:')
            # Info about correlations                        
            st.markdown("""### Interpreting Correlations:""")

            st.markdown("""Looking at the correlation matrix below, we will be able to identify which and how strongly the variables are correlated.""")
            st.markdown("""A correlation coefficient of **1** indicates that the variables have a perfect positive relationship """)
            st.markdown("""A correlation coefficient of **0.8** indicates a strong positive correlation""")
            st.markdown("""A correlation coefficient of **0.6** indicates a moderate positive correlation""")
            st.markdown("""A correlation coefficient of **0** indicates no correlation between variables""")
            st.markdown("""Negative coefficients indicate negative relationships""")
            st.markdown("""--------------------------------------------------------------------------------""")
            st.warning("For large datasets, correlation matrix will only display up to 1000 variables")
            
            st.write(df_corr[:500])

            #st.write(df_corr)
            st.markdown("### Highly-correlated pairs")
            st.write(df_corr.unstack().sort_values(ascending=False).drop_duplicates())

            
            #st.write(df_corr.style.background_gradient(cmap='coolwarm'))
        

    else:
        st.warning("Please load a .csv file")

if __name__ == '__main__':
    main()