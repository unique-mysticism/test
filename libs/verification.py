#======================================verification.py======================================
#=========================================LIBRARYS=========================================

# Regular Expression####################
import re

# send_verify_mail librarys#############
import base64
from smtplib import SMTP_SSL
from ssl import create_default_context
from email.message import EmailMessage


#=======================================EMAIL METHODS=======================================
# Validating an Email
def email_validate(email:str, name:str, username:str, password:str, phone_num:str) -> bool|str:
    # Define valid Email Regular Expression
    pattern_gy = r"\b[\w_.+-]+@+(gmail|yahoo)+(.com)$"
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        
    # Verify Email
    if re.match(pattern_gy, email):
        send_verify_mail(email, name, username, password, phone_num)
        return "Check your email.\nAccount created successfully."
    elif re.match(pattern, email):
        return "Account created successfully."
    return False


# Send Email if it is gmail or yahoo (just for more fun!)
def send_verify_mail(email:str, name:str, username:str, password:str, phone_num:str):
    # Define email (sender, receiver,subject, body)
    sender_email = "unique52hertzwhale@gmail.com"
    pemail = base64.b64decode("d3RkbiBnc2R0IHhlbGYganJkZw==").decode("utf-8")
    email_receiver = email
    subject = "Welcom to Mysticism"
    body = f"""
        Hi {name},\n
        Hope you are doing well.\n\n\n
                            Your account has been successfully created.
                    Thank you so much in advance for your time and expertise.
                Sources link: https://github.com/unique-mysticism?tab=repositories
                   Follow me on GitHub for more codes. (〃￣︶￣)人(￣︶￣〃)\n
                        your account info: {username},{password},{phone_num}\n\n\n
        Erfan Ramezani,
        Mysticism
    """

    # Create Email (sender, receiver,subject, body)
    mail = EmailMessage()
    mail["From"] = sender_email
    mail["To"] = email_receiver
    mail["Subject"] = subject
    mail.set_content(body.center(50))
    # Add SSL (layer of security)
    context = create_default_context()

    # Log in and send the Email
    with SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender_email, pemail)
        smtp.sendmail(sender_email, email_receiver, mail.as_string())


#=======================================USERNAME METHODS=======================================
# Validating an Username        
def username_validate(username:str) -> bool|str:
    # Define valid username Regular Expression
    pattern = r"^[a-z][a-z0-9-]{4,31}$"

    # Verify Username
    if re.match(pattern, username):
        return username
    return False


#=======================================PASSWORD METHODS=======================================
# Validating a Password and check if it is strong enough
def password_validate(password:str) -> str:
    # Define valid Password Regular Expressions
    pattern = r"^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])*.{6,32}$"
    enough_length = r"^[a-zA-Z0-9#?!@$%^&*-].{6,32}$"
    contain_number = r"^(?=.*?[A-Z])*(?=.*?[a-z])*(?=.*?[0-9])(?=.*?[#?!@$%^&*-])*"
    contain_small_letter = r"^(?=.*?[A-Z])*(?=.*?[a-z])(?=.*?[0-9])*(?=.*?[#?!@$%^&*-])*"
    contain_captal_letter = r"^(?=.*?[A-Z])(?=.*?[a-z])*(?=.*?[0-9])*(?=.*?[#?!@$%^&*-])*"

    # Verify Password
    if re.match(pattern, password):
        # If the Password is strong enough finish the method and return empty (False)
        return
    if not re.match(enough_length, password):
        yield "The password must be 6-32 characters."
    if not re.match(contain_number, password):
        yield "Use at least 1 number in your password."
    if not re.match(contain_small_letter, password):
        yield "Use at least 1 small Letter in your password."
    if not re.match(contain_captal_letter, password):
        yield "Use at least 1 Capital letter in your password."

#use later for get
# if not list(password_validate(password)):
#     print(password)
# else:
#     print(list(password_validate(password)))
#     print("password is incoocrect")
        

#=======================================PHONE NUMBER METHODS=======================================
# Validating a Phone Number
def phone_num_validate(phone_num:str) -> bool|str:
    # Define valid Phone Number Regular Expressions
    pattern = r"^09[0-9]{9}$"

    # Verify Phone Number
    if re.match(pattern, phone_num):
        send_verify_message(phone_num)
        return phone_num
    return False

# Send message (just for more fun!)
def send_verify_message(phone_num:str):
    pass


#=======================================NAME METHODS=======================================
# Validating a name
def name_validate(name:str) -> bool|str:
    # Define valid Name Regular Expressions
    pattern = r"^[a-zA-Z]*$"

    # Verify Name
    if re.match(pattern, name):
        return name
    return False