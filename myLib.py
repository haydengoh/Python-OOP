def getIntegerRange(prompt, min, max):
    while True:
        value = int(input(prompt))

        if min <= value <= max:
            return value

        print("Sorry, please re-enter within range ({}-{})".format(min, max))


def getFloatRange(prompt, min, max):
    while True:
        value = float(input(prompt))

        if min <= value <= max:
            return value

        print("Sorry, please re-enter within range ({}-{})".format(min, max))


def getCharSet(prompt, charSet):
    while True:
        value = input(prompt)

        if value[0] in charSet:
            return value[0]

        print("Sorry, please re-enter within ({})".format(charSet))


def getClub(prompt, stringSet):
    while True:
        value = input(prompt).title()

        if value in stringSet:
            return value

        print("Sorry, please re-enter from ({})".format(stringSet))


def getPositiveInteger(prompt):
    while True:
        value = int(input(prompt))

        if value > 0:
            return value

        print("Sorry, please enter positive integer only")


def getPositiveFloat(prompt):
    while True:
        value = float(input(prompt))

        if value > 0:
            return value

        print("Sorry, please enter positive float number only")
