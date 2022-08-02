from math import floor
from turtle import screensize
import cv2, csv, time
import os
import datetime
from screeninfo import get_monitors
import numpy as np
screenSize =()
for m in get_monitors():
    screenSize = (m.width,m.height)
"""
klasörleri listele
    toplam ekran genişliğini 228'e böl -> sonucu aşağı yuvarla -> sonuc countX
    toplam ekran yüksekliğini 228'e böl -> sonucu aşağı yuvarlar -> sonuc countY
    her klasörün faces klasörüne gir 
    (countX * countY) kadar resim olacak. -> sonuc countTotal
    3600(klasördeki dosya sayısı) / countTotal -> kaçar kaçar atlanacağını verecek
    ekrana sırasıyla fotoları yerleştir
        eğer fotoya ulaşılamazsa bir sonraki fotoyu yazdır
        5 hata alınırsa log düş
    Space'e basılırsa sonraki klasöre geç
    ESC'ye basılırsa log'a düş
"""

pathDic = 'D:\\Tez\\-data\\RIGHT\\'
pathLog = 'D:\\Tez\\-data\\qualityControlLOG.txt'
pathError = 'D:\\Tez\\-data\\qualityControl.txt'

f = open(pathLog, 'a+')
def log(data):
    f.write(str(datetime.datetime.now())+" | "+str(str(data)+"\n"))
    f.flush()
    print(str(datetime.datetime.now())+" | "+str(str(data)))
d = open(pathError, 'a+')
def errorLog(data):
    d.write(str(datetime.datetime.now())+" | "+str(str(data)+"\n"))
    d.flush()
    print(str(datetime.datetime.now())+" | "+str(str(data)))
countX=floor(screenSize[0]/228)
countY=floor(screenSize[1]/228)
countTotal = countX*countY
log('<-Start')
errorLog('<-Start')
log('resolation' + str(screenSize))
for dic in os.listdir(pathDic):
    for vidDic in os.listdir(pathDic+'\\'+dic):
        log(pathDic+'\\'+dic+'\\'+vidDic+' açıldı.')
        tempFaces = os.listdir(pathDic+'\\'+dic+'\\'+vidDic+'\\faces\\')
        faces = []
        count=1
        for i in tempFaces:
            faces.append( i.split('-')[0]+"-"+ str(count)+"."+i.split('.')[1])
            count=count+1
        jumpRange = floor(len(faces)/countTotal)
        """
        önce countY kadar satır oluştur
        her satır countX kadar olsun
        sonra birleştir
        """
        rangeJumpCounter=0
        column=[0]*countY
        for i in range(0,countY):
            row=[0]*countX
            for x in range(0,countX):
                if os.path.exists(pathDic+'\\'+dic+'\\'+vidDic+'\\faces\\'+faces[rangeJumpCounter]):
                    row[x] = cv2.imread(pathDic+'\\'+dic+'\\'+vidDic+'\\faces\\'+faces[rangeJumpCounter])
                else:
                    x=x-1
                    continue
                rangeJumpCounter = rangeJumpCounter + jumpRange
            column[i] = row
        Vertic = []
        for i in column:
            Hori = np.concatenate((i), axis=1)
            Vertic.append(Hori)
        last = np.concatenate(Vertic,axis=0)
        cv2.imshow("s",last)
        k = cv2.waitKey(0)
        print(k)
        if k ==27:
            log('Exit->')
            errorLog('Exit->')
            exit(0)
        elif k == 13:
            log(pathDic+'\\'+dic+'\\'+vidDic+' | Passed')
            continue
        elif k==32:
            errorLog(pathDic+'\\'+dic+'\\'+vidDic+' | Hatalı')
            log(pathDic+'\\'+dic+'\\'+vidDic+' | Hatalı')
        #13 enter,32 space


