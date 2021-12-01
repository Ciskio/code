import streamlit as st
import os
import subprocess
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request
import urllib.request
import re
import time
from threading import Thread
import zipfile
# generate link to download
import base64
# send email
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# save the file in the directory where  the app is running.
def save_file(infile):
    with open(infile.name, "wb") as f:
        f.write(infile.getbuffer())

def start_desktop():
    cmdmod = "/opt/TurboVNC/bin/vncserver &" # starts the vncdesktop
    test = subprocess.run(cmdmod, shell=True, universal_newlines=True, check=True)
 
def connect_to_altair():
    cmdmod = "./connect_altair.sh" # connect to altair
    test = subprocess.run(cmdmod, shell=True, universal_newlines=True, check=True)
    with open("test.txt","w") as f:
        f.write("we'r in")


def check_mistakes(parameter_value, parameter_name):
  float_parameters = ["res", "seqid", "eva"]
  safe = 0
  if parameter_value == "":
    st.error("Please enter a valid input")
    safe = 1
  elif type(parameter_value) == str and parameter_name in float_parameters:
    try:
      parameter_value = float(parameter_value)
    except:
      st.error("Please enter a valid input")
      safe = 1
  elif type(parameter_value) == str and parameter_name not in float_parameters:
    try:
      parameter_value = int(parameter_value)
    except:
      st.error("Please enter a valid input")
      safe = 1
  return safe

def write_parameters_file(parameters_dict):
  with open("parameters.dat","w") as f:
    f.write("DB_LOCATION=/home/foliva/Desktop/Algoritmo_testing/Algoritmo/Algoritmo_fresh/\n\n")
    f.write("PYMODHOME=/home/foliva/miniconda/envs/pymod3/lib/python3.7/site-packages/pmg_tk/startup/pymod3/pymod_lib/pymod_main/\n\n")
    f.write("RESOLUTION=" + str(parameters_dict["res"]) + "\n\n")
    f.write("SEQID=" + str(parameters_dict["seqid"]))
    f.write("HMM_TO_IMPORT=" + str(parameters_dict["hmm_2_import"]) + "\n\n")
    f.write("PDB_TO_USE=" + str(parameters_dict["pdb_2_use"]) + "\n\n")
    f.write("E_VAL=" + str(parameters_dict["eva"]) + "\n\n")
    f.write("NUM_OF_MOD_WT=" + str(parameters_dict["number_of_wt_models"]) + "\n\n")
    f.write("NUM_OF_MOD_mut=" + str(parameters_dict["number_of_mut_models"]))

# title
def app():
  st.title("Automodeling Software")

  # drag and drop the mutation file
  input_file = st.file_uploader("Drag your input file here")

  col1, col2 = st.columns(2) # make 2 columns for input parameters
  # parameters = st.form(key='INPUT PARAMETERS')
  safe = []
  with st.form(key='parameters'):
    submit_parameters = st.form_submit_button()
    with col1:
        res = st.text_input(label='Max acceptable resolution for templates', value="4.5", help="test")
        if submit_parameters:
          safe.append(check_mistakes(res, "res"))
        seqid = st.text_input(label='Sequence identity threshold', value="25")
        if submit_parameters:
          safe.append(check_mistakes(seqid, "seqid"))
        hmm_2_import = st.text_input(label='HMM to import', value="100")
        if submit_parameters:
          safe.append(check_mistakes(hmm_2_import, "hmm_2_import)"))
        pdb_2_use = st.text_input(label='MAX number of templates to download', value="10")
        if submit_parameters:
          safe.append(check_mistakes(pdb_2_use, "pdb_2_use"))
    with col2:
        eva = st.text_input(label='E val', value="0.001")
        if submit_parameters:
          safe.append(check_mistakes(eva, "eva"))
        number_of_wt_models = st.text_input(label='Number of WT model to generate', value="50")
        if submit_parameters:
          safe.append(check_mistakes(number_of_wt_models, "number_of_wt_models"))
        number_of_mut_models = st.text_input(label='Number of MUTANTS model to generate', value="25")
        if submit_parameters:
          safe.append(check_mistakes(number_of_mut_models, "number_of_mut_models"))

  if submit_parameters:
    if np.sum(safe) == 0:
      parameters_dict = { "res": res,
                          "seqid": seqid,
                          "hmm_2_import": hmm_2_import,
                          "pdb_2_use": pdb_2_use,
                          "eva": eva,
                          "number_of_wt_models": number_of_wt_models,
                          "number_of_mut_models": number_of_mut_models}
      write_parameters_file(parameters_dict)

  if input_file is not None:
    save_file(input_file)
    connect_to_altair()
    
  #    start_desktop()

