import streamlit as st

# Custom imports 
from multipage import MultiPage
import automodeller# import your pages here

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("Main Page")

# Add all your applications (pages) here
app.add_page("Automodeller", automodeller.app)
app.add_page("Download single point mutations", automodeller.app)
# The main app
app.run()
