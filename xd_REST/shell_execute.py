import os


def shell_start():
    workon = os.system("workon xd-iims")
    print(workon)
    ngrok = os.system('python ngrok//sunny.py')
    print(ngrok)