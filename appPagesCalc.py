import streamlit as st
import os

#Define the pages
mainPage = st.Page("mainCalc.py", title="Página inicial", icon="🎈")
page_2 = st.Page("calDaysCurrent.py", title="Cálculo de dias corridos", icon="📑")
page_3 = st.Page("calDaysUseful.py", title="Cálculo de dias úteis", icon="📙")

# Set up navigation
pg = st.navigation([mainPage, page_2, page_3])

# Run the selected page
pg.run()
