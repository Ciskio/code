# imports
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request
import urllib.request
import re
import os
import streamlit as st
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
# password
from getpass import getpass

# Functions

def get_page(url):
    src = []
    response = urllib.request.urlopen(url)
    checker = True
    savechunk = None
    while checker:
        chunk = str(response.read(1024))
        text = BeautifulSoup(chunk, 'html5lib')
        src.append(text)
        if "</body></html>" in chunk:
            checker = False
        elif savechunk == chunk:
            checker = False
        savechunk = chunk
    response.close()
    return src

def get_page_reduced(url):
    src = []
    response = urllib.request.urlopen(url)
    test = str(BeautifulSoup(response, 'html5lib')).splitlines()
    response.close()
    print_line = "No"
    count_line = 0
    safe = 0
    for line in test:
        if "class=\"grid\"" in line:
            for chunk in line.split("tr class="):
                if "entry selected" in chunk:
                    print_line = "Yes"
                if count_line == 4:
                    print_line == "No"
                    safe = 1
                if print_line == "Yes" and safe == 0:
                    src.append(chunk)
                count_line += 1


    return src

def get_links(url, filter_name, gene_name):
    links = []
    src = get_page_reduced(url)
    gene_to_find = "<strong>" + str(gene_name.upper()) + "</strong>"
    protein_to_find = str(gene_name[0].upper()) + str(gene_name[1:].lower().replace("+"," "))
    entry_name = str(gene_name.upper()) + "_HUMAN"
    entry_uniprot = "id =\"" + str(gene_name.upper())
    counter: int = 1
    for i in src:
        part = str(i)
        bsoup_element = BeautifulSoup(i, "html5lib")
        if gene_to_find in part and "Human" in part:
            for link in bsoup_element.findAll('a', attrs={'href': re.compile(filter_name)}):
                if "query" not in str(link) and str(link)[18:21] != "A0A":
                    links.append(link.get('href'))
        if protein_to_find in part and "Human" in part:
            addlink_list = []
            for link in bsoup_element.findAll('a', attrs={'href': re.compile(filter_name)}):  # check the lines
                if "query" not in str(link) and str(link)[18:21] != "A0A":
                    links.append(link.get('href'))
                    addlink_list.append(link.get('href'))

        if entry_name in part and "Human" in part:
            #                f.write("\n\n" + part + "\n\n")
            for link in bsoup_element.findAll('a', attrs={'href': re.compile(filter_name)}):
                if "query" not in str(link) and str(link)[18:21] != "A0A":
                    links.append(link.get('href'))
        if entry_uniprot in part:
            links.append("/uniprot/" + str(entry_uniprot))
        counter += 1

        k = open(protein_to_find.replace(" ", "_") + "_Top_3_Results.txt", "w")
        for i in src:
            k.write("\n\n" + str(i) + "\n\n")


    while len(links) > 1:
        links.pop()
    return links

def download_mutations(link_protein):
    src = get_page(link_protein)
    count = 0
    mut_list = []

#    arrow = "xe2\\\\x86\\\\x92"
    for i in src:

        if "xe2\\x86\\x92" in str(i) and re.search("mutagenesis", str(i), re.IGNORECASE) is None and "[" in str(i) and \
                re.search("Alternative sequence", str(i), re.IGNORECASE) is None and re.search("Sequence conflict", \
                str(i), re.IGNORECASE) is None :
            newi = str(i)
            '''
            we look into the downloaded html and look for the characters that makes the arrow in uniprot (ie: C -> S) so
            that we can locate the two aminoacids
            '''

            mutation = str(re.search("xe2\\\\x86\\\\x92", str(i), re.IGNORECASE))
            extremes = mutation[mutation.find("("):mutation.find("),")]
            minim = extremes[1:].split(",")
            minim.pop()
            first_res = newi[int(minim[0]) - 3]
            last_res = newi[int(minim[0]) + 12]

            '''
            We want to do the same thing now but we are looking for [ and ] since it contains the position on the 
            sequence
            '''
            openbracket = str(re.search("\[", str(i)))
            extremes = openbracket[openbracket.find("("):openbracket.find("),")]
            openbracket = extremes[1:].split(",")
            openbracket.pop()
            closedbracket = str(re.search("]", str(i)))
            extremes = closedbracket[closedbracket.find("("):closedbracket.find("),")]
            closedbracket = extremes[1:].split(",")
            closedbracket.pop()
#            print(closedbracket)
            try:
                position = newi[int(openbracket[0]) + 1:int(closedbracket[0])]
            except IndexError:
                position = "Not Good"

            try:
                int(position)
            except ValueError:
                position = "Not Good"
            if first_res == first_res.upper() and last_res == last_res.upper() and position != "Not Good" and \
                    first_res.isalpha() is True and last_res.isalpha() is True:
                mutation = first_res + str(position) + last_res
                if count == 0:
                    mut_list.append(mutation)
                    count += 1
                elif mutation not in mut_list:
                    mut_list.append(mutation)
    return mut_list


def old_main():
    isoform_file = "genelist.txt"
    protein_in = open(isoform_file, 'r')
    protein_name = protein_in.readlines()

    mut_list = []
    genes_list = []
    for i in protein_name:
        i = i.strip('\n')
        i = i.replace(" ", "+")
        genes_list.append(i)

    mutlist = []

    linklist = open("protein_links.txt", "w")

    for i in genes_list:
        complete_link = "https://www.uniprot.org/uniprot/?query=" + i + "+human&sort=score"
        nicei = i.replace("+", " ")
        links = get_links(complete_link, "/uniprot/", i)
        no_link = False
        try:
           links[0]
        except IndexError:
           no_link = True
        if no_link is True:
           mutlist.append("NOT FOUND")
        if no_link is False:
           link_protein = "https://www.uniprot.org" + str(links[0])
           mutations = download_mutations(link_protein)  # , dangerzone
           linklist.write(nicei + ": " + str(link_protein) + "\n" )
           mutlist.append(mutations)
    counter = 0
    lenlist = len(mutlist)
    while counter < lenlist:
        if mutlist[counter] == "NOT FOUND":
            linklist.write(str(protein_name[counter].strip()) + ": NOT FOUND\n")
            protein_name.pop(counter)
            mutlist.pop(counter)
            lenlist -= 1
        else:
            counter += 1

    nicelist = []
    for i in protein_name:
        nicelist.append(i.strip())

    df = pd.DataFrame(mutlist, index=[nicelist]).T
    df.to_csv("mutation_list.csv", index=False)
    df.to_excel("mutation_list.xlsx", index=True)
    df
    return df

def save_file(infile):
    with open(infile.name, "wb") as f:
        f.write(infile.getbuffer())
    os.rename(infile.name, "genelist.txt")

def save_genes(genelist):
  with open("genelist.txt", "w") as f:
      f.write(genelist)

def waiting_function(df):
  value = 0
  mybar = st.progress(value)
  while df.empty:
    if value > 1.0:
      value = 0
      time.sleep(0.5)
    if os.path.isfile("output.zip"):
      mybar.progress(1.0)
      # st.balloons()
      break
    else:
      mybar.progress(value)
    if value == 0:
      time.sleep(1)
    else:
      time.sleep(0.1)
    value+=0.1

def compress_function(files, outputname):
  compression = zipfile.ZIP_STORED
  zf = zipfile.ZipFile(outputname, mode="w")
  for file_to_zip in files:
    zf.write(file_to_zip, file_to_zip, compress_type=compression)
  zf.close()

def get_email():
  with st.form(key='email_address'):
    email = st.text_input(label='Insert email address to get notified when your job is done.', value="yourname@yourprovider.com")
    submit_email = st.form_submit_button()
    return email

def send_email(email_address, download_link):
  sender_email = input("Please, enter the email address from which you want to send your email")
  print("Please, insert password for email sender:")
  password = getpass()
  body = "Hi!\n your calculations are done. To download the results please paste the text \
  from the attacched file in your browser"
  filename = "results_link.txt"
  msg = MIMEMultipart("alternative")
  msg["Subject"] = "Your results are in!"
  msg["From"] = sender_email
  msg["To"] = email_address
  # html_line ="""<html> random text <ul> <li> {download_link}</ul></html>""".format(download_link=download_link)
  # print(download_link)
  # part = MIMEText(html_line, "html")
  # msg.attach(part)
  msg.attach(MIMEText(body, "plain"))
  with open(filename, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
  encoders.encode_base64(part)
  # Add header as key/value pair to attachment part
  part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
  )
  msg.attach(part)
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(sender_email, password)
      server.sendmail(
          sender_email, email_address, msg.as_string()
      )


def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    # testcode = base64.b64encode(data).encode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    # print(testcode)
    return href, "data:application/octet-stream;base64," + bin_str

# main
def app():

    st.title("Search for single point mutations on Uniprot")

    safe = 0
    try:
      os.remove("output.zip")
    except FileNotFoundError:
      pass

    email_address = get_email()

    # drag and drop the mutation file
    with st.form(key='genes_file'):
      input_file = st.file_uploader("Drag your input file here")
      if input_file is not None:
          save_file(input_file)
      submit_file_list = st.form_submit_button()

    with st.form(key='genes'):
      genelist = st.text_area("Insert your genes here", height=100, value="NLGN3\nGRIN2B")

      # st.title(genelist)
      submit_pasted_list = st.form_submit_button()

      df = pd.DataFrame()
      loading_bar = Thread(target = waiting_function, args = (df, ))
      st.report_thread.add_report_ctx(loading_bar)



    if submit_pasted_list:
      save_genes(genelist)
    
    if submit_pasted_list or submit_file_list:
      safe = 1
      action_message = st.empty()
      mutations_pasted_list_message = "Looking for mutations"
      action_message.markdown(mutations_pasted_list_message)
      loading_bar.start()

    if safe == 1:
      # run_old_main = Thread(target = old_main)
      df = old_main()
      if df.empty == False:
        files_to_zip = ["mutation_list.csv", "mutation_list.xlsx", "protein_links.txt"]
        compress_function(files_to_zip, "output.zip")
        action_message.markdown("Job completed successfully. Here's the results:")
        st.dataframe(df)
        with open("output.zip", "rb") as fp:
            btn = st.download_button(
                label="Download",
                data=fp,
                file_name="Uniprot_mutations.zip")

        download_link, bin_str = get_binary_file_downloader_html('output.zip', 'zip')
        st.markdown(download_link, unsafe_allow_html=True)
        with open("results_link.txt", "w") as f:
          f.write(bin_str)
        loading_bar.join()
        if email_address:
          send_email(email_address, download_link)
