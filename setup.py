import os
import sys

cwd = os.getcwd()
sys.path.append(cwd + "\Login")

from Login import login_window
from user_data import db

def load_data(username):
    data = db.load(username)
    print(data)

def run():
    window = login_window.Window(load_data, "Rubik's Cube")
