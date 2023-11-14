from Controller import *

if __name__ == '__main__':
    controller = Controller()
    if controller.start():
        while True:
            controller.main_stream()