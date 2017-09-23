# Automail
Automail is an automated personalized email sender. It can send emails from your email-id. You can create different formats for different people. Specifically send attachment as well as sending common attachments. It basically uses a database. It can route any entry anywhere in its options. Everything uses SSL. If it fails to send email, it records the failed ones in fail.txt
# Setup
It uses Python 3. It uses only the standard packages included normally.
If you want to use gmail or other providers which generally block scripts, just go to my account-->Login settings. Then turn on the 'Access to less secure apps.'
# Examples
Look in the examples folder.
# Usage
python automail.py [options] [arguments]

Note: column number starts from 0.

Also, you can use -a command with multiple file names. Preferably, use -a again and again. You can use -a with -c and -c can have multiple columns. Also -e can be used for more than one email id.

Eg: python automail.py -e 0 -e 1 -s "it is example" -a msg.txt -a msg1.txt -m con.txt -c 4 -c 5 -f list.csv --host "exaple.com" --port 25

Other options:
Usage: automail.py [options]

Options:
  -h, --help            show this help message and exit<br>
  -e ECOL, --ecol=ECOL  define the column nummber for email<br>
  -a ATTACH, --attach=ATTACH
                        attach a file or list of files to mail<br>
  -c ACOL, --acol=ACOL  attach file written in a given column<br>
  -m CONTENT, --content=CONTENT   the file containing the email content. Default is nothing.<br>
  -n CCOL, --content-col=CCOL       define column contaning the message file name<br>
  -s SUBJECT, --subject=SUBJECT      define the subject of email. Put it in quotes. Default is nothing.<br>
  -t SCOL, --subject-col=SCOL     define column containing subject<br>
  -d DELIM, --delimiter=DELIM       sets the delimiter. Default is ','<br>
  -f FILE, --file=FILE  define the file to take input<br>
  -p PICK, --pick=PICK  This is used to define what word should be used to
                        call details from file. Default is arg. In content,
                        arg[1] refers to value of cell corresponding to column
                        1 and respective row.<br>
  -i HOST, --host=HOST  used to set the smtp host. Default is
                        smtp.googlemail.com<br>
  -j PORT, --port=PORT  sets the port of smtp host. Default is 465.<br>
  --no-ssl=NOSSL        restricts the use of ssl. For non ssl smtp hosts<br>
  --no-header=NOHEAD    Considers first row as input.<br>
  --html=HTML           Sends HTML emails.
# Contribution
Feel free to use or contribute in any way! If you have any suggestion, create or a pull request or an issue on GitHub.
