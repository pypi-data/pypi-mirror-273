import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from typing import List, Tuple
from io import BytesIO

class Email():
    """
    Classe com funções para envio de e-mails.

    Argumentos para instanciamento:
    :param string host
    :param port string
    :param user string
    :param password string

    :keyword bool mode_debug
    """
    def __init__(self, host: str, port: str, user: str = None, password: str = None, **kwargs):

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.mode_debug = kwargs.get('mode_debug', None)
        
    def send_email(self, subject: str, email_to: List[str], message: str, files: List[Tuple[str, BytesIO]] = []):
        """
            Função para envio de e-mails.
        """
        try:
            self.server = smtplib.SMTP(host = self.host, port = self.port)
            self.server.ehlo()

            if not self.mode_debug:
                self.server.starttls()
                self.server.login(self.user, self.password)

            email_msg = MIMEMultipart()
            email_msg['From'] = self.user
            email_msg['To'] = ', '.join(email_to)
            email_msg['Subject'] = subject
            email_msg.attach(MIMEText(message, 'html'))

            if files:
                for filename, file in files:
                    excel_attachment = MIMEApplication(file.getvalue())
                    excel_attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                    email_msg.attach(excel_attachment)

            self.server.sendmail(self.user, email_to, email_msg.as_string())
            self.server.quit()
        
        except TypeError as type_error:
            raise TypeError(type_error)
        
        except Exception as e:
            raise Exception(e)


