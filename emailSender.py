import smtplib
import os
import maskpass
from email.message import EmailMessage

smtphost = 'smtp.gmail.com'
smtpport = 587

def sendEmail(subject, receivers, message):
  smtp_obj = smtplib.SMTP(smtphost, smtpport)
  smtp_obj.starttls()
  smtp_obj.login(os.environ.get('SENDER'), os.environ.get('PASSWORD'))

  attachments_dir = os.environ.get('ATTACHMENTS_DIR') if os.environ.get('ATTACHMENTS_DIR') != "" else ""

  msg = EmailMessage()
  msg['Subject'] = subject
  msg['From'] = os.environ.get('SENDER')
  msg['To'] = receivers
  msg.set_content(message)

  if attachments_dir != "":
    for filename in os.listdir(attachments_dir):
      f = os.path.join(attachments_dir, filename)
      if os.path.isfile(f):
        with open (f, 'rb') as fn:
          file_data = fn.read()
          file_name = fn.name
        msg.add_attachment( file_data, 
                            maintype='application', 
                            subtype='octet-stream',
                            filename=file_name)
  try:
    print("Sending email....")
    smtp_obj.send_message(msg)
  except Exception as err:
    print(err)
    print(f'Problem occured while sending email')
  else:
    print('Email successfully sent!')
  smtp_obj.quit()

def getSenderInfo():
  SENDER = input("Sender email: ")
  PASSWORD = maskpass.askpass("Sender password: ")
  DISPLAY_NAME = input("Sender name: ")
  os.environ["ATTACHMENTS_DIR"] = input("Attachment folder: [all files in the directory will be attached]: ")

  if not [ x for x in (SENDER, PASSWORD, DISPLAY_NAME) if x is None]:
    os.environ["SENDER"] = SENDER
    os.environ["PASSWORD"] = PASSWORD
    os.environ["DISPLAY_NAME"] = DISPLAY_NAME
  else:
    print("Unable to set sender information")

def checkEnv():
  SENDER = os.environ.get('SENDER')
  PASSWORD = os.environ.get('SENDER')
  DISPLAY_NAME = os.environ.get('SENDER')
  ATTACHMENTS_DIR = os.environ.get('ATTACHMENTS_DIR')

  if not [ x for x in (SENDER, PASSWORD, DISPLAY_NAME, ATTACHMENTS_DIR) if x is None]:
    pass
  else:
    getSenderInfo()

if __name__ == "__main__":
  checkEnv()
  sendEmail("Test Subject 2",
            "alan.clintantone1921@gmail.com",
            "Hello Clint, thanks for being nice to me. Continue uploading videos. Please like and subscribe to my YouTube channel :)"
            )