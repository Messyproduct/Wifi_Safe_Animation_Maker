import os
import subprocess

text_file = open("SSBH_Path.txt", "r")
local_Path=os.getcwd()
SSBH_Path = text_file.read()
text_file.close()

directory=local_Path+'/IN_NUANMB/'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        input=filename
        command= '"'+SSBH_Path+'" "'+local_Path+'/IN_NUANMB/'+input+'" "'+local_Path+'/IN_JSON/'+input+'.json"'
        
        print("Converting "+input+" to JSON")
        process=subprocess.Popen(command, shell=True)
        process.wait()
        print("FINISHED "+input+"\n")