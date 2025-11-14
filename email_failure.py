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
admin = ""

with open("json/email_data.json") as f:
    data = json.load(f)
    print(data)
    recipients = data["recipients"] + ["negveg@blair.edu"]
    classroom = data["classroom"]
    teacher_name = data["teacher_name"]
    admin = data["admin"]
    
if len(recipients) == 0:
    print("JSON failure")
print(recipients)

sender = "notes.scanner.blair@gmail.com"
password = "ohxo qbav dnna vtzb"

client_msg = MIMEMultipart()
client_msg["From"] = sender
client_msg["To"] = ", ".join(recipients)
client_msg["Subject"] = f"NoteScanner failure in {classroom}"

client_msg_content = f"""
Good {greeting} {teacher_name},

Unfortunately, there has been a problem detected with the NoteScanner in {classroom}. We greatly apologize for the inconvenience and can assure you that it will be fixed promptly.

Sincerely,

NoteScanner1.0
"""

client_msg.attach(MIMEText(client_msg_content, "plain"))
print(client_msg)

# To tech support
msg = MIMEMultipart()
msg["From"] = sender
msg["To"] = admin
msg["Subject"] = f"NoteScanner failure in {classroom}"

msg_content = f"""
NoteScanner unit failure in {classroom} ({teacher_name})
"""

msg.attach(MIMEText(msg_content, "plain"))
print(msg)

with open("log.txt", "rb") as f:
    part = MIMEApplication(f.read(), _subtype="txt")
    part.add_header("Content-Disposition", "attachment", filename="log.txt")
    msg.attach(part)
    
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(sender, password)

server.sendmail(sender, recipients, client_msg.as_string())
server.sendmail(sender, admin, msg.as_string())

server.quit()
    
