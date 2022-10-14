from abc import ABC, abstractmethod
from collections import Counter


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
        return self._size / 400

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

# 1c


def main():
    p = PutterHead(3.5, 365, 'Blade')
    print(p, p.getHeight())
    i = IronHead(37.5, 285, 'Forged')
    print(i, i.getHeight())
    w = WoodHead(9.5, 206, 450)
    print(w, w.getHeight())


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
        if diameter == 0.6 or diameter == 0.58:
            self._diameter = diameter
        self._weight = weight
        if material == 'RUBBER' or material == 'LEATHER' or material == 'SYNTHETIC':
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
        self._label = label
        self._head = head
        self._shaft = shaft
        self._grip = grip
        """
        1. Weight of head must be more than the combined weight of the shaft and grip.
        2. Assembled club length must be within 18 to 48 inches.
        Otherwise, raise EquipmentRuleException with appropriate message
        """
        if head.weight < (shaft.weight + grip.weight):
            raise EquipmentRuleException(
                'Club Weight must be more than shaft & grip weight!')
        if 18 > (shaft.length + head.getHeight()) > 48:
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
        return self._shaft.length + self._head.getHeight()

    @property  # accessor / getter method
    def weight(self):
        """
        Weight of the club is the total weight of clubhead, shaft and grip.
        """
        return self._head.weight + self._shaft.weight + self._grip.weight

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
        return "Club: {}\t Loft: {}\t Length: {}in\t Flex: {}\t Weight: {}g".format(self._label, self.loft, self.length, self.flex, self.weight)

    def __str__(self):
        """
        returns the label of the club, follow by the string representations of clubhead, shaft and grip.
        """
        return "{},{},{},{}".format(self._label, self._head, self._shaft, self._grip)

# 2d


def main():
    # 2d.i
    try:
        grip = Grip(0.6, 62, 'rubber'.upper())
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
        print(e)  # print
    except Exception as e:
        print('Something unexpected..', e)

    # 2d.ii
    try:
        newGrip = Grip(0.58, 75, 'leather'.upper())
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
        print('Something unexpected..', e)  # print


class GolfSet:
    _CLUBTYPE = ['Wood', 'Iron', 'Putter']

    def __init__(self, ownerID, owner, newSet):
        self._ownerID = ownerID
        self._owner = owner
        self._clubs = {"Wood": [], "Iron": [], "Putter": []}

        if newSet is True:
            return
        # populate Club objects into _clubs
        else:
            fileName = f'/Users/haydengoh/VS Code/ICT162/TMA/{ownerID}-{owner}.txt'
            if not fileName:
                raise EquipmentRuleException('File is not file!')

            infile = open(fileName, 'r')
            for oneLine in infile:
                newList = []
                newList.append(oneLine.split(','))
                # store in _clubs
                self._clubs[newList[0][1]] = [
                    newList[0][2], newList[0][3], newList[0][4]]

            infile.close()

    @property
    def owner(self):
        return self._owner

    @property
    def numberOfClubs(self):
        """
        sum of all clubs in the 3 categories of golf clubs.
        """
        return Counter(self._clubs.keys())

    @classmethod
    def getClubType(cls):
        pass

    def __str__(self):
        return "{}".format(self._clubs)


def main():
    g = GolfSet('A20', 'Marvin', False)
    print(g)

    print(g.numberOfClubs)


# main()
