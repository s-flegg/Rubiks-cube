import sys
import tkinter as tk
from tkinter import ttk

from . import user_management

user_db = user_management.UserList()


class Window:
    """Creates and manages the login/signup window"""

    def __init__(self, load_game_function, name="Login"):
        """
        :type load_game_function: any
        :param load_game_function: function to load game, no brackets, takes user as param
        :type name: str
        :param name: title of window
        :rtype: object
        """
        self.load_game_function = load_game_function

        self.root = tk.Tk()
        self.root.title(name)

        # prevent resizing
        self.root.resizable = (False, False)

        # for deleting everything
        self.main_frame = ttk.Frame(self.root)

        # window dimensions
        self.window_width = 400
        self.window_height = 450

        # screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # centre points, left and top pos to centre window
        self.centre_x = int(self.screen_width / 2 - self.window_height / 2)
        self.centre_y = int(self.screen_height / 2 - self.window_height / 2)

        # position
        # widthxheight+x_pos+y_pos
        self.root.geometry(
            f"{self.window_width}x{self.window_height}+"
            f"{self.centre_x}+{self.centre_y}"
        )

        self.window_state = "login"
        self.message = None
        self.run()

    def set_state(self, state):
        """For changing the state in tkinter's commands, using lambda"""
        if state == "login":
            self.window_state = "login"
        elif state == "sign up":
            self.window_state = "sign up"
        elif state == "forgot password":
            self.window_state = "forgot password"
        else:
            self.window_state = "quit"
        self.message = None
        self.reset()
        self.run()

    def run(self):
        if self.window_state == "login":
            self.login_window()
        elif self.window_state == "sign up":
            self.sign_up_window()
        elif self.window_state == "forgot password":
            self.forgot_password_window()
        else:
            self.root.destroy()
            sys.exit()

    def reset(self):
        self.main_frame.destroy()
        self.main_frame = ttk.Frame(self.root)

    def frame(
        self,
        text,
        target,
        padding=(0, 10, 0, 10),
        colour="black",
        variable=None,
        show=True,
    ):
        """
        Creates a simple label frame and returns it
        :type text: str
        :type padding: tuple
        :param padding: padding to add in format (leftx,topy,rightx,bottomy)
        :type target: any
        :param target: screen/frame to display on
        :type colour: str
        :param colour: foreground colour, colour of text
        :type variable: any or None
        :param variable: the variable to change, or None
        :type show: bool
        :param show: show text entered into entry box
        """
        frame = ttk.Frame(target)
        frame["padding"] = padding
        label = ttk.Label(frame, text=text, foreground=colour)
        label.grid(column=0, row=0)
        if variable is not None:
            if show:
                entry = ttk.Entry(frame, textvariable=variable)
            else:
                entry = ttk.Entry(frame, textvariable=variable, show="**")
            entry.grid(column=1, row=0)
        return frame

    def login_window(self):
        """
        Displays login window
        """

        def login(username, password):
            """
            Attempts to log in, or re-displays login window with related message
            :type username: object
            :param username: username of user as tk.StringVar
            :type password: object
            :param password: password of user as tk.StringVar
            """
            u = username.get()
            p = password.get()
            if user_db.check_password(u, p):
                self.root.destroy()
                self.load_game_function(u)
                self.window_state = "quit"
            else:
                self.message = "Incorrect username or password"
                self.reset()
                self.run()

        username = tk.StringVar()
        password = tk.StringVar()

        if self.message is not None:
            message_frame = self.frame(
                self.message,
                self.main_frame,
                padding=(0, 10, 0, 10),
                colour="red",
            )
            message_frame.pack()

        username_frame = self.frame(
            "Username  ",  # spaces for spacing
            self.main_frame,
            padding=(0, 10, 0, 10),
            variable=username,
        )

        password_frame = self.frame(
            "Password  ",  # spaces for spacing
            self.main_frame,
            padding=(
                3,
                10,
                0,
                10,
            ),  # 3 padding to align entry box with username entry box
            variable=password,
            show=False,
        )

        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame["padding"] = (0, 10, 0, 10)
        login_button = ttk.Button(
            buttons_frame,
            text="Login",
            command=lambda: login(username, password),
            width=16,
        )
        sign_up_button = ttk.Button(
            buttons_frame,
            text="Sign Up",
            command=lambda: self.set_state("sign up"),
            width=16,
        )
        forgot_password_button = ttk.Button(
            buttons_frame,
            text="Forgot Password?",
            command=lambda: self.set_state("forgot password"),
            width=16,
        )

        login_button.grid(row=0, column=0)
        sign_up_button.grid(row=0, column=1)
        forgot_password_button.grid(row=1, column=0)

        username_frame.pack()
        password_frame.pack()
        buttons_frame.pack()

        self.main_frame.pack()
        self.root.mainloop()

    def sign_up_window(self):
        """
        Displays sign up window
        """

        def sign_up(username, password1, password2, question, answer1, answer2):
            """
            Attempts to create new user, or re-displays with relevant message
            :type username: object
            :param username: tk.StringVar
            :type password1: object
            :param password1: tk.StringVar
            :type password2: object
            :param password2: for checking against password 1, tk.StringVar
            :type question: object
            :param question: security question, tk.StringVar
            :type answer1: object
            :param answer1: tk.StringVar
            :type answer2: object
            :param answer2: for checking against answer 1, tk.StringVar
            """
            u = username.get()
            p1 = password1.get()
            p2 = password2.get()
            q = question.get()
            a1 = answer1.get()
            a2 = answer2.get()
            if len(u) < 1:
                self.message = "No username given."
            elif p1 != p2:
                self.message = "Paswords do not match."
            elif a1 != a2:
                self.message = "Answers do not match."
            elif len(p1) < 1:
                self.message = "No password given."
            elif len(q) < 1:
                self.message = "No security question given."
            elif len(a1) < 1:
                self.message = "No answer given."
            elif not user_db.add_user(u, p1, q, a1):
                self.message = "That username is taken."
            else:
                self.load_game_function(u)
                self.window_state = "quit"

            self.reset()
            self.run()

        username = tk.StringVar()
        password1 = tk.StringVar()
        password2 = tk.StringVar()
        question = tk.StringVar()
        answer1 = tk.StringVar()
        answer2 = tk.StringVar()

        if self.message is not None:
            message_frame = self.frame(
                self.message, self.main_frame, padding=(0, 10, 0, 10), colour="red"
            )
            # message_frame.grid(row=0, column=2)
            message_frame.pack()

        username_frame = self.frame(
            "Username  ",
            self.main_frame,
            padding=(0, 10, 0, 10),
            variable=username,
        )
        password1_frame = self.frame(
            "Password  ",
            self.main_frame,
            padding=(0, 10, 0, 5),
            variable=password1,
            show=False,
        )
        password2_frame = self.frame(
            "Re-enter password  ",
            self.main_frame,
            padding=(0, 0, 0, 10),
            variable=password2,
            show=False,
        )
        question_frame = self.frame(
            "Security Question  ",
            self.main_frame,
            padding=(0, 10, 0, 10),
            variable=question,
        )
        answer1_frame = self.frame(
            "Answer  ",
            self.main_frame,
            padding=(0, 10, 0, 5),
            variable=answer1,
            show=False,
        )
        answer2_frame = self.frame(
            "Re-enter answer  ",
            self.main_frame,
            padding=(0, 0, 0, 10),
            variable=answer2,
            show=False,
        )

        username_frame.pack(ipadx=7)
        password1_frame.pack(ipadx=6)
        password2_frame.pack(ipadx=30)  # align entry boxes
        question_frame.pack(ipadx=27)
        answer1_frame.pack()
        answer2_frame.pack(ipadx=23)

        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame["padding"] = (0, 10, 0, 10)
        sign_up_button = ttk.Button(
            buttons_frame,
            text="Sign Up",
            command=lambda: sign_up(
                username, password1, password2, question, answer1, answer2
            ),
            width=16,
        )
        sign_up_button.pack()

        buttons_frame.pack()
        self.main_frame.pack()

    def forgot_password_window(self):
        """
        Displays forgot password windows
        """

        def get_username():
            """
            Displays window and handles getting username
            """

            def find_question(username):
                """
                Checks user exist, displays correct message if not
                :type username: object
                :param username: tk.StringVar
                """
                u = username.get()
                q = user_db.get_question(u)
                self.reset()
                if q is not False:
                    self.message = None
                    get_answer(username, q)
                else:
                    self.message = "That user does not exist."
                    self.run()

            if self.message is not None:
                message_frame = self.frame(
                    self.message, self.main_frame, padding=(0, 10, 0, 10), colour="red"
                )
                message_frame.pack()

            username = tk.StringVar()

            username_frame = self.frame(
                "Username  ", self.main_frame, padding=(0, 10, 0, 10), variable=username
            )

            username_frame.pack()

            buttons_frame = ttk.Frame(self.main_frame)
            confirm_button = ttk.Button(
                buttons_frame,
                text="Confirm",
                command=lambda: find_question(username),
                width=16,
            )
            confirm_button.pack()

            buttons_frame.pack()

        def get_answer(username, question):
            """
            Displays window and handles getting and checking answer
            :type username: object
            :param username: tk.StringVar
            :type question: str
            """

            def check_answer(username, answer):
                """
                Checks answer is correct and displays message if not
                :type username: object
                :param username: tk.StringVar
                :type answer: object
                :param answer: tk.StringVar
                """
                u = username.get()
                a = answer.get()
                self.reset()
                if user_db.check_answer(u, a):
                    self.message = None
                    change_password(username)
                else:
                    self.message = "Incorrect"
                    get_answer(username, question)

            if self.message is not None:
                message_frame = self.frame(
                    self.message, self.main_frame, padding=(0, 10, 0, 10), colour="red"
                )
                message_frame.pack()

            answer = tk.StringVar()

            question_frame = self.frame(
                question, self.main_frame, padding=(0, 10, 0, 10)
            )

            answer_frame = self.frame(
                "Answer  ", self.main_frame, padding=(0, 10, 0, 10), variable=answer
            )

            question_frame.pack()
            answer_frame.pack()

            buttons_frame = ttk.Frame(self.main_frame)
            confirm_button = ttk.Button(
                buttons_frame,
                text="Enter",
                command=lambda: check_answer(username, answer),
                width=16,
            )
            confirm_button.pack()

            buttons_frame.pack()
            self.main_frame.pack()

        def change_password(username):
            """
            Displays window nad handles changing password
            :type username: object
            :param username: tk.StringVar
            """

            def set_password(username, password1, password2):
                """
                Handles changing password, and ensuring it is valid
                :type username: object
                :param username: tk.StringVar
                :type password1: object
                :param password1: tk.StringVar
                :type password2: object
                :param password2: for comparing against password 1, tk.StringVar
                """
                u = username.get()
                p1 = password1.get()
                p2 = password2.get()
                self.reset()
                if len(p1) < 1:
                    self.message = "No password given."
                elif p1 != p2:
                    self.message = "Passwords do not match."
                else:
                    user_db.change_password(u, p1)
                    self.message = None
                    self.window_state = "login"
                    self.run()
                    return  # prevents change password from re-running
                change_password(username)

            if self.message is not None:
                message_frame = self.frame(
                    self.message,
                    self.main_frame,
                    padding=(0, 10, 0, 10),
                    colour="red",
                )
                message_frame.pack()

            password1 = tk.StringVar()
            password2 = tk.StringVar()

            password1_frame = self.frame(
                "Password  ",
                self.main_frame,
                padding=(0, 10, 0, 5),
                variable=password1,
            )
            password2_frame = self.frame(
                "Re-enter password",
                self.main_frame,
                padding=(0, 0, 0, 10),
                variable=password2,
            )

            password1_frame.pack()
            password2_frame.pack(ipadx=21)

            buttons_frame = tk.Frame(self.main_frame)
            confirm_button = ttk.Button(
                buttons_frame,
                text="Confirm",
                command=lambda: set_password(username, password1, password2),
                width=16,
            )
            confirm_button.pack()
            buttons_frame.pack()
            self.main_frame.pack()

        get_username()
        self.main_frame.pack()


# testing
if __name__ == "__main__":

    def test(n):
        print(n)

    window = Window(lambda n: test(n))
