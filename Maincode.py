import cv2
import mediapipe as mp
from pyfirmata import Arduino
from time import sleep


board = Arduino('COM3')
# Arduino define pins
digitalPins =[4,5,11,7]  

for pins in digitalPins:
    board.digital[pins].write(0)

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)

cap.set(3, wCam)
cap.set(4, hCam)
cap.set(10, 250)#brightness
cap.set(11, 50)#Contrast
cap.set(12, 100)#saturation

class handDetector():
    def __init__(self, mode = False, maxHands = 2, modelComplexity=1,detectionCon=0.75, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, 
										self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
                                
        
    def findHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo = 0, draw = True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 3, (178, 102, 255), cv2.FILLED)
        return lmlist

  

counter, counter1, counter2, counter3 = 0,0,0,0
flag, flag1, flag2, flag3 = 0,0,0,0

detector = handDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    y1, y2 = 15, 80
    grey_color = (211,219,218)
    
    if lmList:

        tip8_x, tip8_y= lmList[8][1], lmList[8][2]  # tracking tip of index finger
        
        #button 1
        if tip8_x > 30 and tip8_x < 90 and tip8_y > 25 and tip8_y < 70:
            counter += 1
            cv2.rectangle(img, (15,y1-5),(105,y2+5), (150,200,150), cv2.FILLED)
            # print("1")
            if counter == 1:
                flag = not flag
        else :
            counter = 0
            if flag: 
                j=0
                while j<7:
                    i=0
                    while i<100999:
                        board.digital[digitalPins[0]].write(1)
                        i=i+1   
                    
                    j=j+1
                board.digital[digitalPins[0]].write(0)
                
                cv2.rectangle(img,(25,y1),(95,y2),(76,138,246),cv2.FILLED)
                cv2.putText(img, "Floor 1", (30, 50), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255), 2)
                flag=not flag
               
            else:
                # board.digital[digitalPins[0]].write(0)
                cv2.rectangle(img,(25,y1),(95,y2), grey_color,cv2.FILLED)
                cv2.putText(img, "Floor 1", (30, 50), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255), 2)
                
        
        #button 2
        if tip8_x > 120 and tip8_x < 180 and tip8_y > 28 and tip8_y < 70:
            counter1 += 1
            cv2.rectangle(img, (105,y1),(195,y2), (150,200,150), cv2.FILLED)
            if counter1 == 1:
                flag1 = not flag1
        else :
            counter1 = 0
            if flag1:
                
                j=0
                while j<3:
                    i=0
                    while i<100999:
                        board.digital[digitalPins[0]].write(1)
                        i=i+1
            
                    j=j+1
                board.digital[digitalPins[0]].write(0)
                
                j=0
                while j<7:
                    i=0
                    while i<100999:
                        board.digital[digitalPins[1]].write(1)
                        i=i+1   
                    
                    j=j+1
                board.digital[digitalPins[1]].write(0)
                
                cv2.rectangle(img,(115,y1),(185,y2),(77,198,254),cv2.FILLED)
                cv2.putText(img, "Floor 2", (120, 50), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255), 2)
                flag1=not flag1
            else:
                # board.digital[digitalPins[1]].write(0)
                cv2.rectangle(img,(115,y1),(185,y2), grey_color,cv2.FILLED)
                cv2.putText(img, "Floor 2", (120, 50), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255), 2)
               
                
        #button 3
        if tip8_x > 210 and tip8_x < 270 and tip8_y > 28 and tip8_y < 70:
            counter2 += 1
            cv2.rectangle(img, (195,y2),(285,y1),(150,200,150), cv2.FILLED)
            if counter2 == 1:
                flag2 = not flag2
        else :
            counter2 = 0
            if flag2:
                j=0
                while j<3:
                    i=0
                    while i<100999:
                        board.digital[digitalPins[0]].write(1)
                        i=i+1
                        
                    j=j+1
                board.digital[digitalPins[0]].write(0)
                
                j=0
                while j<3:
                    i=0
                    while i<100999:
                        board.digital[digitalPins[1]].write(1)
                        i=i+1
            
                    j=j+1
                board.digital[digitalPins[1]].write(0)
                
                j=0
                while j<7:
                    i=0
                    while i<100999:
                        board.digital[digitalPins[2]].write(1)
                        i=i+1   
                    
                    j=j+1
                board.digital[digitalPins[2]].write(0)
                # sleep(1)
                # board.digital[digitalPins[2]].write(0)
                #up=1
                cv2.rectangle(img,(205,y1),(275,y2),(77,198,254),cv2.FILLED)
                cv2.putText(img, "Floor 3", (210, 50), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255), 2)
                flag2=not flag2
                
            else:
                # board.digital[digitalPins[2]].write(0)
                cv2.rectangle(img,(205,y1),(275,y2), grey_color,cv2.FILLED)
                cv2.putText(img, "Floor 3", (210, 50), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255), 2)
                
        #button 4
        if tip8_x > 300 and tip8_x < 360 and tip8_y > 28 and tip8_y < 70:
            counter3 += 1
            cv2.rectangle(img, (285,y1),(375,y2),(150,200,150), cv2.FILLED)
            if counter3 == 1:
                flag3 = not flag3
        else :
            counter3 = 0
            if flag3:
                j=0
                while j<3:
                    i=0
                    while i<100999:
                        board.digital[digitalPins[0]].write(1)
                        i=i+1
                        
                    j=j+1
                board.digital[digitalPins[0]].write(0)
                
                j=0
                while j<3:
                    i=0
                    while i<100999:
                        board.digital[digitalPins[1]].write(1)
                        i=i+1
            
                    j=j+1
                board.digital[digitalPins[1]].write(0)
                
                j=0
                while j<3:
                    i=0
                    while i<100999:
                        board.digital[digitalPins[2]].write(1)
                        i=i+1   
                    
                    j=j+1
                board.digital[digitalPins[2]].write(0)
                
                j=0
                while j<7:
                    i=0
                    while i<100999:
                        board.digital[digitalPins[3]].write(1)
                        i=i+1   
                    
                    j=j+1
                board.digital[digitalPins[3]].write(0)
                
                
               
                cv2.rectangle(img,(295,y1),(365,y2),(77,198,254),cv2.FILLED)
                cv2.putText(img, "Floor 4", (300, 50), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255), 2)
                flag3=not flag3
            else:
                # board.digital[digitalPins[3]].write(0)
                cv2.rectangle(img,(295,y1),(365,y2), grey_color,cv2.FILLED)
                cv2.putText(img, "Floor 4", (300, 50), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255), 2)
                
            
        # Exit button    
        cv2.rectangle(img,(600,y1),(530,y2),(102,102,255),cv2.FILLED)
        cv2.putText(img, "EXIT", (550, 50), cv2.FONT_HERSHEY_PLAIN,1, (255, 255, 255), 2)
        #EXIT by index finger
        cv2.circle(img, (tip8_x, tip8_y), 10, (255, 255, 51), cv2.FILLED)
        if tip8_x > 550 and tip8_x < 590 and tip8_y > 28 and tip8_y < 62:
            cv2.destroyAllWindows()
            cap.release()
            break
        
         
        
    cv2.imshow("Image", img)
    cv2.waitKey(1)
