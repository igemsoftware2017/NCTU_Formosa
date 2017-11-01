#!/usr/bin/python
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding("utf8")

conn1 = sqlite3.connect('Parabase.db')
cursor1 = conn1.execute("SELECT Sequence FROM only_validated_fungus")

dic = {}
count = 1
for i in cursor1:
    i = i[0]
    if count < 10:
        id_str = "000" + str(count)
    elif count < 100:
        id_str = "00" + str(count)
    elif count < 1000:
        id_str = "0" + str(count)
    else:
        id_str = str(count)
    dic[i] = "P" + id_str
    count += 1



for i in dic.keys():
    conn1.execute("UPDATE only_validated_fungus set ID = ? WHERE Sequence = ?", (dic[i], i))
    conn1.commit()
conn1.close()
print("Done")