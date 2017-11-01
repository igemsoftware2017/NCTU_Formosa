#!/usr/bin/python
import sqlite3
import cgi, cgitb 
import sys

reload(sys)
sys.setdefaultencoding("utf8")

cgitb.enable(display=1, logdir="report.txt")
form = cgi.FieldStorage() 

conn = sqlite3.connect('Parabase.db')

select = form.getvalue('Select')
keyword = form.getvalue('Keyword')
cycle = ["Host", "Pathogen", "Peptide"]

goto = {
	"Host":["host_pathogen","Pathogen"],
	"Pathogen":[["host_pathogen","Host"],["peptide_pathogen","Peptide"]],
	"Peptide":["peptide_pathogen","Pathogen"]
}

html_section1 = '''Content-type: text/html

<html>
<head>
    <title>Searching Result</title>
</head>
<body>
'''
html_section2 = '''
    <h3><u>%s</u></h3>
'''
html_section2_error = '''
    <h1>Error!</h1>
'''
html_section3 = '''
</body>
</html>
'''


def searching(direct, column, keyword):
    global select
    def main_function(direct, column, keyword):
        cursor = conn.execute("SELECT * FROM %s WHERE %s GLOB '*%s*'"%(direct[0], column, keyword))
        columns = conn.execute("PRAGMA table_info(%s)"%(direct[0]))
        index = [column_info for column_info in columns if direct[1] in column_info]
        return cursor, index
    def add_href(Select, Keyword, html_section2_content):
        global html_section2
        first_tag = '<a href="search.py?Select=%s&Keyword=%s">'
        second_tag = '</a>'
        if '(' in Keyword:
            Keyword = Keyword[:Keyword.find('(')]
        Keyword = Keyword.strip(' ').replace(" ","+")
        html_section2_content = html_section2_content.strip(" ")
        return first_tag%(Select, Keyword) + html_section2%(html_section2_content) + second_tag

    if select == "Host":
        cursor, index = main_function(direct, column, keyword)
        if cursor:
            for row in cursor:
    	        print(add_href(direct[1], row[index[0][0]], row[index[0][0]]))
        else:
    	    print(html_section2_error)
    elif select == "Pathogen":
        for show in direct:
            cursor, index = main_function(show, column, keyword)
            if cursor:
                for row in cursor:
                    print(add_href(show[1], row[index[0][0]], row[index[0][0]]))
                print('<hr>')
    elif select == "Peptide":
        cursor, index = main_function(direct, column, keyword)
        if cursor:
            for row in cursor:
                pathogens = row[index[0][0]]
                pathogens = pathogens.replace(";",",").split(",")
                for pathogen in pathogens:
                    if not pathogen: continue
                    print(add_href(direct[1], pathogen, pathogen))
        else:
            print(html_section2_error)






print(html_section1)
searching(goto[select], select, keyword)
print(html_section3)
 
