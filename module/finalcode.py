import random
from time import gmtime, strftime
import requests
import os
import time

Entrance='En'
Exit='Ex'

exOrEn=''
exOrEnTime=''
timefull=''
ranCarNo=0
status=''

carSerialNumber=0
currentTotalCarRoadLeft=0
currentTotalCarRoadRight=0
currentTotalCarSideRoadLeft=0
currentTotalCarSideRoadRight=0
presentCarsRoadLeft=[]
presentCarsRoadRight=[]
presentCarsSideRoadLeft=[]
presentCarsSideRoadRight=[]
parkCars=[]
hospitalCars=[]
marketCars=[]
exitCarsFromRoad=[]


#RFID TAG INFORMATION
#C1 : 3147309542 Entrance
#C2 : 2055509328 Exit
#C3 : 3148514150
#C4 : 2055531952

def enOrExCarData(gpio_port, tagId):
    global carSerialNumber
    global currentTotalCarRoadLeft
    global currentTotalCarRoadRight
    global currentTotalCarSideRoadLeft
    global currentTotalCarSideRoadRight
    global presentCarsRoadLeft
    global presentCarsRoadRight
    global parkCars
    global hospitalCars
    global marketCars
    global exOrEn
    global ranCarNo
    global exOrEnTime
    global timefull
    global status
    global exitCarsFromRoad



    
    if(tagId=='3147309542'):
        #first card main road entrance from outside
        carSerialNumber = carSerialNumber + 1
        #cars are entering from two directions, thats why two arrays to identify their entrance path
        a = random.randrange(1, 3)
        # print(a)
        if a == 1:
            presentCarsRoadLeft.append(carSerialNumber)
            currentTotalCarRoadLeft = currentTotalCarRoadLeft + 1
        elif a == 2:
            presentCarsRoadRight.append(carSerialNumber)
            currentTotalCarRoadRight = currentTotalCarRoadRight + 1 #use less i can use len here. later i will use that, for now its ok

        carEnTime = int(time.time()*1000)#strftime("%H:%M:%S", gmtime())
        timefull = strftime("%H:%M:%S", gmtime())
        exOrEnTime=carEnTime
        exOrEn=Entrance
        ranCarNo=carSerialNumber
        status = exOrEn + '\t' + str(ranCarNo) + '\t' + str(currentTotalCarRoadLeft) + '\t' + str(currentTotalCarRoadRight) + '\t' + str(carEnTime) + '\t' + str(currentTotalCarSideRoadLeft) + '\t' + str(currentTotalCarSideRoadRight) + '\t' + str(len(marketCars)) + '\t' + str(len(hospitalCars)) + '\t' + str(len(parkCars))
        writeCarMovement(status)

    elif(tagId=='2055509328'):
        #second card for main road to side road entrance

        a = random.randrange(1, 3)
        # print(a)
        if a == 1:
            ran = random.choice(presentCarsRoadLeft)
            presentCarsRoadLeft.remove(ran)
            currentTotalCarRoadLeft = currentTotalCarRoadLeft - 1
            presentCarsSideRoadLeft.append(ran)
            currentTotalCarSideRoadLeft +=1

        elif a == 2:
            ran = random.choice(presentCarsRoadRight)
            presentCarsRoadRight.remove(ran)
            currentTotalCarRoadRight = currentTotalCarRoadRight - 1
            presentCarsSideRoadRight.append(ran)
            currentTotalCarSideRoadRight += 1

        carExTime = int(time.time()*1000)
        timefull = strftime("%H:%M:%S", gmtime())
        exOrEnTime=carExTime
        exOrEn=Exit
        ranCarNo=ran
        status = exOrEn + '\t' + str(ran) + '\t' + str(currentTotalCarRoadLeft) + '\t' + str(currentTotalCarRoadRight) + '\t' + str(carExTime) + '\t' + str(currentTotalCarSideRoadLeft) + '\t' + str(currentTotalCarSideRoadRight) + '\t' + str(len(marketCars)) + '\t' + str(len(hospitalCars)) + '\t' + str(len(parkCars))
        writeCarMovement(status)

    elif(tagId=='3148514150'):
        #third card entrance to park or hospital or market

        carPlace=''
        carExTime = int(time.time()*1000)#strftime("%H:%M:%S", gmtime())
        timefull = strftime("%H:%M:%S", gmtime())
        exOrEnTime=carExTime
        a = random.randrange(1,5)
        #print(a)
        if a==1 :
            ran = random.choice(presentCarsRoadRight)
            presentCarsRoadRight.remove(ran)
            currentTotalCarRoadRight -=1
            parkCars.append(ran)
            carPlace='Pa'

        elif a==2 :
            ran = random.choice(presentCarsRoadRight)
            presentCarsRoadRight.remove(ran)
            currentTotalCarRoadRight -= 1
            hospitalCars.append(ran)
            carPlace = 'Ho'

        elif a==3 :
            ran = random.choice(presentCarsRoadLeft)
            presentCarsRoadLeft.remove(ran)
            currentTotalCarRoadLeft -= 1
            marketCars.append(ran)
            carPlace = 'Ma'
        elif a==4 :
            ran = random.choice(presentCarsSideRoadLeft)
            presentCarsSideRoadLeft.remove(ran)
            currentTotalCarSideRoadLeft -= 1
            marketCars.append(ran)
            carPlace = 'Ma'

        exOrEn=carPlace
        ranCarNo=ran
        status = exOrEn + '\t' + str(ran) + '\t' + str(currentTotalCarRoadLeft) + '\t' + str(currentTotalCarRoadRight) + '\t' + str(carExTime) + '\t' + str(currentTotalCarSideRoadLeft) + '\t' + str(currentTotalCarSideRoadRight) + '\t' + str(len(marketCars)) + '\t' + str(len(hospitalCars)) + '\t' + str(len(parkCars))



        writeCarMovement(status)

    elif(tagId=='2055531952'):

        exitLeftOrRight = random.randrange(1, 3)#exit from main left road or main right road
        if exitLeftOrRight == 1:
            #LeftRoad
            exitRoadOrEntrance = random.randrange(1, 4) #exit from main road to outside or entrance from market to side road or entrance from side road to main left road
            if exitRoadOrEntrance == 1:
                # exit from main road to outside
                ran = random.choice(presentCarsRoadLeft)
                presentCarsRoadLeft.remove(ran)
                currentTotalCarRoadLeft = currentTotalCarRoadLeft - 1

                exitCarsFromRoad.append(ran)
                exOrEn = 'Ex'


            elif exitRoadOrEntrance == 2:
                # exit from market to side road
                ran = random.choice(marketCars)
                marketCars.remove(ran)
                presentCarsSideRoadLeft.append(ran)
                currentTotalCarSideRoadLeft +=1
                exOrEn = 'En'

            elif exitRoadOrEntrance == 3:
                # exit from side road to main road left
                ran = random.choice(presentCarsSideRoadLeft)
                presentCarsSideRoadLeft.remove(ran)
                currentTotalCarSideRoadLeft -= 1
                presentCarsRoadLeft.append(ran)
                currentTotalCarRoadLeft +=1
                exOrEn = 'En'


        elif exitLeftOrRight == 2:
            #RightRoad
            exitRoadOrEntrance = random.randrange(1,5)  # exit from main road to outside or entrance from market to side road or entrance from side road to main left road
            if exitRoadOrEntrance == 1:
                # exit from main road to outside
                ran = random.choice(presentCarsRoadRight)
                presentCarsRoadRight.remove(ran)
                currentTotalCarRoadRight = currentTotalCarRoadRight - 1

                exitCarsFromRoad.append(ran)
                exOrEn = 'Ex'


            elif exitRoadOrEntrance == 2:
                # exit from park to side road
                ran = random.choice(parkCars)
                parkCars.remove(ran)
                presentCarsRoadRight.append(ran)
                currentTotalCarRoadRight += 1
                exOrEn = 'En'

            elif exitRoadOrEntrance == 3:
                # exit from side road to main road left
                ran = random.choice(presentCarsSideRoadRight)
                presentCarsSideRoadRight.remove(ran)
                currentTotalCarSideRoadRight -= 1
                presentCarsRoadRight.append(ran)
                currentTotalCarRoadRight += 1
                exOrEn = 'En'

            elif exitRoadOrEntrance == 4:
                # exit from hospital to side road
                ran = random.choice(hospitalCars)
                hospitalCars.remove(ran)
                presentCarsSideRoadRight.append(ran)
                currentTotalCarSideRoadRight += 1
                exOrEn = 'En'



        carEnTime = int(time.time()*1000)#strftime("%H:%M:%S", gmtime())
        timefull = strftime("%H:%M:%S", gmtime())
        exOrEnTime=carEnTime
        ranCarNo=ran

        status = exOrEn + '\t' + str(ran) + '\t' + str(currentTotalCarRoadLeft) + '\t' + str(
        currentTotalCarRoadRight) + '\t' + str(carEnTime) + '\t' + str(currentTotalCarSideRoadLeft) + '\t' + str(
        currentTotalCarSideRoadRight) + '\t' + str(len(marketCars)) + '\t' + str(len(hospitalCars)) + '\t' + str(
        len(parkCars))
        #have to change entrance value based on choice

        writeCarMovement(status)



    #show data
    #showCarData(status)

def showCarData(status):
    #print(presentCarsRoadLeft)
    print(' ')
    #print(status)
    #print(marketCars)
    #print(parkCars)
    #print( hospitalCars)
    #print(exitCarsFromRoad)

    #print status
    #print cars

def closeConnection():
    #print 'Program Stopped'
    print('Program Stopped')


def writeCarMovement(status):
    insertIntoDatabase()
    #writing file
    with open("cardata.txt",'a')as data:
         data.write(status)
         data.write('\n')



def insertIntoDatabase():
    # inserting into database
    ##http://localhost/wsn/welcome_get.php?name=y&email=56
    # url = 'http://localhost/wsn/welcome_get.php?name=y&email=' + status + "'"

    #url = 'http://localhost/wsn/welcome_get.php?name=y&enorextime=15:26:25'
    #r = requests.get(url)

    global carSerialNumber
    global currentTotalCarRoadLeft
    global currentTotalCarRoadRight
    global currentTotalCarSideRoadLeft
    global currentTotalCarSideRoadRight
    global presentCarsRoadLeft
    global presentCarsRoadRight
    global presentCarsSideRoadLeft
    global presentCarsSideRoadRight
    global parkCars
    global hospitalCars
    global marketCars
    global exOrEn
    global exOrEnTime
    global ranCarNo
    global timefull
    global status 
    global exitCarsFromRoad 

    #mc=len(marketCars)
    #hc = len(hospitalCars)
    #pc = len(parkCars)
    #print(mc)
    #print(hc)
    #print(pc)
    print('=====================================================================================')
    print(status) 
    print('Number of Cars in Left Main Road: '+str(currentTotalCarRoadLeft))
    print ('Present Cars in Left Main Road: '+str(presentCarsRoadLeft))
    
    print('Number of Cars in Right Main Road: '+str(currentTotalCarRoadRight))
    print('Present Cars in Right Main Road: '+str(presentCarsRoadRight))

    print('Number of Cars in Left Side Road: '+str(currentTotalCarSideRoadLeft))
    print('Present Cars in Left Side Road: '+str(presentCarsSideRoadLeft))

    print('Number of Cars in Right Side Road: '+str(currentTotalCarSideRoadRight))
    print('Present Cars in Right Side Road: '+str(presentCarsSideRoadRight))

    print('Number of Cars in Market: '+str(len(marketCars)))
    print('Market Cars: '+str(marketCars))

    print('Number of Cars in Hospital: '+str(len(hospitalCars)))
    print('Hospital Cars: '+str(hospitalCars))

    print('Number of Cars in Park: '+str(len(parkCars)))
    print('Park Cars: '+str(parkCars))

    print('Number of Exit Cars: '+str(len(exitCarsFromRoad)))
    print('Exit Cars: '+str(exitCarsFromRoad))
    
    

    data='enorex='+exOrEn+'&'+'carno='+str(ranCarNo)+'&'+'currentTotalCarRoadLeft='+str(currentTotalCarRoadLeft)+'&'+'currentTotalCarRoadRight='+str(currentTotalCarRoadRight)\
         +'&'+'enorextime='+str(exOrEnTime)+'&'+'currentTotalCarSideRoadLeft='+str(currentTotalCarSideRoadLeft)+'&'+'currentTotalCarSideRoadRight='+str(currentTotalCarSideRoadRight)\
         +'&'+'marketCarsLen='+str(len(marketCars))+'&'+'hospitalCarsLen='+str(len(hospitalCars))+'&'+'parkCarsLen='+str(len(parkCars))+'&'+'timefull='+str(timefull)

    url = 'http://192.168.0.11/wsn/welcome_get.php?'+data
    r = requests.get(url)
    #print(url)

    #status = exOrEn + '\t' + str(ranCarNo) + '\t' + str(currentTotalCarRoadLeft) + '\t' + str(
        #currentTotalCarRoadRight) + '\t' + str(ranCarNo) + '\t' + str(currentTotalCarSideRoadLeft) + '\t' + str(
        #currentTotalCarSideRoadRight) + '\t' + str(len(marketCars)) + '\t' + str(len(hospitalCars)) + '\t' + str(
        #len(parkCars))
