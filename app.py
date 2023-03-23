import imaplib


class DeletMails:
    def __init__(self, username, mail_pass):
        imap_server = "imap.mail.ru"
        self.imap = imaplib.IMAP4_SSL(imap_server)
        self.imap.login(username, mail_pass)

    def DeleteRareMails(self):
        self.imap.select("INBOX")
        _, unread_msgs = self.imap.search(None, "UNSEEN")
        set_of_unseen = set(unread_msgs[0].split())
        list_of_users = set()
        for num in unread_msgs[0].split():
            typ, data = self.imap.fetch(num, "ENVELOPE")
            list_of_users.add(data[0].split())
        for name in list_of_users:
            _, message = self.imap.search(None, f'FROM {name[0]}')
            message = message[0].split(b' ')
            count = 0
            stop = False
            for letter in message:
                if letter in set_of_unseen:
                    count += 1
                else:
                    stop = True
                    break
            if not stop and count >= 15:
                self.imap.store(name, '+FLAGS', '\\Deleted')
                self.imap.expunge()

    def __exit__(self):
        self.imap.close()
        self.imap.logout()


