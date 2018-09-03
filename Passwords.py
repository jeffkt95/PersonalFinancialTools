from getpass import getpass
import keyring

class Passwords:
    def __init__(self):
        self.service_id = "PotsEnvelopeService"
        
    def storePassword(self, username):
        password = getpass("Enter password for " + username + ":\n")
        keyring.set_password(self.service_id, username, password)
        
    def retrievePassword(self, username):
        password = keyring.get_password(self.service_id, username) 
        return password

def main():
    passwords = Passwords()
    passwords.storePassword("jeffkt95@gmail.com")
    password = passwords.retrievePassword("jeffkt95@gmail.com")
    print(password)

if __name__ == "__main__":
    main()
    