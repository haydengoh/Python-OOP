import os
from abc import ABC, abstractmethod

from myLib import getIntegerRange, getCharSet


class EquipmentRuleException(Exception):
    """
    When the application encounters an equipment rule violation,
an exception from this class is raised.
    """
    pass


class ClubHead(ABC):

    def __init__(self, loft, weight):
        self._loft = loft
        self._weight = weight

    @property  # accessor / getter method
    def loft(self):
        return self._loft

    @property  # accessor / getter method
    def weight(self):
        return self._weight

    @abstractmethod
    def getHeight(self):
        pass

    def __str__(self):
        """
        returns a string representation of a ClubHead object, in the
following order: loft, weight
        """
        return "{},{}".format(self.loft, self.weight)


class WoodHead(ClubHead):

    def __init__(self, loft, weight, size):
        super().__init__(loft, weight)
        self._size = size

    def getHeight(self):
        """
        The height is calculated by dividing the size by 400.
        """
        return int(self._size) / 400

    def __str__(self):
        """
        returns a string representation of a WoodHead object, in the
following order: “Wood”, loft, weight, size
        """
        return "Wood,{},{}".format(super().__str__(), self._size)


class IronHead(ClubHead):
    def __init__(self, loft, weight, material):
        super().__init__(loft, weight)
        self._material = material

    def getHeight(self):
        return 1

    def __str__(self):
        """
        returns a string representation of a IronHead object, in the
following order: “Iron”, loft, weight, material
        """
        return "Iron,{},{}".format(super().__str__(), self._material)


class PutterHead(ClubHead):

    def __init__(self, loft, weight, style):
        super().__init__(loft, weight)
        if style == "Blade" or style == "Mallet" or style == "Half-Mallet":
            self._style = style

    def getHeight(self):
        """
        returns 1 inch if the putter is a “Blade”.
Otherwise, the method returns 0.5 inch.
        """
        if self._style == "Blade":
            return 1
        return 0.5

    def __str__(self):
        return "Putter,{},{}".format(super().__str__(), self._style)


class Shaft:
    def __init__(self, length, weight, material, flex):
        self._length = length
        self._weight = weight
        self._material = material
        """
        flex term: SR for Senior, R for Regular, S for Stiff, XS for Extra-Stiff.
        """
        if flex == 'SR' or flex == 'R' or flex == 'S' or flex == 'XS':
            self._flex = flex

    @property  # accessor / getter method
    def length(self):
        return self._length

    @property  # accessor / getter method
    def weight(self):
        return self._weight

    @property  # accessor / getter method
    def flex(self):
        return self._flex

    def __str__(self):
        """
        returns a string representation of a Shaft object, in the
following order: length, weight, material, flex
        """
        return "{},{},{},{}".format(self.length, self.weight, self._material, self.flex)


class Grip:
    def __init__(self, diameter, weight, material):
        if float(diameter) == 0.6 or float(diameter) == 0.58:
            self._diameter = diameter
        self._weight = weight
        if material == 'Rubber' or material == 'Leather' or material == 'Synthetic':
            self._material = material

    @property  # accessor / getter method
    def weight(self):
        return self._weight

    @property  # accessor / getter method
    def diameter(self):
        return self._diameter

    def __str__(self):
        """
        returns a string representation of a Grip object, in the following
order: diameter, weight, material
        """
        return "{},{},{}".format(self.diameter, self.weight, self._material)


class Club:

    def __init__(self, label, head: ClubHead, shaft: Shaft, grip: Grip):
        # labelling or numbering in uppercase, to help golfers identify the club.
        # For example, “7-IRON”, “3-WOOD” and “4-HYBRID”.
        self._label = label
        self._head = head
        self._shaft = shaft
        self._grip = grip
        """
        1. Weight of head must be more than the combined weight of the shaft and grip.
        2. Assembled club length must be within 18 to 48 inches.
        Otherwise, raise EquipmentRuleException with appropriate message
        """
        if int(head.weight) < (int(shaft.weight) + int(grip.weight)):
            raise EquipmentRuleException(
                'Club Weight must be more than shaft & grip weight!')
        if 18 > (float(shaft.length) + float(head.getHeight())) > 48:
            raise EquipmentRuleException(
                'Assembled club length must be within 18 to 48 inches')

    @property  # accessor / getter method
    def loft(self):
        """
        Loft of the club refers to the loft of the clubhead.
        """
        return self._head.loft

    @property  # accessor / getter method
    def flex(self):
        """
        Flex of the club refers to the shaft’s flex.
        """
        return self._shaft.flex

    @property  # accessor / getter method
    def length(self):
        """
        Length of the club is the length of the shaft and the height of the clubhead.
        """
        return float(self._shaft.length) + float(self._head.getHeight())

    @property  # accessor / getter method
    def weight(self):
        """
        Weight of the club is the total weight of clubhead, shaft and grip.
        """
        return int(self._head.weight) + int(self._shaft.weight) + int(self._grip.weight)

    def changeGrip(self, newGrip: Grip):
        """
        The changeGrip method replaces the instance variable _grip
with the given parameter Grip object, provided that the weight of head must be
more than the combined weight of the shaft and this new grip. Otherwise, raise
EquipmentRuleException with appropriate message.
        """
        if self._head.weight > (self._shaft.weight + newGrip.weight):
            self._grip = newGrip
        else:
            raise EquipmentRuleException(
                'Weight of head must be more than the combined weight of the shaft and this new grip!')

    def getDetails(self):
        """
        getDetails method returns a string presentation of the club’s label, loft, length, flex, and weight
        """
        return "Club: {:10} Loft: {:4} Length: {:6,.2f}in Flex: {:1} Weight: {:3}g".format(self._label, self.loft,
                                                                                        self.length, self.flex,
                                                                                        self.weight)

    def __str__(self):
        """
        returns the label of the club, follow by the string representations of clubhead, shaft and grip.
        """
        return "{},{},{},{}".format(self._label, self._head, self._shaft, self._grip)


class GolfSet:
    _CLUBTYPE = ['Wood', 'Iron', 'Putter']

    def __init__(self, ownerID, owner, newSet):
        self._ownerID = ownerID
        self._owner = owner
        self._clubs = {"Wood": [], "Iron": [], "Putter": []}

        if newSet is True:
            return
        else:
            fileName = f'C:/Users/HAYDEN.GOH/IdeaProjects/HelloPython/TMA/{self._ownerID}-{self._owner}.txt'
            if not os.path.isfile(fileName):
                raise EquipmentRuleException('File is not file!')

            infile = open(fileName, 'r')
            for oneLine in infile:
                newList = []
                newList.append(oneLine.rstrip('\n').split(','))
                """
                DRIVER,Wood,10.5,203,450,44.25,68,Graphite,R,0.6,62,Rubber
                5-WOOD,[Wood,17.5,240,280],[41.5,85,Graphite,R],[0.6,62,Rubber]
                5-IRON,[Iron,26.5,262,Cast],[38.0,102,Steel,S],[0.6,62,Rubber]
                ODYSSEY#7,[Putter,3.0,365,Mallet],[34.0,120,Steel,S],[0.6,62,Rubber]
                
                # TEST
                print(newList[0][2], newList[0][3], newList[0][4])
                print(newList[0][5], newList[0][6], newList[0][7], newList[0][8])
                print(newList[0][9], newList[0][10], newList[0][11])
                """
                label = newList[0][0]
                category = newList[0][1]
                if category == 'Wood':
                    # WoodHead(loft, weight, size)
                    head = WoodHead(newList[0][2], newList[0][3], newList[0][4])
                elif category == 'Iron':
                    # IronHead(loft, weight, material)
                    head = IronHead(newList[0][2], newList[0][3], newList[0][4])
                else:
                    # PutterHead(loft, weight, style)
                    head = PutterHead(newList[0][2], newList[0][3], newList[0][4])

                # Shaft(length, weight, material, flex)
                shaft = Shaft(newList[0][5], newList[0][6], newList[0][7], newList[0][8])
                # Grip(diameter, weight, material)
                grip = Grip(newList[0][9], newList[0][10], newList[0][11])
                # Club(label, head: ClubHead, shaft: Shaft, grip: Grip)
                club = Club(label, head, shaft, grip)

                # print(club.getDetails())

                # if category in self._clubs:
                #     self._clubs[category].append(club)

                # populate Club objects into _clubs
                self._clubs[category] += [club]

            infile.close()
            # print(self._clubs)

    @classmethod
    def getClubType(cls):
        """
        class method getClubType that returns the 3 categories in a List.
        """
        return cls._CLUBTYPE

    @property
    def owner(self):
        return self._owner

    @property
    def numberOfClubs(self):
        """
        sum of all clubs in the 3 categories of golf clubs.
        """
        counter = 0
        for oneValue in self._clubs.values():
            for i in oneValue:
                counter += 1
        return counter

    def add(self, clubType, newClub: Club):
        # The maximum number of clubs in a golf set is 14.
        if self.numberOfClubs >= 14:
            raise EquipmentRuleException('Maximum number of clubs in a golf set is 14!')

        # Each club label should be unique, within the golf set.
        newLabel = newClub._label
        for oneClub in self._clubs[clubType]:
            currentLabel = oneClub._label
            if newLabel == currentLabel:
                raise EquipmentRuleException('Label should be unique!')

        # The new Club’s shaft flex must match those in the same clubType category.
        newFlex = newClub.flex
        for oneClub in self._clubs[clubType]:
            currentFlex = oneClub.flex
            if newFlex is not currentFlex:
                raise EquipmentRuleException('New flex must match those in the same clubType category!')

        # Within the same clubType category, there should not be clubs having the same loft.
        newLoft = newClub.loft
        for oneClub in self._clubs[clubType]:
            currentLoft = oneClub.loft
            if newLoft == currentLoft:
                raise EquipmentRuleException('Should not have same loft within same clubType category!')

        """
        Within the same clubType category,
        the newClub must not be longer than the next club with lower loft.
        E.g., 8-Iron (37.0 degree) must not be longer than 7-Iron (33.5 degree).
        &&
        the newClub must not be shorter than the next club with higher loft.
        E.g., 8-Iron (37.0 degree) must not be shorter than 9-Iron (40.5 degree).
        """
        for oneClub in self._clubs[clubType]:
            currentLabel = oneClub._label
            # NEXT club
            if newLabel[0] > currentLabel[0]:
                # the newClub must not be longer than the next club with lower loft.
                if float(newClub.loft) < float(oneClub.loft):
                    if newClub.length > oneClub.length:
                        raise EquipmentRuleException('New Club must not be longer than the next club with lower loft')
                # the newClub must not be shorter than the next club with higher loft.
                elif float(newClub.loft) > float(oneClub.loft):
                    if newClub.length < oneClub.length:
                        raise EquipmentRuleException('New Club must not be shorter than the next club with lower loft')

        self._clubs[clubType] += [newClub]

    def remove(self, label):
        """
        find the matching Club object and remove it from the collection _clubs.
        raise EquipmentRuleException with message stating there is no such club.
        """
        for k, v in self._clubs.items():
            for i in v:
                if label == i._label:
                    print('TEST:', label, '==', i._label)
                    self._clubs[k].pop()
                    return True
        raise EquipmentRuleException('No exiting label!')

    def saveToFile(self):
        """
        construct a filename using “ownerID-owner.txt”.
        write the updated golf set specifications into the file.
        """
        fileName = f'C:/Users/HAYDEN.GOH/IdeaProjects/HelloPython/TMA/{self._ownerID}-{self._owner}.txt'
        outfile = open(fileName, 'w')

        for k, v in self._clubs.items():
            for oneLine in v:
                outfile.write(oneLine.__str__())
                outfile.write('\n')

        outfile.close()

    def getGolfSetDetails(self):
        """
        returns a string presentation the golf set, including the count of clubs in this golf set
        """
        newString = ''
        for k, v in self._clubs.items():
            for oneValue in v:
                newString += (oneValue.getDetails() + '\n')
        newString += 'No of clubs: {}\n'.format(self.numberOfClubs.__str__())
        return newString

    def __str__(self):
        text = ''
        for oneValue in self._clubs.values():
            for i in oneValue:
                text += '{}\n'.format(i)
        return text


def menuOption():
    print("Golfit Main Menu")
    print("==========================")
    print("1. Build a golf set")
    print("2. Load a golf set")
    print("0. Quit")
    option = getIntegerRange("Enter option: ", 0, 2)
    return option


def subMenuOption(owner):
    print('Club Fitting for {}'.format(owner))
    print('==========================')
    print('1. Add a club')
    print('2. Remove a club')
    print('0. Back to Main Menu')
    option = getIntegerRange("SUB: Enter choice: ", 0, 2)
    return option


def subMenu(owner, golfSet):
    while True:
        option = subMenuOption(owner)
        if option == 0:
            break
        elif option == 1:
            addClub(golfSet)
        else:
            removeClub(golfSet)


def buildGolfSet():
    try:
        ownerID = input('Enter golfer\'s ID: ')
        owner = input('Enter golfer\'s name: ')
        golfSet = GolfSet(ownerID, owner, True)
        print('\n*********************************************')
        print('Recommendation:\n'
              '- Build the set from longest to shortest club\n'
              '- i.e., from Driver to Putter')
        print('*********************************************\n')

        print('{} {}'.format(ownerID, owner))
        print('No of clubs: {}\n'.format(golfSet.numberOfClubs))
        subMenu(owner, golfSet)
    except EquipmentRuleException as e:
        print(e)
    except Exception as e:
        print(e)


def loadGolfSet():
    try:
        # golferID = input('Enter golfer\'s ID: ')
        # name = input('Enter golfer\'s name: ')
        ownerID = 'A20'
        owner = 'Marvin'
        golfSet = GolfSet(ownerID, owner, False)
        print('{} {}'.format(ownerID, owner))
        print(golfSet.getGolfSetDetails())
        subMenu(owner, golfSet)
    except EquipmentRuleException as e:
        print(e)
    except Exception as e:
        print(e)


def removeClub(golfSet):
    try:
        label = input('Enter the club label to remove: ').upper()
        if golfSet.remove(label):
            print('Removal done...\n')
            print(golfSet._ownerID, golfSet.owner)
            print(golfSet.getGolfSetDetails())
            golfSet.saveToFile()
    except EquipmentRuleException:
        print('Cannot remove as {} is not in set\n'.format(label))
        print(golfSet._ownerID, golfSet.owner)
        print(golfSet.getGolfSetDetails())
    except Exception as e:
        print(e)


def addClub(golfSet):
    try:
        """
        clubType = input('Which club type to add: ').title()
        label = input('Enter the new club label: ').upper()
        # Club Head
        loft = input('Enter clubhead loft: ')
        headWeight = input('Enter clubhead weight: ')
        if clubType == 'Wood':
            headSize = input('Enter wood size: ')
        elif clubType == 'Iron':
            headMaterial = input('Enter Iron material: ')
        else:
            headStyle = input('Enter Putter style: ')
        # 'Club Head' Object
        if clubType == 'Wood':
            clubHead = WoodHead(loft, headWeight, headSize)
        elif clubType == 'Iron':
            clubHead = IronHead(loft, headWeight, headMaterial)
        else:
            clubHead = PutterHead(loft, headWeight, headStyle)

        # Shaft
        length = input('Enter length of shaft: ')
        shaftWeight = input('Enter weight of shaft: ')
        shaftMaterial = input('Enter shaft material: ').title()
        flex = input('Enter shaft flex: ').upper()
        shaft = Shaft(length, shaftWeight, shaftMaterial, flex)
        # Grip
        diameter = input('Enter diameter of grip: ')
        gripWeight = input('Enter weight of grip: ')
        gripMaterial = input('Enter grip material: ').title()
        grip = Grip(diameter, gripWeight, gripMaterial)
        """
        # TEST DATA
        clubType = 'Wood'
        label = '3-hybrid'.upper()
        loft = 20.5
        headWeight = 250
        headSize = 22
        clubHead = WoodHead(loft, headWeight, headSize)
        length = 40
        shaftWeight = 90
        shaftMaterial = 'Graphite'
        flex = 'R'
        shaft = Shaft(length, shaftWeight, shaftMaterial, flex)
        diameter = 0.6
        gripWeight = 62
        gripMaterial = 'Rubber'
        grip = Grip(diameter, gripWeight, gripMaterial)

        # Club Object
        newClub = Club(label, clubHead, shaft, grip)

        # add to golfer's set
        golfSet.add(clubType, newClub)
        """
        Display any error or confirmation messages for this add request, then return to
    the sub menu.
        """
        print('New Club added\n')
        print(golfSet._ownerID, golfSet.owner)
        print(golfSet.getGolfSetDetails())
        golfSet.saveToFile()
    except EquipmentRuleException as e:
        print(e)
    except Exception as e:
        print(e)


def main():
    while True:
        option = menuOption()
        if option == 0:
            break
        elif option == 1:
            buildGolfSet()
        else:
            loadGolfSet()
    print("bye")

    """
    g = GolfSet('A20', 'Marvin', False)
    print(g)

    print('No. of clubs:', g.numberOfClubs)

    print(g.getClubType())

    # ADD
    head = WoodHead(17.5, 240, 280)
    shaft = Shaft(41.5, 85, 'Graphite', 'R')
    grip = Grip(0.6, 62, 'Rubber')
    newClub = Club('6-WOOD', head, shaft, grip)
    g.add('Wood', newClub)
    print('AFTER ADD..')
    print(g)

    # REMOVE
    try:
        g.remove('6-WOOD')
        print('AFTER REMOVE..')
        print(g)
    except EquipmentRuleException as e:
        print(e)

    # WRITE
    g.saveToFile()
    print('AFTER WRITE..')
    print(g)

    # getGolfSetDetails()
    print('AFTER getGolfSetDetails()..')
    print(g.getGolfSetDetails())
    """

    """
    # Question 1
    p = PutterHead(3.5, 365, 'Blade')
    print(p, p.getHeight())
    i = IronHead(37.5, 285, 'Forged')
    print(i, i.getHeight())
    w = WoodHead(9.5, 206, 450)
    print(w, w.getHeight())
    
    
    # Question 2
    # 2d.i
    try:
        grip = Grip(0.6, 62, 'Rubber')
        gClub1 = Club('Driver', WoodHead(10.5, 203, 450),
                      Shaft(45, 68, 'Graphite', 'S'), grip)
        gClub2 = Club('8-iron', IronHead(34.5, 268, 'Cast'),
                      Shaft(35.5, 109, 'Steel', 'R'), grip)
        gClub3 = Club('Sunset', PutterHead(3, 380, 'Mallet'),
                      Shaft(33, 120, 'Steel', 'S'), grip)
        gClub4 = Club('5-wood', WoodHead(17.5, 150, 280),
                      Shaft(42.5, 89, 'Steel', 'S'), grip)
        print(gClub1.weight)
        print(gClub2.weight)
        print(gClub3.weight)
        print(gClub4.weight)
    except EquipmentRuleException as e:
        print(e)
    except Exception as e:
        print('Something unexpected..', e)

    # 2d.ii
    try:
        newGrip = Grip(0.58, 75, 'Leather')
        gClub1.changeGrip(newGrip)
        gClub2.changeGrip(newGrip)
        gClub3.changeGrip(newGrip)
        gClub4.changeGrip(newGrip)

        print(gClub1.weight)
        print(gClub2.weight)
        print(gClub3.weight)
        print(gClub4.weight)
    except EquipmentRuleException as e:
        print(e)
    except Exception as e:
        print('Something unexpected..', e)
        
    """


main()
