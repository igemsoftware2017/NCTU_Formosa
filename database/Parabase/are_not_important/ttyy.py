#!/usr/bin/python
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding("utf8")
countt = {}
conn1 = sqlite3.connect('Parabase.db')
cursor1 = conn1.execute("SELECT PubMed FROM only_validated_fungus")
for row in cursor1:
    row = list(row)
    row = row[0]
    if row:
        countt[row] = ""

keys = countt.keys()
print(len(keys))