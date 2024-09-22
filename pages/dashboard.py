import streamlit as st
import time
import pandas as pd
import numpy as np

st.set_page_config(page_title="Dashboard", page_icon="📈")

st.markdown("# Dashboards")

st.write(
    """This demo illustrates a combination of plotting and analysis that have been done in Observables and others as part of mimilabs.ai powerful dataset in Databricks. Enjoy!"""
)

st.markdown("## Most Prescribed Drug from 2020 - 2024")
new_data = pd.read_csv("/Users/gisseldiaz/Desktop/Gi Projects/gi_chatbot/most_prescribed_drug_20to24_2024_05_16.csv")


st.bar_chart(new_data, x="gnrc_name", y="total_claims", x_label="Generic Drug Name", y_label="Total Claims per Drug")