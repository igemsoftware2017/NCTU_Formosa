import os
import shutil
import subprocess
from optparse import OptionParser #markliou
cmdparser = OptionParser()
cmdparser.add_option("-s", "--score", action="store", dest="scorecard", default=0, help="input a scorecard filename")

(options, args) = cmdparser.parse_args()
scorecard = options.scorecard
if scorecard==0:
    print ("  the input filename is not specified!! Please use -f or --file option...")
    exit(" For more information, use -h or --help")
def reader(readlist=[],keyword=''):
    files=[]
    if keyword != '':
        for file in os.listdir():
            # 可以改成 endswith
            if keyword in file:
                files.append(file)
    return files

    
    
files = reader(keyword='.pdb')
for file in files:
    args = [file,scorecard,'0','2','0',file.replace('.pdb','.pml')]
    cmd='perl SCM_colortool.pl '+' '.join(args)
    subprocess.call(cmd,shell=True)
    print(file)