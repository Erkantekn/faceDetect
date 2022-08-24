"""
Ana klasörleri listele
    eğer klasör isminin başında ~varsa continue geç
    Faces_all/KLASÖRİSMİ varmı bak
    alt klasörleri listele
        eğer klasör isminin başında ~varsa continue geç
        Faces_all/KLASÖRİSMİ(Back)/KLASÖRİSMİ2(1) var mı bak
        klasörleri(aab1) listele
            eğer klasör isminin(aab1) başında ~varsa continue geç
            klasör(aab1)/faces klasörünü aç
            içindekileri Faces_all/KLASÖRİSMİ(Back)/KLASÖRİSMİ2(1) içine kopyala
            hata alırsan log günlüğüne düş Faces_all/log.txt
            klasör bittiğinde klasör isminin(aab1) başına ~ ekle
        klasör bittiğinde isminin başına ~ ekle
    klasör bittiğinde isminin başına ~ ekle
FİNİTTO
"""
from operator import countOf
import cv2, csv, time
import os
import datetime
import shutil

path = "D:\\Tez\\-data"
pathKopyalanicak ="D:\\Tez\\-Faces_all\\"

f = open(pathKopyalanicak+"-LOG.txt", 'a+')

def log(data):
    f.write(str(datetime.datetime.now())+" | "+str(str(data)+"\n"))
    f.flush()
    print(str(datetime.datetime.now())+" | "+str(str(data)))
log("Started")

for mainDir in os.listdir(path):
    if(mainDir[0]=="-"):
        continue
    for childDir in os.listdir(path+"\\"+mainDir):
        if(childDir[0]=="-"):
            continue
        sizes=[]
        for vid in os.listdir(path+"\\"+mainDir+"\\"+childDir):
            if(vid[0]=="-"):
                continue
            #mainDir= BACK, childDir= 1,2, vid=aab1,eeb1
            if not os.path.exists(pathKopyalanicak):
                os.makedirs(pathKopyalanicak)
            if not os.path.exists(pathKopyalanicak+mainDir):
                os.makedirs(pathKopyalanicak+mainDir)
            if not os.path.exists(pathKopyalanicak+mainDir+"\\"+childDir):
                os.makedirs(pathKopyalanicak+mainDir+"\\"+childDir)
            
            #vid//faces içini kopyala
            faces = os.listdir(path+"\\"+mainDir+"\\"+childDir+"\\"+vid+"\\faces\\")
            faces_len =len(faces)
            log(path+"\\"+mainDir+"\\"+childDir+"\\"+vid+" açıldı. "+str(faces_len) +" adet face bulundu.")
            if faces_len>0:
                for face in faces:
                    src = path+"\\"+mainDir+"\\"+childDir+"\\"+vid+"\\faces\\"+face
                    dst = pathKopyalanicak+mainDir+"\\"+childDir+"\\"
                    shutil.copy(src,dst)
            log(path+"\\"+mainDir+"\\"+childDir+"\\"+vid+" kopyalandı.")
            os.rename(path+"\\"+mainDir+"\\"+childDir+"\\"+vid,path+"\\"+mainDir+"\\"+childDir+"\\-"+vid)
        log(path+"\\"+mainDir+"\\"+childDir+ " bitti.")
        os.rename(path+"\\"+mainDir+"\\"+childDir,path+"\\"+mainDir+"\\-"+childDir)
    log(path+"\\"+mainDir+ " bitti.")
    os.rename(path+"\\"+mainDir,path+"\\-"+mainDir)
            