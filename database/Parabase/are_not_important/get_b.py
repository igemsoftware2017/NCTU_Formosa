import sqlite3 as sql
B_list=[]
F_list=[]
file1 = open('Bacteria.txt','rt')
lines1 = file1.readlines()
B_count=0
for line1 in lines1:
    count_space = line1.count(' ')
    if line1[0].isupper() and count_space==1 and not'sp.' in line1:
        line1 = line1.replace('\n','')
        B_count +=1
        
        B_list.append(line1)
        
      


file2 = open('Fungi.txt','rt')
lines2 = file2.readlines()
count=0
for line2 in lines2:
    count_space = line2.count(' ')
    if line2[0].isupper() and count_space==1 and not'sp.' in line2:
        line2 = line2.replace('\n','')
        count +=1
        
        F_list.append(line2)
        

conn = sql.connect('Parabase.db')
curs = conn.cursor()
curs.execute('CREATE TABLE bf(name TEXT,short_name TEXT,type TEXT)')
for i in B_list:
    tmp_li = i.split(' ')
    tmp_li[0] = tmp_li[0][0]
    z = tmp_li[0] + '. ' + tmp_li[1] + ', ' + tmp_li[0] + '.' + tmp_li[1]
    t = 'Bacteria'  
    curs.execute('INSERT INTO bf(name,short_name,type) VALUES(?,?,?)',(i ,z ,t))
    



for j in F_list:
    tmp_li = j.split(' ')
    tmp_li[0] = tmp_li[0][0]
    z = tmp_li[0] + '. ' + tmp_li[1] + ', ' + tmp_li[0] + '.' + tmp_li[1]
    t = 'Fungi'
    curs.execute('INSERT INTO bf(name,short_name,type) VALUES(?,?,?)',(j ,z ,t))


conn.commit()
print('Done')














