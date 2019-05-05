import bcrypt


class EncryptionManager:

    def __init__(self):
        pass

    def GenerateSalt(self):
        salt = bcrypt.gensalt(12)
        return salt

    def EncryptMessage(self, message, encryptKey):
        pass

    def DecryptMessage(self, message, encryptKey):
        pass


