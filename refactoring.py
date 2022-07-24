"""Мы устроились на новую работу. Бывший сотрудник начал разрабатывать модуль
 для работы с почтой, но не успел доделать его. Код рабочий. Нужно только провести рефакторинг кода.

Создать класс для работы с почтой;
Создать методы для отправки и получения писем;
Убрать "захардкоженный" код. Все значения должны определяться как аттрибуты класса, либо аргументы методов;
Переменные должны быть названы по стандарту PEP8;
Весь остальной код должен соответствовать стандарту PEP8;
Класс должен инициализироваться в конструкции."""

import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Gmail:
    GMAIL_SMTP = "smtp.gmail.com"
    GMAIL_IMAP = "imap.gmail.com"

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.header = None

    def send_message(self, recipients_, subject_, body_):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.login
            msg['To'] = ', '.join(recipients_)
            msg['Subject'] = subject_
            msg.attach(MIMEText(body_))

            # подключаемся к почтовому сервису
            ms = smtplib.SMTP(self.GMAIL_SMTP, 587)
            ms.starttls()
            ms.ehlo()
            # логинимся на почтовом сервере
            ms.login(self.login, self.password)
            # пробуем послать письмо
            result = ms.sendmail(self.login, msg['To'], msg.as_string())
            return result
        except smtplib.SMTPException as err:
            print('Что - то пошло не так...')
            raise err

        finally:
            ms.quit()

    def recieve(self, folder='inbox'):
        try:
            mail = imaplib.IMAP4_SSL(self.GMAIL_IMAP, 993)
            mail.login(self.login, self.password)
            mail.list()
            mail.select(folder)
            criterion = '(HEADER Subject "%s")' % self.header if self.header else 'ALL'
            result, data = mail.uid('search', None, criterion)
            assert data[0], 'There are no letters with current header'
            latest_email_uid = data[0].split()[-1]
            result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = data[0][1]
            email_message = email.message_from_string(raw_email)
            mail.logout()
            return email_message
        except Exception as err:
            print('Что - то пошло не так...')
            raise err


if __name__ == '__main__':
    gmail = Gmail('login@gmail.com', 'qwerty')
    res_send = gmail.send_message(['vasya@email.com', 'petya@email.com'], 'Test', 'Body message')
    res_recieve = gmail.recieve()
