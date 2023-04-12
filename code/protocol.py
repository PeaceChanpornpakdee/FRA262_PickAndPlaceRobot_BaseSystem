class Protocol():
    """
    Protocol Class
    """
    def __init__(self, app):
        self.app = app

    def heartbeat(self):
        print("Read - Heartbeat Protocol")
        if "Ya" == "Ya":
            print("Write - Heartbeat Protocol = Hi")

    def routine(self):
        print("""Read
        Base System Status
        End Effector Status
        y-Axis Moving Status
        x-Axis Moving Status""")
