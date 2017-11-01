#!/usr/bin/python
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding("utf8")

conn1 = sqlite3.connect('Parabase.db')
cursor1 = conn1.execute("SELECT Pathogen FROM only_validated_fungus")
dic1 = {}
for row in cursor1:
    row = str(row)
    row = row.replace(';', ',')
    pathogens = row.split(',')
    for pathogen in pathogens:
        if '(' in pathogen:
            pathogen = pathogen[:pathogen.find('(')]
        pathogen = pathogen.strip(' ')
        if not pathogen: continue
        if pathogen.count(' ') < 1: continue
        pathogen = pathogen.split(' ')
        if '.' not in pathogen[0]:
            pathogen[0] = pathogen[0][0] + '.'
            pathogen = pathogen[0] + pathogen[1]
            tmp = ''
            for letter in pathogen:
                if letter.islower():
                    if not letter.isdigit():
                        if letter != "'":
                            tmp = tmp + letter
            dic1[tmp] = 0
                    
        elif '.' in pathogen[0]:    
            pathogen = pathogen[0] + pathogen[1]
            tmp = ''
            for letter in pathogen:
                if letter.islower():
                    if not letter.isdigit():
                        if letter != "'":
                            tmp = tmp + letter
            dic1[tmp] = 0
        else: continue
list = dic1.keys()
num = len(list)
print(num)
            
        