import streamlit as st

# Custom imports 
from multipage import MultiPage
import monviso, single_point_mutations# import your pages here

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("__The __*Mo*__deling e__*Nv*__ironment for __*Iso*__forms website__")


# Add all your applications (pages) here
app.add_page("Download single point mutations", single_point_mutations.app)
app.add_page("MoNvIso", monviso.app)
# The main app
app.run()
