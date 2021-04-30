import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import socket
import time

str = "self.userNames = []\nself.passwords=[]".encode()
__key = b'UlDmSjZX_V9lrnh6xNsxduK-_u6oa69JKuYYWHFwHEQ='


# ServerSocket = f.encrypt(str)
# f.encrypt(b"asdasd")
# g = f.decrypt(ServerSocket)
# print(ServerSocket)
# print(g)
# with open("Users", "wb") as user:
#     f = Fernet(__key)
#     user.write(f.encrypt(str))


# data = user.read()
# print(data)
# print(f.decrypt(data))

class loginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.width = 623
        self.height = 550
        self.font = font.Font(self.root, size=30)
        img = Image.open("BG.jpg")
        self.background = ImageTk.PhotoImage(image=img)
        self.onScreenText = None
        self.screen = "main"
        self.__create_Socket()
        self.__connect(True)
        # TODO place this is in a better place
        # WILL BE REMOVED LATER TO BE PUT IN A MORE SUITABLE PLACE
        # self.__key = b'UlDmSjZX_V9lrnh6xNsxduK-_u6oa69JKuYYWHFwHEQ='
        # self.__fernet = Fernet(self.__key)
        # with open("Users", "rb") as user:
        #     data = user.read()
        #     g = self.__fernet.decrypt(data)
        #     exec(g)
        # self.users = dict(zip(self.userNames, self.passwords))  # NOQA

    def __create_Socket(self):
        self.server = ("192.168.137.1", 56969)
        self.__hostName = socket.gethostname()
        self.__ipAddress = socket.gethostbyname(self.__hostName)
        self.addr = (self.__ipAddress, 0)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.addr)

    def __create_canvas(self):
        self.onScreenText = None
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.background)

    def __login_button_press_handler(self, userNameWidget, passwordWidget):
        if self.onScreenText is not None:
            self.canvas.delete(self.onScreenText)
        userName = userNameWidget.get()
        password = passwordWidget.get()
        try:
            self.socket.send(f'L09{userName}:{password}'.encode())
            time.sleep(0.075)
            response = self.socket.recv(1024).decode()
            self.onScreenText = self.canvas.create_text(312, 50, text=f"{response}", font=self.font)
            passwordWidget.delete(0, "end")
        except socket.error:
            self.screen = "error"
            self.__error()
        # if self.__users.get(userNameWidget.get()) == passwordWidget.get():
        #     self.canvas.quit()
        # else:
        #     self.onScreenText = self.canvas.create_text(312, 50, text="Wrong user name or password", font=self.font)
        #     passwordWidget.delete(0, "end")

    def __signup_button_press_handler(self, userNameWidget, password1Widget, password2Widget):
        if self.onScreenText is not None:
            self.canvas.delete(self.onScreenText)
        p1 = password1Widget.get()
        p2 = password2Widget.get()
        userName = userNameWidget.get()
        if p1 != "" and p1 == p2:
            try:
                self.socket.send(f'S19{userName}:{p1}'.encode())
                time.sleep(0.075)
                response = self.socket.recv(1024).decode()
                self.onScreenText = self.canvas.create_text(312, 50, text=f"{response}", font=self.font)
            except socket.error:
                self.__error()
        elif p1 == "":
            self.onScreenText = self.canvas.create_text(312, 50, text="Please enter a password", font=self.font)
        else:
            self.onScreenText = self.canvas.create_text(312, 50, text="Passwords do not match", font=self.font)

        # if userName != "":
        #     if self.users.get(userName) is None:
        #         if p1 == p2 and p1 != "":
        #             self.users[userName] = p1
        #             st = f"self.userNames = {list(self.users.keys()).__str__()} " \
        #                  f"\nself.passwords = {list(self.users.values()).__str__()}".encode()
        #             with open("Users", "wb") as user:
        #                 user.write(self.__fernet.encrypt(st))
        #             self.onScreenText = self.canvas.create_text(312, 50, text="Successfully signed", font=self.font)
        #         elif p1 == "":
        #             self.onScreenText = self.canvas.create_text(312, 50, text="Please enter a password", font=self.font)
        #         else:
        #             self.onScreenText = self.canvas.create_text(312, 50, text="Passwords do not match", font=self.font)
        #     else:
        #         self.onScreenText = self.canvas.create_text(312, 50, text="User name already exists",
        #                                                     font=self.font)
        # else:
        #     self.onScreenText = self.canvas.create_text(312, 50, text="User name cannot be black", font=self.font)

    def __error(self):
        self.__create_Socket()
        self.screen = "error"
        self.canvas.destroy()
        self.__create_widgets()

    def __back_button_press_handler(self):
        self.screen = "main"
        self.canvas.destroy()
        self.__create_widgets()

    def __login_window_button_press_handler(self):
        self.screen = "login"
        self.canvas.destroy()
        self.__create_widgets()

    def __signup_window_button_press_handler(self):
        self.screen = "signup"
        self.canvas.destroy()
        self.__create_widgets()

    def __create_widgets_main(self):
        self.loginWindowButton = tk.Button(self.canvas, text="Login", bg="#c54985", font=self.font,
                                           command=lambda: self.__login_window_button_press_handler())
        self.canvas.create_window(300, 180, window=self.loginWindowButton)
        self.signupWindowButton = tk.Button(self.canvas, text="Signup", bg="#c54985", font=self.font,
                                            command=lambda: self.__signup_window_button_press_handler())
        self.canvas.create_window(300, 380, window=self.signupWindowButton)

    def __connect(self, firstTime=False):
        try:
            self.socket.connect(self.server)
            if not firstTime:
                self.__back_button_press_handler()
        except socket.error:
            self.screen = "error"

    def __create_widgets_error(self):
        self.canvas.create_text(312, 50, text="Error please check your connection", font=self.font)
        self.canvas.create_text(312, 100, text="with server and try again", font=self.font)
        self.canvas.create_text(312, 150, text="If the problem keeps happening", font=self.font)
        self.canvas.create_text(312, 200, text=" please contact admins", font=self.font)
        self.tryAgainButton = tk.Button(self.canvas, text="Try again", font=self.font, bg="#c54985",
                                        command=self.__connect)
        self.canvas.create_window(300, 480, window=self.tryAgainButton)

    def __create_widgets(self):
        self.__create_canvas()
        if self.screen == "main":
            self.__create_widgets_main()
        elif self.screen == "login":
            self.__create_widgets_login()
        elif self.screen == "signup":
            self.__create_widgets_signup()
        else:
            self.__create_widgets_error()

    def __create_widgets_signup(self):
        self.canvas.create_text(312, 90, text="User Name:", fill="black", font=self.font)
        userNameWidget = tk.Entry(self.canvas, font=self.font)
        self.canvas.create_text(312, 200, text="Password:", fill="black", font=self.font)
        password1Widget = tk.Entry(self.canvas, font=self.font, show="*")
        self.canvas.create_text(312, 300, text="Retype Password:", fill="black", font=self.font)
        password2Widget = tk.Entry(self.canvas, font=self.font, show="*")
        self.signupButton = tk.Button(self.canvas, text="Signup", font=self.font, bg="#c54985",
                                      command=lambda: self.__signup_button_press_handler(userNameWidget,
                                                                                         password1Widget,
                                                                                         password2Widget))
        self.backButton = tk.Button(self.canvas, text="back", bg="#c54985",
                                    command=lambda: self.__back_button_press_handler())
        self.canvas.create_window(0, 0, anchor="nw", window=self.backButton)
        self.canvas.create_window(300, 480, window=self.signupButton)
        self.canvas.create_window(312, 150, window=userNameWidget)
        self.canvas.create_window(312, 250, window=password1Widget)
        self.canvas.create_window(312, 350, window=password2Widget)

    def __create_widgets_login(self):
        self.canvas.create_text(312, 190, text="User Name:", fill="black", font=self.font)
        userNameWidget = tk.Entry(self.canvas, font=self.font)
        self.canvas.create_text(312, 300, text="Password:", fill="black", font=self.font)
        passwordWidget = tk.Entry(self.canvas, font=self.font, show="*")
        self.loginButton = tk.Button(self.canvas, text="Login", font=self.font, bg="#c54985",
                                     command=lambda: self.__login_button_press_handler(userNameWidget, passwordWidget))
        self.backButton = tk.Button(self.canvas, text="back", bg="#c54985",
                                    command=lambda: self.__back_button_press_handler())
        self.canvas.create_window(0, 0, anchor="nw", window=self.backButton)
        self.canvas.create_window(300, 480, window=self.loginButton)
        self.canvas.create_window(312, 250, window=userNameWidget)
        self.canvas.create_window(312, 350, window=passwordWidget)

    def main(self):
        self.__create_widgets()
        self.canvas.mainloop()


lw = loginWindow()
lw.main()
