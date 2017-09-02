# Automail
Automail is an automated personalized email sender. It can send emails from your email-id. You can create different formats for different people. Specifically send attachment as well as sending common attachments. It basically uses a database. It can route any entry anywhere in its options. Everything uses SSL.
# Setup
It uses Python 3. It uses only the standard packages included normally.
If you want to use gmail or other providers which generally block scripts, just go to my account-->Login settings. Then turn on the 'Access to less secure apps.'
# Examples
Look in the examples folder.
# Usage
python automail.py [options] [arguments]

Other options:
Usage: automail.py [options]

Options:
  -h, --help            show this help message and exit
  -e ECOL, --ecol=ECOL  define the column nummber for email
  -a ATTACH, --attach=ATTACH
                        attach a file or list of files to mail
  -c ACOL, --acol=ACOL  attach file written in a given column
  -m CONTENT, --content=CONTENT
                        the file containing the email content. Default is
                        nothing.
  -n CCOL, --content-col=CCOL
                        define column contaning the message file name
  -s SUBJECT, --subject=SUBJECT
                        define the subject of email. Put it in quotes. Default
                        is nothing.
  -t SCOL, --subject-col=SCOL
                        define column containing subject
  -d DELIM, --delimiter=DELIM
                        sets the delimiter. Default is ,
  -f FILE, --file=FILE  define the file to take input
  -p PICK, --pick=PICK  This is used to define what word should be used to
                        call details from file. Default is arg. In content,
                        arg[1] refers to value of cell corresponding to column
                        1 and respective row.
  -i HOST, --host=HOST  used to set the smtp host. Default is
                        smtp.googlemail.com
  -j PORT, --port=PORT  sets the port of smtp host. Default is 465.
  --no-ssl=NOSSL        restricts the use of ssl. For non ssl smtp hosts
