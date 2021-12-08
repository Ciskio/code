import streamlit as st

# Custom imports 
from multipage import MultiPage
import monviso, single_point_mutations# import your pages here

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("The __Mo__deling e**Nv**ironment for **Iso**forms website")


# Add all your applications (pages) here
app.add_page("Download single point mutations", single_point_mutations.app)
app.add_page("MoNvIso", monviso.app)
# The main app
app.run()
