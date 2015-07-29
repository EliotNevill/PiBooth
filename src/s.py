#Import Modules
import time, picamera, pygame, RPi.GPIO as gpio, smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage 
from email.mime.multipart import MIMEMultipart

#Define Functions
def play(file):
        pygame.mixer.init()
        pygame.mixer.music.load("/home/pi/scotsman/"+file+".mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

def green(status):
        gpio.output(5,status)
def red(status):
        gpio.output(3,status)
def yellow(status):
        gpio.output(11,status)

def countdown(cooldown):
        try:
                while cooldown > 0:
                        red(1)
                        green(1)
                        yellow(1)
                        print("\n"+str(cooldown))
                        pygame.mixer.init()
                        yep = str(cooldown)
                        play(yep)
                        red(0)
                        green(0)
                        yellow(0)
                        cooldown = int(cooldown)-1
                        time.sleep(0.1)
        except KeyboardInterrupt:
                play("TerminatedUser")
                print("\n\n*Program Terminated By User*")
                exit(1)
        
play("welcome")
play("ButtonWhenR")
# Define email addresses to use
addr_to   = '101cookie.m.123.8910@gmail.com'
addr_from = '101cookie.m.123.8910@gmail.com'

#Define server and login details
smtp_server = 'smtp.gmail.com:587'
smtp_user   = '101cookie.m.123.8910@gmail.com'
smtp_pass   = 'pitest123'

#Setup GPIO pins
gpio.setwarnings(False)

gpio.setmode(gpio.BOARD)
gpio.setup(7,gpio.IN) #MD
gpio.setup(37, gpio.IN) #BUTTON

gpio.setup(3,gpio.OUT) #RED (NOT BUSY)
gpio.setup(5,gpio.OUT) #GREEN (BUSY)
gpio.setup(11,gpio.OUT) #YELLOW (TAKING PICS)

red(0)
green(0)
yellow(0)

#GeoLocation
location = "The Studio: Room 10"#input ("State the area RaspPi is Located: ")

print("<<Press and Hold Button to Initialise Program>>")

while True:
    input_value = gpio.input(37)
    if input_value == True:
        while input_value == True:
                input_value = gpio.input(37)
                yellow(1)
                time.sleep(0.05)
                red(1)
                time.sleep(0.05)
                green(1)
                time.sleep(0.1)
                green(0)
                time.sleep(0.05)
                red(0)
                time.sleep(0.05)
                yellow(0)
                time.sleep(0.1)
    else:
            break

play("InitIn")
print("PROGRAM STARTING IN...")
countdown(3)
      
print("\n*PROGRAM INITIATED: ON STANDBY*")
play("ProgramReady")
def motion_detect():
        while True:
                try:
                        repeat = 101
                        input_value = gpio.input(37)
                        print ("-WAITING FOR BUTTON PRESS-")
                        if input_value == True:
                                while input_value == True:
                                        if repeat > 100:
                                                play("PictureTaken")
                                                repeat=0
                                        input_value = gpio.input(37)
                                        red(1)
                                        repeat = repeat+0.0004
                        print("Button Pressed")
                        play("welcome")
                        red(0)
                        green(1)
                        play("WhenMotion")
                        play("MotionToCapture")
                        print("-WAITING FOR MOTION DETECTION-")
                        while True:
                                if gpio.input(7)==1:
                                        print("Motion Detected")
                                        print("Capturing Images...")
                                        play("MotionD")
                                        with picamera.PiCamera() as camera:
                                                try:
                                                        camera.start_preview()
                                                        countdown(5)
                                                        yellow(1)
                                                        name1 = time.ctime()
                                                        print ("Capturing IMAGE 1")
                                                        camera.capture('/home/pi/Desktop/MDimages/'+name1+'.jpg')
                                                        print('Captured IMAGE 1 at "'+name1+'. Ready and Waiting for Sending..."')
                                                        yellow(0)
                                                        camera.stop_preview()
                                                        print("Image Successfully Captured")
                                                except:
                                                        print("\n--ERROR-Image Captures Unsuccessful--\n")
                                                        play("SorryError")
                                                        
                                                try:
                                                        # Construct email PART 1
                                                        print ("Constructing Email...")
                                                        msg = MIMEMultipart()
                                                        msg['To'] = addr_to
                                                        msg['From'] = addr_from
                                                        msg['Subject'] = 'MOTION DETECTED'

                                                        #PART 2
                                                        time1=time.ctime()
                                                        tittle="Motion Detected in "+location
                                                        messagee="<p>Motion Detected in "+location+". One Picture Taken:</p>"
                                                        date = '<p>'+time1+'</p>'
                                                        copy = '<p>Copywrite &copy; James Cook 2014</p>'
                                                        msg_content = '<h2>SENT_FROM_RaspPi: <font color="red">'+tittle+'</font></h2>'.format()
                                                        msg.attach(MIMEText((msg_content+messagee+date+copy), 'html'))
                                                except:
                                                        print("\n--ERROR-Couldn't Construct E-mail Message--\n")
                                                        play("SorryError")
                                                                
                                                try:
                                                        #Attach Images
                                                        fb=open("/home/pi/Desktop/MDimages/"+name1+".jpg",'rb')
                                                        img = MIMEImage(fb.read())
                                                        fb.close()
                                                        msg.attach(img)
                                                except:
                                                        print("\n--ERROR-Couldn't Attach Images--\n")
                                                        play("SorryError")
                                                        
                                                try:
                                                        play("Sending")
                                                        # Send the message via an SMTP server
                                                        print ("Defining Server")
                                                        s = smtplib.SMTP(smtp_server)
                                                        print("Connecting to Server")
                                                        s.ehlo()
                                                        s.starttls()
                                                        print ("Logging in")
                                                        s.login(smtp_user,smtp_pass)
                                                        print ("Server Connection and Loggin Successful")
                                                        print ("Sending E-mail Message to Admin")
                                                        s.sendmail(addr_from, addr_to, msg.as_string())
                                                        print("Message Sent Successfully")
                                                        s.quit()
                                                        print("Disconnected from Server")
                                                        play("PicSent")
                                                except:
                                                        print("\n--ERROR-Couldn't Connect to Server--\n")
                                                        play("Error")
                                                #Cooldown
                                                play("InitIn")
                                                print ("\nCOOLDOWN PERIOD:\nReturning to Standby in...")
                                                countdown(3)
                                                print("\n*PROGRAM ON STANDBY*")
                                                green(0)
                                                break
                                else:
                                      if repeat == 100:
                                              play("MotionToCapture")
                              
                                      else:
                                              repeat=repeat+0.005
                except KeyboardInterrupt:
                        gpio.cleanup()
                        print ("\n\n*Program Terminated by User*")
                        play("TerminatedUser")
                        exit(1)
                except:
                        print("\n\nERROR-Program Terminated")
                        gpio.cleanup()
                        play("SorryError")
                        
if __name__ == "__main__":
	motion_detect()
