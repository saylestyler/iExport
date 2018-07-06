#!/usr/bin/env python3

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
body { margin: 0; padding: 0; }
.message {
    white-space: pre-wrap;
    max-width: 800px;
    padding: 10px;
    margin: 10px;
}
.me { background-color: #A6DBFF; }
.buddy { background-color: #EEE; }
.message img { max-width: 800px; }
</style>
</head>
<body>
""")

def list_chats():
    db = sqlite3.connect(CHAT_DB)
    cursor = db.cursor()
    rows = cursor.execute("""
        SELECT chat_identifier
          FROM chat;
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
        who = "me" if row[1] is 1 else "contact"
        if row[3]:
            attachment = path.expanduser(row[3])
            media_type = mimetypes.guess_type(attachment)[0]
            try:
                with open(attachment, "rb") as image:
                    encoded_data = base64.b64encode(image.read())
            except:
                encoded_data = ""
            text = "<img src=\"data:%s;base64,%s\">" % (
                media_type, encoded_data)
            text = "<img src=\"%s\">" % (attachment)

        else:
            text = cgi.escape(row[2] or '')
        line = "<div class=\"from-%s\" title=\"%s\">%s</div>" % (
            who, date, text)
        print(line.encode("utf8"))

    print("""
    </body>
    </html>
    """)
export_all()

#list_chats()

