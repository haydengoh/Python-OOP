from ClubHead import IronHead, PutterHead, WoodHead

class playground:
    _CLUBTYPE = ['Wood', 'Iron', 'Putter']

    def __init__(self, ownerID, owner, newSet):
        self._ownerID = ownerID
        self._owner = owner
        self._clubs = {"Wood":[ ], "Iron":[ ], "Putter":[ ]}

        if newSet is True:
            return
        else:
            fileName = f'{ownerID}-{owner}.txt'
            infile = open(fileName, 'r')

            for oneLine in infile:
                newList = []
                newList.append(oneLine.split(','))
                # label, loft, hWeight, hSub, length, sWeight, sMaterial, flex, diamater, gWeight, gMaterial = oneLine.split(',')
                

def main():
    # p = playground('A20', 'Marvin', False)

    _CLUBTYPE = ['Wood', 'Iron', 'Putter']

    dict = {"Wood":[ ], "Iron":[ ], "Putter":[ ]}


    fileName = '/Users/haydengoh/VS Code/ICT162/TMA/A20-Marvin.txt'
    infile = open(fileName, 'r')
    # newList = []
    for oneLine in infile:
        newList = []
        newList.append(oneLine.split(','))
        dict[newList[0][1]] = [newList[0][2], newList[0][3], newList[0][4]]
    print(dict)


main()
