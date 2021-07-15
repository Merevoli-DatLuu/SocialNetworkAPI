from django.core.mail import EmailMessage
import threading
import datetime
import base64


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

class EmailSending:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()

def generate_key(email):
    return base64.b32encode((str(email) + "|" + str(datetime.date.today())).encode())