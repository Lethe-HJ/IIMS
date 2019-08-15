import os


def shell_start():
    workon = os.system("workon xd-iims")
    print(workon)
    flask = os.system('python runserver.py')
    print(flask)
