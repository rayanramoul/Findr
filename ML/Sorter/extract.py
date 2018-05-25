''' A simple script to extract all configuration files stored in /etc 
to prepare a big dataset for a classifier of categorizable texts '''

import os,shutil
import random

user=str(input("What's your main user's username ?\n ")).lower()
os.system("mkdir /home/"+user+"/configs")
root="/etc/"
r=2
rlist=[]
print(" The files that weren't copied : ")


# Extract from /etc/
for path, subdirs, files in os.walk(root):
    for name in files:
        place=os.path.join(path, name)
        r=random.randint(1,9999999999)
        #if os.path.isfile(place):
        try:
            shutil.copy2(str(place),'/home/'+user+'/configs/'+str(r))
        except:
            print(str(place))


root="/home/"+user+"/.*"


# Extract all the config files in the ~/.* path
for path, subdirs, files in os.walk(root):
    for name in files:
        place=os.path.join(path, name)
        r=random.randint(1,9999999999)
        #if os.path.isfile(place):
        try:
            shutil.copy2(str(place),'/home/'+user+'/configs/'+str(r))
        except:
            print(str(place))
os.chdir("/home/"+user+"/configs")
# Deleting some dangerous files
''' os.system('grep "CERTIFICATE" * | cut -f 1 -d :  > delete && rm -f delete')
os.system('grep "RSA PRIVATE" * | cut -f 1 -d :  > delete && rm -f delete')
os.system('grep ssh- * | cut -f 1 -d :  > delete && rm -f delete')
'''
# Creating the .zip
os.chdir("/home/"+user)
shutil.make_archive("Configs", 'zip', "configs")
shutil.rmtree("configs")
print(" Archive Configs.zip created in your home directory.\n Please send it at : raysamram@protonmail.com.\nThank you!")
