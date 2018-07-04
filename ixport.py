#!/usr/bin/env python

import base64
import mimetypes
import cgi

from os import path

import sqlite3
# import phonenumbers

CHAT_DB = path.expanduser("~/Library/Messages/chat.db")
ADDRESS_BOOK_DB = path.expanduser('~/Library/Application Support/AddressBook/AddressBook-v22.abcddb')

print("<!doctype html><html><head><meta charset=\"utf-8\"><style>body{width:100%;margin:0px;}.message{max-width:600px;padding:25px;margin:30px auto;border-radius: 3px;font-size:22px; font-family: 'Helvetica'; } .me { background-color: #c2ffe4; } .friend { background-color: #faf; } .message img { max-width: 550px; margin: 20px; } hr { width: 75%; } </style> </head> <body>")

def export_all_contacts():
    db = sqlite3.connect(ADDRESS_BOOK_DB)
    cursor = db.cursor()
    rows = cursor.execute("""
        SELECT ZSTRINGFORINDEXING
          FROM ZABCDCONTACTINDEX;
    """)
    for row in rows:
        line = row[0]
        print(line.encode("utf8"))
        # for match in phonenumbers.PhoneNumberMatcher(line, "US"):
            # print phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)

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
          SELECT m.is_from_me,
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
           WHERE c.chat_identifier = ?;
    """, (chat_id))
    for row in rows:
        who = "me" if row[1] is 1 else "friend"
        if row[3]:
            attachment = path.expanduser(row[3])
            media_type = mimetypes.guess_type(attachment)[0]
            try:
                with open(attachment, "rb") as image:
                    encoded_data = base64.b64encode(image.read())
            except:
                encoded_data = ""
            # text = "<img src=\"data:%s;base64,%s\">" % (media_type, encoded_data)
            text = "<img src=\"file://%s\">" % (attachment)
        else:
            text = cgi.escape(row[2] or '')
        line = "<div class=\"message %s\"> %s <br/> %s</div> " % (who, text)
        print(line.encode("utf8"))
    print("</body></html>")

export_all()
# export_all_contacts()

