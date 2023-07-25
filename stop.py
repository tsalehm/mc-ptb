import os
from re import findall
import time

# tim
counter=0
while True:
   with open("/root/mc/logs/latest.log","r") as f:
      logs=f.read()

   if len(findall("mcscr",os.popen("screen -ls").read())) ==0:
      stat= "سرور خاموش است"
    
   elif len(findall("\[Server thread/INFO\]: Stopping the server",logs))>0: stat= "سرور در حال خاموش شدن است (بزار کامل خاموش شه بعد روشنش کن)"
   elif len(findall("\[Server thread/INFO\]: Done \(",logs))==0: stat= "سرور در حال روشن شدن است، صبر کن"
   else : 

      with open("/root/mc/logs/latest.log","r") as f:
         logs=f.read()
         # print(logs,"k\nk\nk\n")
         os.popen("screen -XS mcscr stuff \"list\\n\"")
         time.sleep(1)
         logs=f.read()
         if int(findall("There are (\d) of a max of \d players online:",logs)[0]) ==0:
            counter+=1
         else : counter=0
         
   if counter==5:
      counter=0
      print("sending stop signal")
      os.popen("screen -XS mcscr stuff \"stop\\n\"")     
      time.sleep(60)
   time.sleep(20)
   
