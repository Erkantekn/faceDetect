from ast import While
from email.mime import image
import cv2, csv, time
import os
import copy
"""
Ana klasörleri listele
    eğer klasör isminin başında ~varsa continue geç
    alt klasörleri listele
        eğer klasör isminin başında ~varsa continue geç
        videoları listele
            eğer video isminin başında ~varsa continue geç

            videoyu aç
            siyah kare varsa olmayana kadar resim oku
            rectangle seçtir
            okeylerse 
            data/TXTKLASÖRÜ/KLASÖRİSMİ/KLASÖRİSMİ2/VİDEOİSMİ.txt dosyasına yazdır

            video bittiğinde isminin başına ~ ekle
        klasör bittiğinde isminin başına ~ ekle
    klasör bittiğinde isminin başına ~ ekle
FİNİTTO
"""
def draw_bbox(img, bbox):
    newImg=img
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(newImg, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)
    cv2.putText(newImg, "W: "+str(w)+" H: "+str(h)+" || Yeniden -> R || Cikis -> ESC", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow("Tracking",newImg)

path = "D:\\Tez\\"

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
            if not os.path.exists(path+"\\-data\\TXT"):
                os.makedirs(path+"\\-data\\TXT")
            if not os.path.exists(path+"\\-data\\TXT\\"+mainDir):
                os.makedirs(path+"\\-data\\TXT\\"+mainDir)
            if not os.path.exists(path+"\\-data\\TXT\\"+mainDir+"\\"+childDir):
                os.makedirs(path+"\\-data\\TXT\\"+mainDir+"\\"+childDir)

            cap = cv2.VideoCapture(path+"\\"+mainDir+"\\"+childDir+"\\"+vid)
            tracker = cv2.legacy.TrackerMIL_create()
            success, img = cap.read()
            while str(img[0,0]) == "[0 0 0]" and str(img[1,1]) == "[0 0 0]" and str(img[47,0]) == "[0 0 0]" and str(img[100,330]) == "[0 0 0]" and str(img[400,400]) == "[0 0 0]" and str(img[500,530]) == "[0 0 0]":
                print("siyah ekran")
                success, img = cap.read()
            orgImg=copy.deepcopy(img)
            bbox=(0,0,0,0)
            pointX=515
            pointY=225
            size=250
            oran=5
            bbox = (pointX,pointY,size,size)
            draw_bbox(img,bbox)
            while True:
                k = cv2.waitKey(0)
                print(k)
                #print(k)
                #119 W, 97 A,115 S,100 D,+ 43, - 45
                if k==27:    # Esc key to stop
                    exit(0)
                if k==119:    
                    pointY=pointY-oran
                if k==97:    
                    pointX=pointX-oran
                if k==115:    
                    pointY=pointY+oran
                if k==100:    
                    pointX=pointX+oran
                if k==43:    
                    size=size+oran
                if k==45:    
                    size=size-oran
                if k==13:
                    break
                if k==27:
                    exit(0)
                img=copy.deepcopy(orgImg)
                draw_bbox(img,bbox = (pointX,pointY,size,size))
            
            if str(bbox[0])+'-'+str(bbox[1])+'-'+str(bbox[2])+'-'+str(bbox[3]) !="0-0-0-0":
                with open(path+"\\-data\\TXT\\"+mainDir+"\\"+childDir+"\\"+vid.split('.')[0]+".txt", 'w') as f:
                    f.write(str(bbox[0])+'-'+str(bbox[1])+'-'+str(bbox[2])+'-'+str(bbox[3]))
            else:
                exit(0)
            cap.release()
            cv2.destroyAllWindows()
            print("video bitti")
            os.rename(path+"\\"+mainDir+"\\"+childDir+"\\"+vid,path+"\\"+mainDir+"\\"+childDir+"\\-"+vid)
        print("1 klasörü bitti")
        os.rename(path+"\\"+mainDir+"\\"+childDir,path+"\\"+mainDir+"\\-"+childDir)
    print("FRONT klasörü bitti")
    os.rename(path+"\\"+mainDir,path+"\\-"+mainDir)