#!/usr/bin/python
import requests as rq
from bs4 import BeautifulSoup as bs
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding("utf8")
cookies = {'limit' : 250,}
pubmed = "https://www.ncbi.nlm.nih.gov/pubmed/"

def pubmed_crawler(pub_id):
        global pubmed
        search_result = rq.get(pubmed + pub_id, cookies, timeout=60)
        search_soup = bs(search_result.text, "lxml")
        rprt_abstract = search_soup.find("div", class_="rprt abstract")
        title = rprt_abstract.h1.text
        abstract = rprt_abstract.find("div", class_="abstr").abstracttext.text
        author = rprt_abstract.find("div", class_="auths")
        author = author.find_all("a")
        authors = ''
        num = len(author)
        count = 0
        for i in author:
                count += 1
                if count == num:
                        i = i.text
                        authors = authors + i
                        break
                i = i.text
                authors = authors + i + ', '
        return title, abstract, authors
countt = {}
conn1 = sqlite3.connect('Parabase.db')
cursor1 = conn1.execute("SELECT * FROM only_validated_fungus")
list1 = []
for row in cursor1:
    list2 = []
    for i in range(0, len(row)):
        list2.append(row[i])
    list1.append(list2)

for i in list1:    
    if i[17]:
        countt[i[17]] = ""
    if i[27]: continue
    if i[17]:
              
        if ',' in i[17]: 
            i[17] = i[17][:i[17].find(',')]
        try:
            pubmed_id = str(int(i[17]))
            title, abstract, authors = pubmed_crawler(pubmed_id)
        except:
            continue
        seq = i[0]
        '''
        conn1.execute("UPDATE only_validated_fungus set Abstract = ? where Sequence = ?",(abstract, seq))
        conn1.commit()
        conn1.execute("UPDATE only_validated_fungus set Title = ? where Sequence = ?",(title, seq))
        conn1.commit()
        '''
        conn1.execute("UPDATE only_validated_fungus set authors = ? where Sequence = ?",(authors, seq))
        conn1.commit()
conn1.close()
keyli = countt.keys()
print(len(keyli))


print('Done')
        

