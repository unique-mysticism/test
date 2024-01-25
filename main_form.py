#=======================================main_form.py=======================================
#=========================================LIBRARYS=========================================
# Tk GUI toolkit####################
from tkinter import *
import tkinter.messagebox as tkMessageBox

# Database##########################
import sqlite3

# Local Librarys###########jhgjkuy#########
from libs.verification import *
from libs.io import *
from libs.messages import *
dhtd

#=======================================METHODS=======================================
def database():
    global conn, cursor
    conn = sqlite3.connect("users_info.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `profile` (user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT, first_name TEXT, last_name TEXT, email_address TEXT, phone_num TEXT)")


def myexit():
    result = tkMessageBox.askquestion("System", "Are you sure you want to exit?", icon="warning")
    if result == "yes":
        form.destroy()
        exit()


# Conver input to str and remove spaces
def get_input(input):
    return str(input.get()).strip()


def signup():
    # Check if filds are empty (no problem if phone number is empty)
    if USERNAME.get == "" or PASSWORD.get() == "" or FIRST_NAME.get() == "" or LAST_NAME.get == "" or EMAIL_ADDRESS.get == "":
        lbl_result1.config(text=error_empty_input, fg="red")
    # Connect to Database and check if entered username is in Database
    else:
        database()
        cursor.execute("SELECT * FROM `profile` WHERE `username` = ?", (USERNAME.get(),))
        # If entered username was found, show error
        if cursor.fetchone() is not None:
            lbl_result1.config(text=error_duplicate_username, fg="black")
        # If entered username was not found, else:
        else:
            # Check inputs validate========================================================
            if username_validate(USERNAME.get(),):
                if not list(password_validate(PASSWORD.get(),)):
                    if (CONFIRM_PASSWORD.get(),) == (PASSWORD.get(),):
                        if name_validate(FIRST_NAME.get(),):
                            if name_validate(LAST_NAME.get(),):
                                if phone_num_validate(PHONE_NUMBER.get(),):
                                    if email_validate(EMAIL_ADDRESS.get(), FIRST_NAME.get(), USERNAME.get(), PASSWORD.get(), PHONE_NUMBER.get()):
                                        # Insert inputs in Database=======================================================================================================================================================================================================================================
                                        cursor.execute("INSERT INTO `profile` (username, password, first_name, last_name, email_address, phone_num) VALUES(?, ?, ?, ?, ?, ?)", (get_input(USERNAME), get_input(PASSWORD), get_input(FIRST_NAME), get_input(LAST_NAME), get_input(EMAIL_ADDRESS), get_input(PHONE_NUMBER)))
                                        conn.commit()
                                        USERNAME.set("")
                                        PASSWORD.set("")
                                        CONFIRM_PASSWORD.set("")
                                        FIRST_NAME.set("")
                                        LAST_NAME.set("")
                                        EMAIL_ADDRESS.set("")
                                        PHONE_NUMBER.set("")
                                        cursor.close()
                                        conn.close()
                                        lbl_result1.config(text=successful_account_created, fg="blue")
                                        #=================================================================================================================================================================================================================================================================
            # Show Errors==================================================================
                                    else:lbl_result1.config(text=error_email_address, fg="black")
                                else:lbl_result1.config(text = error_phone_num, fg="black")
                            else:lbl_result1.config(text = error_last_name, fg="black")
                        else:lbl_result1.config(text = error_first_name, fg="black")
                    else:lbl_result1.config(text = error_passwords_match, fg="black")
                else:lbl_result1.config(text = "\n".join(list(password_validate(PASSWORD.get(),))), fg="black")#shows password validate errors
            else:lbl_result1.config(text = error_username, fg="black")


def login():
    # Check if filds are empty
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result2.config(text=error_empty_input, fg="red")
    # Connect to Database and check If entered username and password found in Database
    else:
        database()
        # Selected hole row and put it in info
        cursor.execute("SELECT * FROM `profile` WHERE `username` = ? and `password` = ?", (get_input(USERNAME), get_input(PASSWORD)))
        info = cursor.fetchone()
        if info is not None:
            # Put res and info in a Dictonary and Show
            res = ("user_id", "username", "password", "first_name", "last_name", "email_address", "phone_num")
            info = dict(map(lambda i,j : (i,j) , res,info))
            lbl_result2.config(text=f'{successful_login}\n\n\nFirst Name: {info["first_name"]}\nLast Name: {info["last_name"]}\nEmail Address:\n{info["email_address"]}\nPhone Number:{info["phone_num"]}', fg="green")
        # If entered username and password was not found, show error
        else:
            lbl_result2.config(text=error_username_password_match, fg="red")


def reset_password():
    # Check if filds are empty
    if USERNAME.get == "" or PASSWORD.get() == "" or CONFIRM_PASSWORD.get() == "":
        lbl_result3.config(text=error_empty_input, fg="red")

    else:
        # Connect to Database
        database()
        # Check If username is valid
        if username_validate(USERNAME.get(),):
            # Check If entered username found in Database
            cursor.execute("SELECT * FROM `profile` WHERE `username` = ?", (USERNAME.get(),))
            if cursor.fetchone() is not None:
                # Check If password is valid
                if not list(password_validate(PASSWORD.get(),)):
                    # Check If PASSWORD is equal with CONFIRM_PASSWORD
                    if (CONFIRM_PASSWORD.get(),) == (PASSWORD.get(),):
                        # Check If password is used before
                        cursor.execute("SELECT * FROM `profile` WHERE `username` = ? and `password` = ?", (USERNAME.get(), PASSWORD.get()))
                        if cursor.fetchone() is not None:
                            lbl_result3.config(text = error_duplicate_password, fg="black")
                        # Update Password
                        else:
                            cursor.execute("Update `profile` set password = (?) WHERE username = (?)", (get_input(PASSWORD), get_input(USERNAME)))
                            conn.commit()
                            cursor.close()
                            conn.close() 
                            lbl_result3.config(text=successful_password_changed, fg="blue")
                    else:lbl_result3.config(text = error_passwords_match, fg="black")
                else:lbl_result3.config(text = "\n".join(list(password_validate(PASSWORD.get(),))), fg="black")#shows password validate errors
            else:lbl_result3.config(text=error_exist_username, fg="black")
        else:lbl_result3.config(text = error_username, fg="black")


#=========================================CHANGE PAGES=========================================
def ToggleToLogin(event=None):
    CurrentFrame.destroy()
    login_form()

def ToggleToSignup(event=None):
    CurrentFrame.destroy()
    signup_form()

def ToggleToResetPassword(event=None):
    CurrentFrame.destroy()
    reset_password_form()


#=========================================FORMS=========================================
def signup_form():
    global CurrentFrame, lbl_result1
    CurrentFrame = Frame(form, bg=TEXT_BG)
    CurrentFrame.pack(side=TOP, pady=20)

    lbls = ["Username:", "Password:", "Confirm Password:", "First name:", "Last name:", "Email Address:", "Phone Number:", "Already have account?"]
    entrys = [USERNAME, PASSWORD, CONFIRM_PASSWORD, FIRST_NAME, LAST_NAME, EMAIL_ADDRESS, PHONE_NUMBER]
    lbl_username            = Label(CurrentFrame, text=lbls[0], font=TEXT_FONT, bd=15, bg=TEXT_BG)
    lbl_password            = Label(CurrentFrame, text=lbls[1], font=TEXT_FONT, bd=15, bg=TEXT_BG)
    lbl_password_confirm    = Label(CurrentFrame, text=lbls[2], font=TEXT_FONT, bd=15, bg=TEXT_BG)
    lbl_firstname           = Label(CurrentFrame, text=lbls[3], font=TEXT_FONT, bd=15, bg=TEXT_BG)
    lbl_lastname            = Label(CurrentFrame, text=lbls[4], font=TEXT_FONT, bd=15, bg=TEXT_BG)
    lbl_email_address       = Label(CurrentFrame, text=lbls[5], font=TEXT_FONT, bd=15, bg=TEXT_BG)
    lbl_phone_num           = Label(CurrentFrame, text=lbls[6], font=TEXT_FONT, bd=15, bg=TEXT_BG)
    lbl_login               = Label(CurrentFrame, text=lbls[7], font="Helvetica 15 underline", bg=TEXT_BG)
    lbl_result1             = Label(CurrentFrame, text="", font=TEXT_FONT, bd=15, bg=TEXT_BG)
    entry_username          = Entry(CurrentFrame, textvariable=entrys[0], font=TEXT_FONT, width=20, bg=ENTRY_BG)
    entry_password          = Entry(CurrentFrame, textvariable=entrys[1], font=TEXT_FONT, width=20, show="*", bg=ENTRY_BG)
    entry_password_confirm  = Entry(CurrentFrame, textvariable=entrys[2], font=TEXT_FONT, width=20, show="*", bg=ENTRY_BG)
    entry_firstname         = Entry(CurrentFrame, textvariable=entrys[3], font=TEXT_FONT, width=20, bg=ENTRY_BG)
    entry_lastname          = Entry(CurrentFrame, textvariable=entrys[4], font=TEXT_FONT, width=20, bg=ENTRY_BG)
    entry_email_address     = Entry(CurrentFrame, textvariable=entrys[5], font=TEXT_FONT, width=30, bg=ENTRY_BG)
    entry_phone_num         = Entry(CurrentFrame, textvariable=entrys[6], font=TEXT_FONT, width=20, bg=ENTRY_BG)
    btn_sginup              = Button(CurrentFrame, text="Register", command=signup, font=TEXT_FONT, width=20, bg=ENTRY_BG, borderwidth=8)

    lbl_username.grid(row=1, sticky="E")
    lbl_password.grid(row=2, sticky="E")
    lbl_password_confirm.grid(row=3, sticky="E")
    lbl_firstname.grid(row=4, sticky="E")
    lbl_lastname.grid(row=5, sticky="E")
    lbl_email_address.grid(row=6, sticky="E")
    lbl_phone_num.grid(row=7, sticky="E")
    lbl_login.grid(row=8, columnspan=2)
    lbl_result1.grid(row=11, columnspan=2, pady=(10,0))
    entry_username.grid(row=1, column=1, sticky="W")
    entry_password.grid(row=2, column=1, sticky="W")
    entry_password_confirm.grid(row=3, column=1, sticky="W")
    entry_firstname.grid(row=4, column=1, sticky="W")
    entry_lastname.grid(row=5, column=1, sticky="W")
    entry_email_address.grid(row=6, column=1)
    entry_phone_num.grid(row=7, column=1, sticky="W")
    btn_sginup.grid(row=9, columnspan=2, pady=(10,0))

    lbl_login.bind("<Button-1>", ToggleToLogin)



def login_form():
    global CurrentFrame, lbl_result2, btn_login
    CurrentFrame = Frame(form, bg=TEXT_BG)
    CurrentFrame.pack(side=TOP, pady=20)

    lbls = ["Username:", "Password:", "Forget Password", "Don't have account?"]
    entrys = [USERNAME, PASSWORD]
    lbl_username        = Label(CurrentFrame, text=lbls[0], font=TEXT_FONT, bd=15, bg=TEXT_BG)
    lbl_password        = Label(CurrentFrame, text=lbls[1], font=TEXT_FONT, bd=15, bg=TEXT_BG)
    lbl_forget_password = Label(CurrentFrame, text=lbls[2], font="Helvetica 15 underline", bg=TEXT_BG)
    lbl_login           = Label(CurrentFrame, text=lbls[3], font="Helvetica 15 underline", bg=TEXT_BG)
    lbl_result2         = Label(CurrentFrame, text="", font=TEXT_FONT, bg=TEXT_BG)
    entry_username      = Entry(CurrentFrame, textvariable=entrys[0], font=TEXT_FONT, width=20, bg=ENTRY_BG)
    entry_password      = Entry(CurrentFrame, textvariable=entrys[1], font=TEXT_FONT, width=20, show="*", bg=ENTRY_BG)
    btn_login           = Button(CurrentFrame, text="Login", font=TEXT_FONT, command=login, width=20, bg=ENTRY_BG, borderwidth=8)

    lbl_username.grid(row=1)
    lbl_password.grid(row=2)
    lbl_forget_password.grid(row=3, columnspan=2)
    lbl_login.grid(row=4, columnspan=2)
    lbl_result2.grid(row=6, columnspan=2, pady=(10,0))
    entry_username.grid(row=1, column=1)
    entry_password.grid(row=2, column=1)
    btn_login.grid(row=5, columnspan=2, pady=(10,0))

    lbl_login.bind("<Button-1>", ToggleToSignup)
    lbl_forget_password.bind("<Button-1>", ToggleToResetPassword)



def reset_password_form():
    global CurrentFrame, lbl_result3
    CurrentFrame = Frame(form, bg=TEXT_BG)
    CurrentFrame.pack(side=TOP, pady=20)

    lbls = ["Username:", "Password:", "Confirm Password:"]
    entrys = [USERNAME, PASSWORD, CONFIRM_PASSWORD]
    lbl_username            = Label(CurrentFrame, text=lbls[0], font=TEXT_FONT, bd=15, bg=TEXT_BG)
    lbl_password            = Label(CurrentFrame, text=lbls[1], font=TEXT_FONT, bd=15, bg=TEXT_BG)
    lbl_password_confirm    = Label(CurrentFrame, text=lbls[2], font=TEXT_FONT, bd=15, bg=TEXT_BG)
    lbl_result3             = Label(CurrentFrame, text="", font=TEXT_FONT, bd=15, bg=TEXT_BG)
    entry_username          = Entry(CurrentFrame, textvariable=entrys[0], font=TEXT_FONT, bg=ENTRY_BG, width=20)
    entry_password          = Entry(CurrentFrame, textvariable=entrys[1], font=TEXT_FONT, bg=ENTRY_BG, width=20, show="*")
    entry_password_confirm  = Entry(CurrentFrame, textvariable=entrys[2], font=TEXT_FONT, bg=ENTRY_BG, width=20, show="*")
    btn_change_password     = Button(CurrentFrame, text="Change Password", font=TEXT_FONT, command=reset_password, width=20, bg=ENTRY_BG, borderwidth=8)
    btn_back                = Button(CurrentFrame, text="⬅️Back", command=ToggleToLogin, font=TEXT_FONT, bg=ENTRY_BG, borderwidth=8)

    lbl_username.grid(row=1)
    lbl_password.grid(row=2)
    lbl_password_confirm.grid(row=3)
    lbl_result3.grid(row=5, columnspan=2, pady=(10,0))
    entry_username.grid(row=1, column=1)
    entry_password.grid(row=2, column=1)
    entry_password_confirm.grid(row=3, column=1)
    btn_back.grid(row=4, sticky="W", pady=(10,0), padx=(50,0))
    btn_change_password.grid(row=4, columnspan=2, pady=(10,0), padx=(110,0))



#=========================================MAIN=========================================
def main():
     #===============================Create MAIN FORM===================================
    global form
    form = Tk()
    form.title("(⌐■_■)ノ  Mysticism ")
    # Form size
    width = 600
    height = 650
    # The form appears in the middle of the screen
    screen_width = form.winfo_screenwidth()
    screen_height = form.winfo_screenheight()
    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/1.8))
    form.geometry(f"{width}x{height}+{x}+{y}")
    # Lock resizing
    form.resizable(0, 0)


    #===========================Define INPUT VARIABLES=================================
    global USERNAME, PASSWORD, CONFIRM_PASSWORD, FIRST_NAME, LAST_NAME, EMAIL_ADDRESS, PHONE_NUMBER, TEXT_FONT, TEXT_BG, ENTRY_BG, bad_input
    USERNAME = StringVar()
    PASSWORD = StringVar()
    CONFIRM_PASSWORD = StringVar()
    FIRST_NAME = StringVar()
    LAST_NAME = StringVar()
    EMAIL_ADDRESS = StringVar()
    PHONE_NUMBER = StringVar()
    TEXT_FONT = ("arial", 15)
    TEXT_BG = "#92C7CF"
    ENTRY_BG = "#E5E1DA"
    bad_input = 0
    # Default form page
    signup_form()


    #===============================Create MENUBAR===================================
    mainbar = Menu(form,)
    account = Menu(mainbar, tearoff=0, font=TEXT_FONT)
    mainbar.add_cascade(label="Account 👤", menu=account)
    mainbar.add_command(label="Exit", command=myexit)
    account.add_command(label="Sign Up", command=ToggleToSignup)
    account.add_command(label="Log In", command=ToggleToLogin)
    form.config(menu=mainbar, bg=TEXT_BG)



#========================================INITIALIZATION===================================
if __name__ == "__main__":
    main()
    form.mainloop()