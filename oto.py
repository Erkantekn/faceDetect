"""
Ana klasörleri listele
    eğer klasör isminin başında ~varsa continue geç
    data/KLASÖRİSMİ varmı bak
    alt klasörleri listele
        eğer klasör isminin başında ~varsa continue geç
        data/KLASÖRİSMİ/KLASÖRİSMİ2 var mı bak
        videoları listele
            eğer video isminin başında ~varsa continue geç
            data/KLASÖRİSMİ/KLASÖRİSMİ2/VİDEOKLASÖRÜ var mı bak
            data/KLASÖRİSMİ/KLASÖRİSMİ2/VİDEOKLASÖRÜ/frames var mı bak
            data/KLASÖRİSMİ/KLASÖRİSMİ2/VİDEOKLASÖRÜ/faces var mı bak
            videoyu aç
            siyah kare varsa olmayana kadar resim oku
            data/TXTKLASÖRÜ/KLASÖRİSMİ/KLASÖRİSMİ2/VİDEOİSMİ.txt dosyasını oku
            sırayla x y w h değerlerini al
            track işlemini başlat
            hata alırsan log günlüğüne düş data/log.txt
            video bittiğinde isminin başına ~ ekle
        klasör bittiğinde isminin başına ~ ekle
    klasör bittiğinde isminin başına ~ ekle
FİNİTTO
"""


from operator import countOf
import cv2, csv, time
import os
import datetime


constW=228
constH=228
path = "D:\\Tez\\"

def save_bbox(img, bbox,cnt,save_path,vidName):
    #burada oran orantı yapmamız gerekiyor
    #tüm verileri 228x228 formatında yapmamız lazım
    cv2.imwrite(save_path + "\\frames\\"+str(vidName)+"-"+str(cnt)+".jpg" , img)

    y,x, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    resized =cv2.resize(img[x:x+w, y:y+h],(constW,constH),cv2.INTER_AREA)
    cv2.imwrite(save_path + "\\faces\\"+str(vidName)+"-"+str(cnt)+".jpg" , resized)
    
def replaceTurkishCaracter(string):
     returnData = str(string).replace('ı','i').replace('ç','c').replace('ğ','g').replace('ş','s').replace('ö','o').replace('ü','u').replace('İ','I').replace('Ç','C').replace('Ğ','G').replace('Ş','S').replace('Ö','O').replace('Ü','U')
     return returnData
def draw_bbox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)
    ##cv2.putText(img, "W: "+str(w)+" H: "+str(h)+"\nYeniden seçmek için R tuşuna basın.", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


f = open(path+"-LOG.txt", 'a+')

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
            #vid = blabla.mp4 verisi
            #childDir = 1,2,3... 16 klasör verisi
            #mainDir = FRONT,BACK.. klasör verisi
            path2=replaceTurkishCaracter(path)
            mainDir2=replaceTurkishCaracter(mainDir)
            childDir2=replaceTurkishCaracter(childDir)
            vid2=replaceTurkishCaracter(vid)

            if not os.path.exists(path2+"\\-data"):
                os.makedirs(path2+"\\-data")
            if not os.path.exists(path2+"\\-data\\"+mainDir2):
                os.makedirs(path2+"\\-data\\"+mainDir2)
            if not os.path.exists(path2+"\\-data\\"+mainDir2+"\\"+childDir2):
                os.makedirs(path2+"\\-data\\"+mainDir2+"\\"+childDir2)
            if not os.path.exists(path2+"\\-data\\"+mainDir2+"\\"+childDir2+"\\"+vid2.split('.')[0]):
                os.makedirs(path2+"\\-data\\"+mainDir2+"\\"+childDir2+"\\"+vid2.split('.')[0])
            if not os.path.exists(path2+"\\-data\\"+mainDir2+"\\"+childDir2+"\\"+vid2.split('.')[0]+"\\frames"):
                os.makedirs(path2+"\\-data\\"+mainDir2+"\\"+childDir2+"\\"+vid2.split('.')[0]+"\\frames")
            if not os.path.exists(path2+"\\-data\\"+mainDir2+"\\"+childDir2+"\\"+vid2.split('.')[0]+"\\faces"):
                os.makedirs(path2+"\\-data\\"+mainDir2+"\\"+childDir2+"\\"+vid2.split('.')[0]+"\\faces")
            #/data/FRONT/4/ae3f/faces-frames klasör yapısı kuruldu

            cap = cv2.VideoCapture(path+"\\"+mainDir+"\\"+childDir+"\\"+vid)
            tracker = cv2.legacy.TrackerMIL_create()
            success, img = cap.read()
            while str(img[0,0]) == "[0 0 0]" and str(img[1,1]) == "[0 0 0]" and str(img[47,0]) == "[0 0 0]" and str(img[100,330]) == "[0 0 0]" and str(img[400,400]) == "[0 0 0]" and str(img[500,530]) == "[0 0 0]":
                log(str(path+"\\-data\\"+mainDir+"\\"+childDir+"\\"+vid+" -> siyah ekran"))
                success, img = cap.read()
            #burada txt'den veri okunacak
            txtX=0
            txtY=0
            txtW=0
            txtH=0
            bbox=(txtX,txtY,txtW,txtH)

            contents=[]
            with open(path+"-data\\TXT\\"+mainDir+"\\"+childDir+"\\"+vid.split('.')[0]+".txt",'r') as c:
                contents = c.readlines()
            log(path+"\\-data\\"+mainDir+"\\"+childDir+"\\"+vid+" -> txt açıldı -> "+str(contents[0]))
            txtX=int(contents[0].split('-')[0])
            txtY=int(contents[0].split('-')[1])
            txtW=int(contents[0].split('-')[2])
            txtH=int(contents[0].split('-')[3])
            bbox=(txtX,txtY,txtW,txtH)
            ###silinecek
            #bbox = cv2.selectROI("Tracking", img, False)

            tracker.init(img, bbox)
            count=1

            while True:
                success, img = cap.read()
                if not success:
                    break

                success, bbox = tracker.update(img)
                if success:
                    
                    savepath=path+"\\-data\\"+mainDir2+"\\"+childDir2+"\\"+vid2.split('.')[0]
                    save_bbox(img, bbox,count,savepath,vid2.split('.')[0])
                    count = count+1
                    #draw_bbox(img, bbox)

                else:
                    log(path+"\\-data\\"+mainDir+"\\"+childDir+"\\"+vid+" -> HATA! TRACK EDİLEMEDİ -> FRAME "+str(count))
                    break
                    #bbox = cv2.selectROI("Tracking", img, False)
                    #tracker.init(img, bbox)

                #cv2.imshow("Tracking", img)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                if cv2.waitKey(1) & 0xFF == ord('b'):
                    bbox = cv2.selectROI("Tracking", img, False)
                    tracker.init(img, bbox)
            cap.release()
            cv2.destroyAllWindows()
            log(path+"\\-data\\"+mainDir+"\\"+childDir+"\\"+vid+" -> Videosu Bitti")
            os.rename(path+"\\"+mainDir+"\\"+childDir+"\\"+vid,path+"\\"+mainDir+"\\"+childDir+"\\-"+vid)
        log(path+"\\-data\\"+mainDir+"\\"+childDir+" -> Ara Klasörü Bitti")
        os.rename(path+"\\"+mainDir+"\\"+childDir,path+"\\"+mainDir+"\\-"+childDir)
    log(path+"\\-data\\"+mainDir+" -> Ana Klasörü Bitti")
    os.rename(path+"\\"+mainDir,path+"\\-"+mainDir)

