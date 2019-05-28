# iExport

If you have iMessage, then the files are backed up in `~/Library/Messages/chat.db`

This script will process them from a wild collection of `.plist`s to a single html file

It relies on sqlite3 & python (should be factory installs)

1. `git clone https://www.github.com/saylestyler/iExport && cd iExport`
2. run `python iExport.py > your-backup.html`
3. njoy `your-backup.html`
