import cv2

class mphands:
    import mediapipe as mp
    def __init__(self,maxhands=2,tol1=0.5,tol2=0.5):
        self.hands=self.mp.solutions.hands.Hands(False,maxhands,tol1,tol2)
    def Marks(self,frame):
        myhands=[]
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landmark in handLandMarks.landmark:
                    myHand.append((int(landmark.x*width),int(landmark.y*height)))
                myhands.append(myHand)
        return myhands


width=640
height=360
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
findhands=mphands(1)
paddleweidth=125
paddleheight=25
ballradius=10
xpos=int(width/2)
ypos=int(height/2)
deltax=2
deltay=2
score=0
lives=5
font=cv2.FONT_HERSHEY_COMPLEX
ind=8


while True:
    ignore, frame = cam.read()   #to grab single frame of video
    
    handdata=findhands.Marks(frame)
    cv2.circle(frame,(xpos,ypos),ballradius,(0,0,255),-1)
    cv2.putText(frame,str(score),(25,int(6*paddleheight)),font,6,(255,0,0),5)
    cv2.putText(frame,str(lives),(width-125,int(6*paddleheight)),font,6,(255,0,0),5)
    for hand in handdata:
        cv2.rectangle(frame,(int(hand[8][0]-paddleweidth/2),0),(int(hand[8][0]+paddleweidth/2),paddleheight),(0,255,0),-1)
    topedgeball=ypos-ballradius
    bottomedgeball=ypos+ballradius
    leftedgeball=xpos-ballradius
    rightedgeball=xpos+ballradius
    if leftedgeball<=0 or rightedgeball>=width:
        deltax=deltax*(-1)
    if bottomedgeball>=height:
        deltay=deltay*(-1)
    
    if topedgeball<=paddleheight:
        if xpos>=int(hand[ind][0]-paddleweidth/2) and xpos<int(hand[ind][0]+paddleweidth/2):
            deltay=deltay*(-1)
            score=score+1
            if score==1 or score==10 or score==15:
                deltax=deltax*2
                deltay=deltay*2
        else:
            xpos=int(width/2)
            ypos=int(height/2)
            lives=lives-1
    xpos=xpos+deltax
    ypos=ypos+deltay
    cv2.imshow('my WEBcam',frame)
    cv2.moveWindow('my WEBcam' , 0 ,0)
    if lives==0:
        break
    if cv2.waitKey(1) & 0xff == ord('q'):
        break 
cam.release()    