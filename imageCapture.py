from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

#Kill runninggphoto2 process to access usb
def killGphoto2Process():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, error = p.communicate()
    
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)
            
shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


picID = "testShots"

clearCommand = ['--folder', '/store_00020001/DCIM/100CANON', '-R', '--delete-all-files']
triggerCommand = ['--trigger-capture']
downloadCommand = ['--get-all-files']

folderName = shot_date + picID
saveLocation = '/home/pi/Desktop/gphoto/imgs' + folderName

def createSaveFolder():
    try:
        os.makedirs(saveLocation)
    except:
        print("Failed to create new directory")
    os.chdir(saveLocation)
    
def captureImages():
    gp(triggerCommand)
    sleep(2) #Increase for long exposures, gives time to take picture
    gp(downloadCommand)
    sleep(2)
    gp(clearCommand)
    
def renameFiles(id):
    shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for filename in os.listdir('.'):
        if len(filename) < 13:
            if filename.endswith(".JPG"):
                os.rename(filename, (shot_time + id + '.JPG'))
                print("renamed the jpg")
            elif filename.endswith(".CR2"):
                os.rename(filename, (shot_time + id + '.CR2'))
                print("renamed the cr2")
                
killGphoto2Process()
gp(clearCommand)
createSaveFolder()


for i in range(0, 10):
    captureImages()
    renameFiles(picID)
    sleep(1)


                
    





    
