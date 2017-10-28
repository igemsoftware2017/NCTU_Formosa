from bs4 import BeautifulSoup as bs
import requests as rq
import sqlite3 as sql
from multiprocessing import Pool
#setting

uni = "http://www.uniprot.org/uniprot/"
search = "http://www.uniprot.org/uniprot/?query=length%3a%5b10+TO+150%5d&fil=reviewed%3ayes&offset=0&sort=score&columns=id%2centry+name%2creviewed%2cprotein+names%2cgenes%2corganism%2clength"
fasta = ".fasta"
cookies = {'limit' : 250,}
total = 114840


#lists needed

id_list = []
herf_list = []

chain_sequence_list = []
dictionary = {}   # id:chain_sequence

tname='negative_2'
table = "'name','seq','clas'"
mydb = sql.connect("antifungal_db.db")
c = mydb.cursor()

try:
    c.execute('create table '+tname+' ('+table+')')
    mydb.commit()
except:
    c.execute('DROP TABLE '+tname)
    mydb.commit()
    c.execute('create table '+tname+' ('+table+')')

def writer(dic,tname):
    try:
        ctitle = []
        ccontent = []
        for item in dic.items():
            ctitle.append(str(item[0]))
            ccontent.append(str(item[1]))

        title = '("'+'", "'.join(ctitle)+'")'
        content = '("'+'", "'.join(ccontent)+'")'
        c.execute('insert into ' + tname +' ' + title + ' values ' + content)
        mydb.commit()
        print('writer done')
    except Exception as e:
        print(e)

for i in range(0,int(total/250)):
    print(i)
    succeed = None
    
    while not succeed:
 
        try:
            search_result = rq.get(search, cookies)
        except:
            pass
        else:
            succeed = True
    
    else:
        search_result.close()     
    
    search = search.replace("set=" + str(i*250) , "set=" + str(i*250 + 250))
    
    search_soup = bs(search_result.text, "lxml")
    temp_list = search_soup.find_all('td')
    
    for i in temp_list:
    
        temp_i = i
        i = str(i)
    
        if 'entryID' in i:

            i = temp_i
            i = i.a.string
            
            herf_list.append(uni + i)

#finish finding id and herf

#use herf to get sequence,second requests

#pool
pool=Pool(4)

def get_prot(u):

    succeed = None

    while not succeed:

        try:
            search_result = rq.get(u, cookies)
            search_result_fasta = rq.get(u + fasta, cookies)
        except:
            pass
        else:
            succeed = True
    else:
        search_result.close()
        search_result_fasta.close()
    
    
    search_soup = bs(search_result.text, "lxml")
    temp_list = search_soup.select('[class~=feature_row]')
    print(len(temp_list))
    fasta_soup = bs(search_result_fasta.text , "lxml")
    seq = fasta_soup.p.string
    seq = seq[seq.find('\n')+1:].replace("\n","")
    
    
    for i in temp_list:
        temp_i = i
        i = str(i)
        
        if 'Chain' in i or 'Peptide' in i:
            i = temp_i
            i = i.a
            i = str(i)
            c1 = i.find('[') + 1
            c2 = i.find(']')
            i = i[c1:c2]
            i_list = i.split("-") 
            print(i_list)
            
            if len(i_list) == 2:
                
                final_seq = seq[int(i_list[0]):int(i_list[1])]
                
                u = u.replace(uni,"")
                
    dictionary={'name':u,'seq':final_seq}
    #writer(dictionary,tname)

            
get_prot('http://www.uniprot.org/uniprot/P01501')




#c.close()
#mydb.close() 
print("ending")








####################################################################################################################








    
            
        
    
    
     
        




