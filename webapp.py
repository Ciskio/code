import streamlit as stl
import os
import subprocess

# save the file in the directory where  the app is running.
def save_file(infile):
    with open(infile.name, "wb") as f:
        f.write(infile.getbuffer())

def start_desktop():
    cmdmod = "/opt/TurboVNC/bin/vncserver &" # starts the vncdesktop
    test = subprocess.run(cmdmod, shell=True, universal_newlines=True, check=True)

def check_mistakes(parameter_value, parameter_name):
  float_parameters = ["res", "seqid", "eva"]
  if parameter_value == "":
    stl.error("Please enter a valid input")
  elif type(parameter_value) == str and parameter_name in float_parameters:
    try:
      parameter_value = float(parameter_value)
    except:
      stl.error("Please enter a valid input")

  elif type(parameter_value) == str and parameter_name not in float_parameters:
    try:
      parameter_value = int(parameter_value)
    except:
      stl.error("Please enter a valid input")


# title

stl.title("Automodeling Software")

# drag and drop the mutation file
input_file = stl.file_uploader("Drag your input file here")

col1, col2 = stl.columns(2) # make 2 columns for input parameters
# parameters = stl.form(key='INPUT PARAMETERS')
with stl.form(key='parameters'):
  with col1:
      res = stl.text_input(label='Max acceptable resolution for templates')
      check_mistakes(res, "res")
      seqid = stl.text_input(label='Sequence identity threshold')
      check_mistakes(seqid, "seqid")
      hmm_2_import = stl.text_input(label='HMM to import')
      check_mistakes(hmm_2_import, "hmm_2_import)")
      pdb_2_use = stl.text_input(label='MAX number of templates to download')
      check_mistakes(pdb_2_use, "pdb_2_use")
  with col2:
      eva = stl.text_input(label='E val')
      check_mistakes(eva, "eva")
      number_of_wt_models = stl.text_input(label='Number of WT model to generate')
      check_mistakes(number_of_wt_models, "number_of_wt_models")
      number_of_mut_models = stl.text_input(label='Number of MUTANTS model to generate')
      check_mistakes(number_of_mut_models, "number_of_mut_models")
  stl.form_submit_button()

if input_file is not None:
  save_file(input_file)
#    start_desktop()
