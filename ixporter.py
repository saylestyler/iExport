#!/usr/bin/env python

# from https://gist.github.com/nslater/b3cbc894ad2c2516dd02

import sys
import urllib
import urlparse
import base64
import mimetypes
import cgi

from os import path

import sqlite3

CHAT_DB = path.expanduser("~/Library/Messages/chat.db")

EPOCH=978307200

print("""
    <!doctype html>
    <html>
    <head>
    <meta charset=\"utf-8\">
    <style>
    body { 
        width: 100%; 
        margin: 0px;
    }
    .message {
        max-width: 800px;
        padding: 25px;
        margin: 30px auto;
        border-radius: 3px;
        font-size: 24px;
    }
    .me { 
        background-color: #c2ffe4; 
    }
    .buddy { 
        background-color: #e4c2ff; 
    }
    .message img {
        max-width: 760px;
        margin: 20px;
    }
    hr {
        width: 75%;
    }
    </style>
    </head>
    <body>
""")

def list_chats():
    db = sqlite3.connect(CHAT_DB)
    cursor = db.cursor()
    rows = cursor.execute("""
        SELECT chat_identifier
          FROM chat
          ORDER by desc
          LIMIT 2;
    """)
    for row in rows:
        print(row[0])

def export_all():
    db = sqlite3.connect(CHAT_DB)
    cursor = db.cursor()
    rows = cursor.execute("""
        SELECT chat_identifier
          FROM chat;
    """)
    for row in rows:
        export(row[0])
        print('<hr>')

def export(chat_id):
    db = sqlite3.connect(CHAT_DB)
    cursor = db.cursor()
    rows = cursor.execute("""
          SELECT datetime(m.date + ?, 'unixepoch', 'localtime') as fmtdate,
                 m.is_from_me,
                 m.text,
                 a.filename
            FROM chat as c
      INNER JOIN chat_message_join AS cm
              ON cm.chat_id = c.ROWID
      INNER JOIN message AS m
                 ON m.ROWID = cm.message_id
       LEFT JOIN message_attachment_join AS ma
              ON ma.message_id = m.ROWID
       LEFT JOIN attachment as a
              ON a.ROWID = ma.attachment_id
           WHERE c.chat_identifier = ?
        ORDER BY m.date;
    """, (EPOCH, chat_id))


    for row in rows:
        date = row[0]
        who = "me" if row[1] is 1 else "buddy"
        if row[3]:
            attachment = path.expanduser(row[3])
            media_type = mimetypes.guess_type(attachment)[0]
            try:
                with open(attachment, "rb") as image:
                    encoded_data = base64.b64encode(image.read())
            except:
                encoded_data = ""
            # text = "<img src=\"data:%s;base64,%s\">" % (media_type, encoded_data) # to encode images as strings/host
            text = "<img src=\"file://%s\">" % (attachment) # to serve images locally
        else:
            text = cgi.escape(row[2] or '')
        line = "<div class=\"message %s\" title=\"%s\">%s</div> " % (
                who, date, text)
        print(line.encode("utf8"))
        # print(who, date) # here = 'me' || buddy + utc
        print("""
            </body>
            </html>
        """)

def main():
    if len(sys.argv) == 1:
        export_all()
    sys.exit()
chat_id = None
if len(sys.argv) > 1:
    chat_id = sys.argv[1]
if len(sys.argv) > 2:
    sys.exit()
export_all()

if __name__ == "__main__":
    main()

