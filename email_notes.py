import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime

hour = datetime.now().hour
if hour < 12:
    greeting = "morning"
elif hour < 18:
    greeting = "afternoon"
else:
    greeting = "evening"

recipients = []
classroom = ""
teacher_name = ""

with open("json/email_data.json") as f:
    data = json.load(f)
    print(data)
    recipients = data["recipients"]
    classroom = data["classroom"]
    teacher_name = data["teacher_name"]
    
if len(recipients) == 0:
    print("JSON failure")
print(recipients)

sender = "notes.scanner.blair@gmail.com"
password = "ohxo qbav dnna vtzb"

msg = MIMEMultipart()
msg["From"] = sender
msg["To"] = ", ".join(recipients)
msg["Subject"] = f"Notes from {classroom}"

msg_content = f"""
Good {greeting} {teacher_name},

Attached are the notes from class in {classroom}. If there appear to be any problems with these notes, please do not hesitate to reach out to Gerald Negvesky at negveg@blair.edu or (570) 580-5027. Have a wonderful day.

Sincerely,

NoteScanner1.0
"""
print(msg)
print(msg_content)

msg.attach(MIMEText(msg_content, "plain"))

with open("output.pdf", "rb") as f:
    part = MIMEApplication(f.read(), _subtype="pdf")
    part.add_header("Content-Disposition", "attachment", filename="output.pdf")
    msg.attach(part)
    
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(sender, password)
server.sendmail(sender, recipients, msg.as_string())
server.quit()
    