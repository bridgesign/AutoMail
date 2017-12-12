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

parser = OptionParser()

parser.add_option("-e", "--ecol", type="string", help="define the column nummber for email", action="append", dest="ecol")
parser.add_option("-a", "--attach", type="string", help="attach a file or list of files to mail", action="append", dest="attach")
parser.add_option("-c", "--acol", type="string", help="attach file written in a given column", action="append", dest="acol")
parser.add_option("-m", "--content", type="string", help="the file containing the email content. Default is nothing.", action="store", default="", dest="content")
parser.add_option("-n", "--content-col", type="string", help="define column contaning the message file name", action="store", dest="ccol")
parser.add_option("-s", "--subject", type="string", help="define the subject of email. Put it in quotes. Default is nothing.", default="", action="store", dest="subject")
parser.add_option("-t", "--subject-col", type="string", help="define column containing subject", action="store", dest="scol")
parser.add_option("-d", "--delimiter", type="string", help="sets the delimiter. Default is ,", default=",", action="store", dest="delim")
parser.add_option("-f", "--file", type="string", help="define the file to take input", action="store", dest="file")
parser.add_option("-p", "--pick", type="string", help="This is used to define what word should be used to call details from file. Default is arg. In content, arg[1] refers to value of cell corresponding to column 1 and respective row.", default="arg", action="store", dest="pick")
parser.add_option("-i", "--host", type="string", help="used to set the smtp host. Default is smtp.googlemail.com", default="smtp.googlemail.com", action="store", dest="host")
parser.add_option("-j", "--port", type="string", help="sets the port of smtp host. Default is 465.", default="465", action="store", dest="port")
parser.add_option("-w", "--wait", type="string", help="Creates delays in sending individual emails.", default="30", action="store", dest="wait")
parser.add_option("--no-ssl", help="restricts the use of ssl. For non ssl smtp hosts", action="store_true", dest="nossl")
parser.add_option("--no-header", action="store_true", help="Tells that first row is to considered as entry.", dest="nohead", default="")
parser.add_option("--html", action="store_true", help="Sends HTML email.", dest="html", default="")

(options, args) = parser.parse_args()

if not options.file:
    print("No file defined")
    sys.exit(0)    

if not options.ecol:
    print("Column for receivers not defined")
    sys.exit(0)

if not options.content:
    if not options.ccol:
        print("No message file defined.")
        print("Sending email with default content")
        print("Program will wait for 30 seconds. Close it for stopping the process.")
        time.sleep(30)

if options.content:
    con = options.content
    if options.ccol:
        print("You cannot use both content and content-col options.")
        sys.exit(0)

if options.subject:
    if options.scol:
        print("You cannot use both subject and subject-col options.")
        sys.exit(0)

emid = input("Email-Id: ")
password = getpass.getpass()

if options.wait:
    wait = int(options.wait)
options.port = int(options.port)
pick = options.pick
delim = options.delim
attachment = []
subject = options.subject

ifile = open(options.file, 'rU')
reader = csv.reader(ifile, delimiter=delim)
a = []
rownum = int(0)
g = (-1)*len(options.ecol)

if options.nohead:
    g = int(0)

try:
    server_ssl = smtplib.SMTP_SSL(options.host, int(options.port))
    if options.nossl:
        server_ssl = smtplib.SMTP(options.host, int(options.port))
except:
    print('Cannot Connect to server')
    sys.exit(0)

try:
    server_ssl.ehlo()
    server_ssl.login(emid, password)
except:
    print("Login Failed.")
    server_ssl.quit()
    sys.exit(0)

fail = open('fail.txt','w')
fail.close()

for (row) in reader:
    a = (row)
    k = int(0)
    while ((k < len(options.ecol)) and (a[int(options.ecol[k])] != '') and (g > -1)):
        delay=0
        if options.wait:
            delay = random.randint(wait, wait+10)
        msg = email.mime.multipart.MIMEMultipart()
        if options.scol:
            options.scol = int(options.scol)
            subject = a[(options.scol)]
        msg['Subject'] = subject
        msg['From'] = emid
        msg['To'] = a[int(options.ecol[k])]
        time.sleep(delay*(0.33))

        if options.ccol:
            options.ccol = int(options.ccol)
            con = open(a[(options.ccol)], 'r')
            message = con.read()
            con.close()
        if options.content:
            con = open(options.content, 'r')
            message = con.read()
            con.close()
        i = int(0)
        while i < len(a):
            message = message.replace(pick + '[' + str(i) + ']', a[i])
            i+=1

        body = email.mime.text.MIMEText(message)
        if options.html:
            body = email.mime.text.MIMEText(message, 'html')
        time.sleep(delay*(0.33))
        msg.attach(body)

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
        try:
            server_ssl.sendmail(emid,[a[int(options.ecol[k])]], msg.as_string())
            rownum+=1
            print("Completed " + str(rownum) + " emails.")
            time.sleep(delay*(0.1))
            k+=1
        except:
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
server_ssl.quit()
