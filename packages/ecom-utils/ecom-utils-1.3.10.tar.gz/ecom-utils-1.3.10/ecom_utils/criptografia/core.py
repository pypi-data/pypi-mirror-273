from cryptography.fernet import Fernet

class Encript():
    
    def __init__(self, key):
        self.key = key

    def encriptar(self, valor_raw):
        #print(valor_raw, 'valor     ', self.key)
        encriptador = Fernet(self.key)
        token = encriptador.encrypt(bytes(valor_raw, 'utf-8'))
        #print(token)
        return token.decode()
    
    def desencriptar(self, token_decoded):
        token = bytes(token_decoded, 'utf-8')
        encriptador = Fernet(self.key)
        return encriptador.decrypt(token).decode()