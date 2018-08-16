#!/usr/bin/python
import smtplib
import sys
import time
import csv
from csv import reader
import mimetypes
import email
import email.mime.application
import os
import subprocess
import optparse
from optparse import OptionParser
import glob
from email.mime import multipart
from email.mime import text
from os import path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import random

#Creates parser for arguments
parser = OptionParser()

#Defines the email columns using -e or --ecol. Action type is append.
parser.add_option("-e", "--ecol", type="string", help="define the column nummber for email", action="append", dest="ecol")
#Defines an attachemnt for all emails. It is also type append.
parser.add_option("-a", "--attach", type="string", help="attach a file or list of files to mail", action="append", dest="attach")
#To attach files to the respective emails in the row. Type is append.
parser.add_option("-c", "--acol", type="string", help="attach file written in a given column", action="append", dest="acol")
#Defines the mail content. Type is store.
parser.add_option("-m", "--content", type="string", help="the file containing the email content. Default is nothing.", action="store", default="", dest="content")
#This defines the column for respective mailing formats for the respective emails in that row.
parser.add_option("-n", "--content-col", type="string", help="define column contaning the message file name", action="store", dest="ccol")
#Defines the subject of the email.
parser.add_option("-s", "--subject", type="string", help="define the subject of email. Put it in quotes. Default is nothing.", default="", action="store", dest="subject")
#Defines the suject column which sets the subject to emails in that row.
parser.add_option("-t", "--subject-col", type="string", help="define column containing subject", action="store", dest="scol")
#Sets the delimiter for datafile.
parser.add_option("-d", "--delimiter", type="string", help="sets the delimiter. Default is ,", default=",", action="store", dest="delim")
#Defines the input file or datafile.
parser.add_option("-f", "--file", type="string", help="define the file to take input", action="store", dest="file")
#Defines a special string for calling details from the file for respective emails in the row.
parser.add_option("-p", "--pick", type="string", help="This is used to define what word should be used to call details from file. Default is arg. In content, arg[1] refers to value of cell corresponding to column 1 and respective row.", default="arg", action="store", dest="pick")
#Defines the host
parser.add_option("-i", "--host", type="string", help="used to set the smtp host. Default is smtp.googlemail.com", default="smtp.googlemail.com", action="store", dest="host")
#Define the port
parser.add_option("-j", "--port", type="string", help="sets the port of smtp host. Default is 465.", default="465", action="store", dest="port")
#Sets the delay between consecutive emails.
parser.add_option("-w", "--wait", type="string", help="Creates delays in sending individual emails.", default="30", action="store", dest="wait")
#Restricts the use of ssl for non-ssl servers.
parser.add_option("--no-ssl", help="restricts the use of ssl. For non ssl smtp hosts", action="store_true", dest="nossl")
#Assumes that first row also conatins mailing data.
parser.add_option("--no-header", action="store_true", help="Tells that first row is to considered as entry.", dest="nohead", default="")
#Defines mail type as html.
parser.add_option("--html", action="store_true", help="Sends HTML email.", dest="html", default="")

(options, args) = parser.parse_args()

#Checks if input file is defines.
if not options.file:
    print("No file defined")
    sys.exit(0)    

#Checks if email column is defined or not.
if not options.ecol:
    print("Column for receivers not defined")
    sys.exit(0)

#If conetnt is not defined then throws a warning.
if not options.content:
    if not options.ccol:
        print("No message file defined.")
        print("Sending email with default content")
        print("Program will wait for 30 seconds. Close it for stopping the process.")
        time.sleep(30)

#Throws error as both content and content-column cannot be used together.
if options.content:
    con = options.content
    if options.ccol:
        print("You cannot use both content and content-col options.")
        sys.exit(0)

#Throws error as both subject and subject-column cannot be used together.
if options.subject:
    if options.scol:
        print("You cannot use both subject and subject-col options.")
        sys.exit(0)

#Stores email id as varibale emid till the end of program.
emid = input("Email-Id: ")
#Stores password till the end of program.
password = getpass.getpass()

#Checks if option wait is used. If yes, then converts the value to int.
if options.wait:
    wait = int(options.wait)
#Converts type of options.port to int.
options.port = int(options.port)
#Stores the value parsed to options.pick as pick.
pick = options.pick
#Stores the value parsed to options.delim to delim.
delim = options.delim
#Defines an empty list for attachemts.
attachment = []
#Stores the value of options.suject as subject.
subject = options.subject

#Defines ifile as the file operator for the input file.
ifile = open(options.file, 'rU')
#Reads the data from input file to reader.
reader = csv.reader(ifile, delimiter=delim)
#Sets the row-number for counting to zero
rownum = int(0)
#It is being used to stop the program from taking input from first row.
g = (-1)*len(options.ecol)

#Setting g = 0 allows the program to take input from first row.
if options.nohead:
    g = int(0)

#Tries to connect to the smtp server.
try:
    server_ssl = smtplib.SMTP_SSL(options.host, int(options.port))
    if options.nossl:
        server_ssl = smtplib.SMTP(options.host, int(options.port))
except:
    print('Cannot Connect to server')
    sys.exit(0)

#Tries to login with the given credentials.
try:
    server_ssl.ehlo()
    server_ssl.login(emid, password)
except:
    print("Login Failed.")
    server_ssl.quit()
    sys.exit(0)

#Create a file handler and then close it to create the file fail.txt if it does not exist or otherwise to clear it.
fail = open('fail.txt','w')
fail.close()

#List 'a' is used temporarily to store the data in sa row.
a=[]

for (row) in reader:
    a = (row)
    #Varibale 'k' is set to zero in each iteration so that it can be used to keep a count on the number of email coulmns.
    k = int(0)
    while ((k < len(options.ecol)) and (a[int(options.ecol[k])] != '') and (g > -1)):
        #Defines a varibale to delay to store the delay between emails.
        delay=0
        #Creates varibale delays between emails in the range of 10 sec more than parsed value.
        if options.wait:
            delay = random.randint(wait, wait+10)
        #Defines msg as the object that stores the email data.
        msg = email.mime.multipart.MIMEMultipart()
        #Stores the subject if subject-column is used.
        if options.scol:
            options.scol = int(options.scol)
            subject = a[(options.scol)]
        #Adds subject to the msg.
        msg['Subject'] = subject
        #Adds the From and To data to msg.
        msg['From'] = emid
        msg['To'] = a[int(options.ecol[k])]
        time.sleep(delay*(0.33))

        #Defines message to store the content data.
        if options.ccol:
            options.ccol = int(options.ccol)
            con = open(a[(options.ccol)], 'r')
            message = con.read()
            con.close()
        if options.content:
            con = open(options.content, 'r')
            message = con.read()
            con.close()
        #Here i is used as a conter.
        i = int(0)
        while i < len(a):
            #Adds the data from the input file.
            message = message.replace(pick + '[' + str(i) + ']', a[i])
            i+=1

        #Defines message as the email body.
        body = email.mime.text.MIMEText(message)
        if options.html:
            body = email.mime.text.MIMEText(message, 'html')
        time.sleep(delay*(0.33))
        #Attaches the body to msg.
        msg.attach(body)

        #This section handles the attachment part for theh email.
        if options.acol:
            acola = []
            acolas = []
            acola = options.acol[:]
            i = int(0)
            while i < len(acola):
                acolas.append(a[int(acola[i])])
                i+=1
            if options.attach:
                attachment = options.attach[:]
                attachment = acolas + attachment
            else:
                attachment = acolas[:]
        i = int(0)
        if options.acol or options.attach:
        	if options.attach and options.acol is None:
        		attachment = options.attach[:]
        	while i < len(attachment):
        		if attachment[i] != '':
        			filename=attachment[i]
        			fp=open(filename, 'rb')
        			att_file, ext = os.path.splitext(filename)
        			ext = ext[1:]
        			att = email.mime.application.MIMEApplication(fp.read(),_subtype=ext)
        			fp.close()
        			att.add_header('Content-Disposition','attachment',filename=filename)
        			msg.attach(att)
        		i+=1
        #Tries to send the mail.
        try:
            server_ssl.sendmail(emid,[a[int(options.ecol[k])]], msg.as_string())
            rownum+=1
            print("Completed " + str(rownum) + " emails.")
            time.sleep(delay*(0.1))
            k+=1
        except:
            #On failure on first try, tries it again.
            try:
                server_ssl.sendmail(emid,[a[int(options.ecol[k])]], msg.as_string())
                rownum+=1
                print("Completed " + str(rownum) + " emails.")
                time.sleep(delay*(0.33))
                k+=1
            except:
                with open('fail.txt', 'a') as fail:
                    fail.write(a[int(options.ecol[k])] + '\n')
                    k+=1
                    fail.close()
    g+=1
#Closes the connection to the ssl server.
server_ssl.quit()
