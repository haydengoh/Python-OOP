# this something we can re-use from lab3 q5

from myLib import getIntegerRange

def menuOption():
    print("Menu")
    print("1. Option A")
    print("2. Option B")
    print("3. Option C")
    print("0. Quit")
    option = getIntegerRange("Enter choice: ",0,3)
    return option

def actionA():
    print("I am doing action A")

def actionB():
    print("I am doing action B")

def actionC():
    print("I am doing action C")
    
def main():
    while True:
        option = menuOption()
        if option == 0:
            break
        elif option == 1:
            actionA()
        elif option == 2:
            actionB()
        else:
            actionC()

    print("bye")
    
main()
