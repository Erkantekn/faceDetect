import os
import datetime


constW=228
constH=228
path = "D:\\Tez\\-data"
def clearPrefix():
    for mainDir in os.listdir(path):
        if mainDir!="-data" and mainDir!="data" and mainDir!="TESTT" and mainDir!="TESTT" and mainDir!="LOG.txt" and mainDir!="-LOG.txt" :
            for childDir in os.listdir(path+"\\"+mainDir):
                for vid in os.listdir(path+"\\"+mainDir+"\\"+childDir):
                    if(vid[0]=="-"):
                        os.rename(path+"\\"+mainDir+"\\"+childDir+"\\"+vid,path+"\\"+mainDir+"\\"+childDir+"\\"+vid[1:len(vid)])
                if(childDir[0]=="-"):
                    os.rename(path+"\\"+mainDir+"\\"+childDir,path+"\\"+mainDir+"\\"+childDir[1:len(childDir)])
            if(mainDir[0]=="-"):
                os.rename(path+"\\"+mainDir,path+"\\"+mainDir[1:len(mainDir)])
clearPrefix()