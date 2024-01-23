#==========================================io.py==========================================
#=========================================LIBRARYS=========================================
from libs.verification import password_validate


#=======================================GET VALUE METHODES=======================================
# Get a Value
def get_value(message) -> str:
    return input(message).strip()


#=======================================PASSWORD METHODES=======================================
# Get a Password and check if it is strong enough
def get_password() -> str:
    password = input("password: ")
    if not list(password_validate(password)):
        if password == input("confirm password: "):
            #ADD Code Later (save hashed password in DB)
            return password
        else: print("passwords do not match, try again.")
    else:
        print(list(password_validate(password)))
        print("password is incoocrect")
