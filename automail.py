#!/usr/bin/python3
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


def create_parser():
    #Creates parser for arguments
    parser = OptionParser()
    
    #Defines the email columns using -e or --ecol. Action type is append.
    parser.add_option("-e", "--ecol", type="int", help="define the column nummber for email", action="append", dest="ecol")
    #Defines an attachemnt for all emails. It is also type append.
    parser.add_option("-a", "--attach", type="string", help="attach a file or list of files to mail", action="append", dest="attach")
    #To attach files to the respective emails in the row. Type is append.
    parser.add_option("-c", "--acol", type="int", help="attach file written in a given column", action="append", dest="acol")
    #Defines the mail content. Type is store.
    parser.add_option("-m", "--content", type="string", help="the file containing the email content. Default is nothing.", action="store", default="", dest="content")
    #This defines the column for respective mailing formats for the respective emails in that row.
    parser.add_option("-n", "--content-col", type="int", help="define column contaning the message file name", action="store", dest="ccol")
    #Defines the subject of the email.
    parser.add_option("-s", "--subject", type="string", help="define the subject of email. Put it in quotes. Default is nothing.", default="", action="store", dest="subject")
    #Defines the suject column which sets the subject to emails in that row.
    parser.add_option("-t", "--subject-col", type="int", help="define column containing subject", action="store", dest="scol")
    #Sets the delimiter for datafile.
    parser.add_option("-d", "--delimiter", type="string", help="sets the delimiter. Default is ,", default=",", action="store", dest="delim")
    #Defines the input file or datafile.
    parser.add_option("-f", "--file", type="string", help="define the file to take input", action="store", dest="file")
    #Defines a special string for calling details from the file for respective emails in the row.
    parser.add_option("-p", "--pick", type="string", help="This is used to define what word should be used to call details from file. Default is arg. In content, arg[1] refers to value of cell corresponding to column 1 and respective row.", default="arg", action="store", dest="pick")
    #Defines the host
    parser.add_option("-i", "--host", type="string", help="used to set the smtp host. Default is smtp.googlemail.com", default="smtp.googlemail.com", action="store", dest="host")
    #Define the port
    parser.add_option("-j", "--port", type="int", help="sets the port of smtp host. Default is 465.", default=465, action="store", dest="port")
    #Sets the delay between consecutive emails.
    parser.add_option("-w", "--wait", type="int", help="Creates delays in sending individual emails.", default=30, action="store", dest="wait")
    #Restricts the use of ssl for non-ssl servers.
    parser.add_option("--no-ssl", help="restricts the use of ssl. For non ssl smtp hosts", action="store_true", dest="nossl")
    #Assumes that first row also conatins mailing data.
    parser.add_option("--no-header", action="store_true", help="Tells that first row is to considered as entry.", dest="nohead", default="")
    #Defines mail type as html.
    parser.add_option("--html", action="store_true", help="Sends HTML email.", dest="html", default="")

    return parser


def check_options(options):
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


# Parse the message content
def message_parse(row, message, pick):
    for i, v in enumerate(row):
        message = message.replace(pick + '[' + str(i) + ']', v)
    return message


class smtpsession:
    # Takes in the options, sender email and file handler for fail file
    def __init__(self, options, emid, fail):
        self.options = options
        self.attachment = []
        self.emid = emid
        self.counter = 0
        self.fail = fail
        if options.content:
        	with open(options.content, 'r') as f:
        		self.content = f.read()

    # Starts session
    def start_session(self):
        try:
            if self.options.nossl:
                self.session = smtplib.SMTP(self.options.host, self.options.port)
            else:
                self.session = smtplib.SMTP_SSL(self.options.host, self.options.port)
        except Exception as e:
            print("Connection Error")
            print(e.message, e.args)
            sys.exit(0)

    # Try Session Login
    def login_session(self):
        try:
            self.session.ehlo()
            self.session.login(self.emid, getpass.getpass())
        except Exception as e:
            print("Login Error")
            print(e.message, e.args)
            self.session.quit()
            sys.exit(0)

    def quit_session(self):
        self.session.quit()

    def attach_file(self, filename):
         fp=open(filename, 'rb')
         att_file, ext = os.path.splitext(filename)
         ext = ext[1:]
         att = email.mime.application.MIMEApplication(fp.read(),_subtype=ext)
         fp.close()
         att.add_header('Content-Disposition','attachment',filename=filename)
         self.msg.attach(att)


    def create_mail(self, row, receiver):
        self.msg = email.mime.multipart.MIMEMultipart()
        self.msg['From'] = self.emid

        if self.options.scol:
            self.msg['Subject'] = row[self.options.scol]
        else:
            self.msg['Subject'] = self.options.subject

        self.msg['To'] = receiver

        if self.options.ccol:
            con = open(a[(options.ccol)], 'r')
            message = message_parse(row, con.read(), self.options.pick)
            con.close()
        else:
            message = message_parse(row, self.content, self.options.pick)

        if self.options.html:
            body = email.mime.text.MIMEText(message, 'html')
        else:
            body = email.mime.text.MIMEText(message)

        self.msg.attach(body)

        if self.options.attach:
            for filename in self.options.attach:
                self.attach_file(filename)
        if self.options.acol:
            for filei in self.options.acol:
                self.attach_file(row[filei])

    def send_email(self, receiver, retry=True):
        try:
            self.session.sendmail(self.emid, receiver, self.msg.as_string())
            self.counter+=1
            print("Completed", self.counter, "emails")
        except Exception as e:
            print("Error in sending email")
            print(e.message, e.args)
            if retry:
                self.send_email(receiver, retry=False)


def main():
    (options, args) = create_parser().parse_args()

    check_options(options)

    # Opening fail file
    fail = open('fail.txt','w')

    # Email Id
    emid = input("Email Id: ")

    # Create SMTPsession
    session = smtpsession(options, emid, fail)
    session.start_session()
    session.login_session()

    #Defines ifile as the file operator for the input file.
    ifile = open(options.file, 'r')
    #Reads the data from input file to reader.
    reader = csv.reader(ifile, delimiter=options.delim)

    if not options.nohead:
        next(reader)

    for row in reader:
        for rec in options.ecol:
            session.create_mail(row, row[rec])
            if options.wait:
                sleep(random.randint(options.wait, options.wait+10))
            session.send_email()

    fail.close()
    ifile.close()
    session.quit_session()


if __name__ == '__main__':
    main()
