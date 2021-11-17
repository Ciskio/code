import streamlit as stl
import os
import paramiko

# save the file in the directory where  the app is running.
def save_file(infile):
    with open(infile.name, "wb") as f:
        f.write(infile.getbuffer())


def download_file_to_computer(filename, host, user, psw):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # # ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect(hostname=host, username=user, password=psw)
    sftp = ssh.open_sftp()
    #
    finalpath = "/home/" + user + "/Desktop/" + filename 
    sftp.put("/content/" + filename, finalpath)
    sftp.close()
    ssh.close()


stl.title("Automodeling Software")

# drag and drop the mutation file
input_file = stl.file_uploader("Drag your input file here")

host = "XXX.dsf.unica.it" # nome macchina
user = "" # nome utente
psw = ""  # password

if input_file is not None:
    save_file(input_file)
    download_file_to_computer(input_file.name, host, user, psw)
