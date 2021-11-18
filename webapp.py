import streamlit as stl
import os
import subprocess
import numpy as np

# save the file in the directory where  the app is running.
def save_file(infile):
    with open(infile.name, "wb") as f:
        f.write(infile.getbuffer())

def start_desktop():
    cmdmod = "/opt/TurboVNC/bin/vncserver &" # starts the vncdesktop
    test = subprocess.run(cmdmod, shell=True, universal_newlines=True, check=True)

def check_mistakes(parameter_value, parameter_name):
  float_parameters = ["res", "seqid", "eva"]
  safe = 0
  if parameter_value == "":
    stl.error("Please enter a valid input")
    safe = 1
  elif type(parameter_value) == str and parameter_name in float_parameters:
    try:
      parameter_value = float(parameter_value)
    except:
      stl.error("Please enter a valid input")
    safe = 1
  elif type(parameter_value) == str and parameter_name not in float_parameters:
    try:
      parameter_value = int(parameter_value)
    except:
      stl.error("Please enter a valid input")
      safe = 1
  return safe

def write_parameters_file(parameters_dict):
  with open("parameters.dat","w") as f:
    f.write("DB_LOCATION=/home/foliva/Desktop/Algoritmo_testing/Algoritmo/Algoritmo_fresh/\n\n")
    f.write("PYMODHOME=/home/foliva/miniconda/envs/pymod3/lib/python3.7/site-packages/pmg_tk/startup/pymod3/pymod_lib/pymod_main/\n\n")
    f.write("RESOLUTION=" + str(parameters_dict["res"]))
    f.write("SEQID=" + str(parameters_dict["sequid"]))
    f.write("HMM_TO_IMPORT=" + str(parameters_dict["hmm_2_import"]))
    f.write("PDB_TO_USE=" + str(parameters_dict["pdb_2_use"]))
    f.write("E_VAL=" + str(parameters_dict["eva"]))
    f.write("NUM_OF_MOD_WT=" + str(parameters_dict["number_of_wt_models"]))
    f.write("NUM_OF_MOD_mut=" + str(parameters_dict["number_of_MUT_models"]))

# title

stl.title("Automodeling Software")

# drag and drop the mutation file
input_file = stl.file_uploader("Drag your input file here")

col1, col2 = stl.columns(2) # make 2 columns for input parameters
# parameters = stl.form(key='INPUT PARAMETERS')
safe = []
with stl.form(key='parameters'):
  with col1:
      res = stl.text_input(label='Max acceptable resolution for templates')
      safe.append(check_mistakes(res, "res"))
      seqid = stl.text_input(label='Sequence identity threshold')
      safe.append(check_mistakes(seqid, "seqid"))
      hmm_2_import = stl.text_input(label='HMM to import')
      safe.append(check_mistakes(hmm_2_import, "hmm_2_import)"))
      pdb_2_use = stl.text_input(label='MAX number of templates to download')
      safe.append(check_mistakes(pdb_2_use, "pdb_2_use"))
  with col2:
      eva = stl.text_input(label='E val')
      safe.append(check_mistakes(eva, "eva"))
      number_of_wt_models = stl.text_input(label='Number of WT model to generate')
      safe.append(check_mistakes(number_of_wt_models, "number_of_wt_models"))
      number_of_mut_models = stl.text_input(label='Number of MUTANTS model to generate')
      safe.append(check_mistakes(number_of_mut_models, "number_of_mut_models"))
  stl.form_submit_button()

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
#    start_desktop()

