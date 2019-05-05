import bcrypt


class EncryptionManager:

    def __init__(self, serverSocket):
        self.serverSocket = serverSocket

        self.plaintextPassword = ''
        self.salt = ''
        self.hashedPassword = ''

        # Key used to encrypt and decrypt messages. Sent from server.
        self.encryptionKey = ''

    # Takes a plaintext password and salt and creates a salted, hashed password.
    def SaltAndHashPassword(self, password):

        plainTextPassword = password.encode("utf-8")

        salt = bcrypt.gensalt(12)

        # Hash the salted password
        hashedPassword = bcrypt.hashpw(plainTextPassword, salt)

        hashedPassword.decode()

        print("Hashed password generated.")
        return hashedPassword

    def EncryptMessage(self, message, encryptKey):
        pass

    def DecryptMessage(self, message, encryptKey):
        pass
