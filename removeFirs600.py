"""
E:\Veriler\BACK\1\abb1\faces

Back/1/abb1-123.jpg
Back/2/abb2-243.jpg
Back/2/ebb2-155.jpg
pathSelected = Faces_selected64
pathRemoved = Faces_removed_firs_600

function IfNotExistCreateDirectory(string path,string ana,string alt){
if not exist(path)
    create path
if not exist(path + ana)
    create path+ana
if not exist(path+ana+alt)
    create path+ana+alt
}

klasörleri listele ANA
    klasörleri listele ALT
        list persons = [{abb1},{count}]
        dosyaları listele ITEM
            persons doldurulacak
        IfNotExistCreateDirectory(oathSelected,ANA,ALT)
        IfNotExistCreateDirectory(oathRemoved,ANA,ALT)
        person in persons
            randoms = [64] -> 600 ile person[1]  arasındaki çift sayılardan oluşacak
            random in randoms
                copy to pathSelected + ANA + ALT+(person[0]+"-"+random+".jpg")
            sayac = 1
            for(int i = 600;i<person[1];i += 2)
                copy to pathRemoved + ANA + ALT +person[0]+"-"+str(sayac)+".jpg"

"""
import os
import datetime
import random
import shutil
pathMain = "E:\\Faces Toplu"
pathToSelected="E:\\Faces_Selected_64"
pathToRemoved="E:\\Faces_Removed_First_600"
pathGetCount = "E:\\Veriler"

f = open("E:\\-LOG.txt", 'a+')

def log(data):
    f.write(str(datetime.datetime.now())+" | "+str(str(data)+"\n"))
    f.flush()
    print(str(datetime.datetime.now())+" | "+str(str(data)))

def IfNotExistCreateDirectory(path,ana,alt):
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path+"\\"+ana):
        os.makedirs(path+"\\"+ana)
    if not os.path.exists(path+"\\"+ana+"\\"+alt):
        os.makedirs(path+"\\"+ana+"\\"+alt)
log("program çalıştırıldı")
for ANA in os.listdir(pathMain):
    if(ANA[0]=="-"):
        log(ANA+" klasörü es geçiliyor")
        continue
    for ALT in os.listdir(pathMain+"\\"+ANA):
        if(ALT[0]=="-"):
            log(ANA+"\\"+ALT+" klasörü es geçiliyor")
            continue
        log(pathMain+"\\"+ANA+"\\"+ALT+" klasörü üzerinde işlemler başlatıldı")
        persons={}
        for item in os.listdir(pathGetCount+"\\"+ANA+"\\"+ALT):
            persons[item] = len(os.listdir(pathGetCount+"\\"+ANA+"\\"+ALT+"\\"+item+"\\faces"))

        """
        listItems=[]
        for item in os.listdir(pathMain+"\\"+ANA+"\\"+ALT):
            listItems.append(item.split('-')[0])
        persons ={i:listItems.count(i) for i in listItems}
        listItems.clear()
        """


        log("klasördeki tüm resimlerin sayısı çekildi")
        log(persons)


        IfNotExistCreateDirectory(pathToSelected,ANA,ALT)
        IfNotExistCreateDirectory(pathToRemoved,ANA,ALT)
        for person in persons.items():
            print(str(person) +" üzerinde işlemler başlatıldı")
            randoms = []
            print("random sayılar üretiliyor")
            for x in range(0, 64):
                while True:
                    rndm =random.randint(600,person[1])
                    if rndm % 2 == 0 and (not rndm in randoms):
                        randoms.append(rndm)
                        break
            log("random sayılar üretildi")
            log(randoms)
            log("random dosyalar kopyalanmaya başlandı")
            sayac = 1
            for rndm in randoms:
                shutil.copyfile(pathMain+"\\"+ANA+"\\"+ALT+"\\"+(person[0]+"-"+str(rndm)+".jpg"),pathToSelected+"\\"+ANA+"\\"+ALT+"\\"+(person[0]+"-"+str(sayac)+".jpg"))
                sayac+=1
            log("random dosyalar kopyalandı")
            sayac=1
            log("600'den büyük dosyalar kopyalanmaya başlandı")
            for i in range(600,person[1],2):
                shutil.copyfile(pathMain+"\\"+ANA+"\\"+ALT+"\\"+(person[0]+"-"+str(i)+".jpg"),pathToRemoved+"\\"+ANA+"\\"+ALT+"\\"+(person[0]+"-"+str(sayac)+".jpg")) 
                sayac+=1
            log("600'den büyük dosyalar kopyalandı")
        log("ALT klasörünün başına - koyuluyor")
        os.rename(pathMain+"\\"+ANA+"\\"+ALT,pathMain+"\\"+ANA+"\\-"+ALT)
    log("ANA klasörünün başına - koyuluyor")
    os.rename(pathMain+"\\"+ANA,pathMain+"\\-"+ANA)



