import time
import picamera
import RPi.GPIO as gpio
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage 
from email.mime.multipart import MIMEMultipart

# Define email addresses to use
addr_to   = '101cookie.m.123.8910@gmail.com'
addr_from = '101cookie.m.123.8910@gmail.com'

#Define server and login details
smtp_server = 'smtp.gmail.com:587'
smtp_user   = '101cookie.m.123.8910@gmail.com'
smtp_pass   = 'notallowedtoknowm9'


gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(7,gpio.IN) #MD

gpio.setup(3,gpio.OUT) #RED (ALL CLEAR)
gpio.setup(5,gpio.OUT) #GREEN (MOTION DETECTED)
gpio.setup(11,gpio.OUT) #YELLOW (TAKING PICS)

gpio.output(3,0)
gpio.output(5,0)
gpio.output(11,0)
while True:
        try:
                cooldown=int(input("INITIALISATION PERIOD: "))
                break
        except:
                print("\n<PERIOD MUST BE AN INTEGER>")
location = input ("State the area RaspPi is Located: \n[THEN PRESS <<ENTER>> TO INITIATE PROGRAM]: ")
print("PROGRAM STARTING IN...")
while cooldown > 0:
        print("\n"+str(cooldown))
        cooldown = int(cooldown)-1
        gpio.output(3,1)
        gpio.output(5,1)
        gpio.output(11,1)
        time.sleep(0.5)
        gpio.output(3,0)
        gpio.output(5,0)
        gpio.output(11,0)
        time.sleep(0.5)
        
print("\n*PROGRAM INITIATED: ON STANDBY*")
def motion_detect():
	try:
		while True:
			if gpio.input(7)==1:
				gpio.output(3,0)
				gpio.output(5,1)
				print("Motion Detected")
				print("Capturing Images...")
				with picamera.PiCamera() as camera:
                                        try:
                                                camera.start_preview()
                                                gpio.output(11,1)
                                                name1 = time.ctime()
                                                print ("Capturing IMAGE 1")
                                                camera.capture('/home/pi/Desktop/MDimages/'+name1+'.jpg')
                                                print('Captured IMAGE 1 at "'+name1+'. Ready and Waiting for Sending..."')
                                                gpio.output(11,0)
                                                time.sleep(2)
                                                gpio.output(11,1)
                                                name2=time.ctime()
                                                print ("Capturing IMAGE 2")
                                                camera.capture('/home/pi/Desktop/MDimages/'+name2+'.jpg')
                                                print('Captured IMAGE 2 at "'+name2+'. Ready and Waiting for Sending..."')
                                                
                                                gpio.output(11,0)
                                                camera.stop_preview()
                                                print("All Images Successfully Captured")
					except:
                                                print("\n--ERROR-Image Captures Unsuccessful--\n")
                                        
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
                                                messagee="<p>Motion Detected in "+location+". Two Pictures Taken:</p>"
                                                date = '<p>'+time1+'</p>'
                                                copy = '<p>Copywrite &copy; James Cook 2014</p>'
                                                msg_content = '<h2>SENT_FROM_RaspPi: <font color="red">'+tittle+'</font></h2>'.format()
                                                msg.attach(MIMEText((msg_content+messagee+date+copy), 'html'))
                                        except:
                                                print("\n--ERROR-Couldn't Construct E-mail Message--\n")
                                                
                                        try:
                                                #Attach Images
                                                fb=open("/home/pi/Desktop/MDimages/"+name1+".jpg",'rb')
                                                img = MIMEImage(fb.read())
                                                fb.close()
                                                msg.attach(img)
                                                fb=open("/home/pi/Desktop/MDimages/"+name2+".jpg",'rb')
                                                img = MIMEImage(fb.read())
                                                fb.close()
                                                msg.attach(img)
                                        except:
                                                print("\n--ERROR-Couldn't Attach Images--\n")
                                        
                                        try:          
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
                                        except:
                                                ("\n--ERROR-Couldn't Connect to Server--\n")
                                        #Cooldown
                                        sn = 5
                                        print ("\nCOOLDOWN PERIOD:\nReturning to Standby in...")
                                        while sn > 0:
                                                print("\n"+str(sn))
                                                sn = int(sn)-1
                                                gpio.output(5,1)
                                                time.sleep(0.5)
                                                gpio.output(5,0)
                                                time.sleep(0.5)
                                        print("\n*PROGRAM ON STANDBY*")
                                        gpio.output(5,0)
			else:
				print ("-ALL CLEAR-")
				time.sleep(0.1)
				gpio.output(3,1)
	except KeyboardInterrupt:
		gpio.cleanup()
		print ("\n\n*Program Terminated by User*")
	except:
		print("\n\nERROR-Program Terminated")
		gpio.cleanup()

if __name__ == "__main__":
	motion_detect()


