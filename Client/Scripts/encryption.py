import bcrypt
from Scripts import jsonIO


class EncryptionManager:

    def __init__(self, serverSocket):
        self.serverSocket = serverSocket

        self.plaintextPassword = ''
        self.salt = ''
        self.hashedPassword = ''

        self.username = ''

        # Key used to encrypt and decrypt messages. Sent from server.
        self.encryptionKey = ''

    # Takes a plaintext password and salt and creates a salted, hashed password.
    def SaltAndHashPassword(self, password):

        plainTextPassword = password.encode("utf-8")

        salt = bcrypt.gensalt(12)

        # Hash the salted password
        hashedPassword = bcrypt.hashpw(plainTextPassword, salt)

        hashedPassword = hashedPassword.decode()

        print("Hashed password generated.")
        return hashedPassword

    def VerifyPassword(self, correctPass):
        result = bcrypt.checkpw(self.plaintextPassword.encode('utf-8'), bytes(correctPass, 'utf-8'))

        if result is True:
            jsonIO.JsonIO.Output(self.serverSocket, "##LoginPassVerified " + self.username)

        else:
            jsonIO.JsonIO.Output(self.serverSocket, "##LoginPassRejected " + self.username)

    def EncryptMessage(self, message, encryptKey):
        pass

    def DecryptMessage(self, message, encryptKey):
        pass
