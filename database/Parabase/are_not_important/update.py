#!/usr/bin/python
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding("utf8")
conn1 = sqlite3.connect('Parabase.db')
cursor1 = conn1.execute("SELECT Sequence FROM only_validated_fungus")

conn2 = sqlite3.connect('antifungal_b.db')

for i in cursor1:
    seq = list(i)[0]
    cursor2 = conn2.execute("SELECT Source, Name FROM Hey WHERE Sequence = ?",i)
    lt = ''
    for u in cursor2:
        u = list(u)
        lt = u
    if len(lt) != 2: continue
    source = lt[0]
    name = lt[1]
    conn1.execute("UPDATE only_validated_fungus set Source = ? where Sequence = ?",(source, seq))
    conn1.commit()
    conn1.execute("UPDATE only_validated_fungus set Peptide = ? where Sequence = ?",(name, seq))
    conn1.commit()

conn1.close()
conn2.close()
print("Done")
