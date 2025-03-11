import math

class Troops:

    minion = "Minion"
    archer = "Archer"
    giant = "Giant"
    dragon = "Dragon"
    balloon = "Balloon"
    prince = "Prince"
    barbarian = "Barbarian"
    princess ="Princess"
    knight = "Knight"
    minion = "Minion"
    skeleton = "Skeleton"
    wizard = "Wizard"

    def __init__(self, list_):
        self.list_ = list_

    def deploy_archer(self,location):
        self.list_.append(("Archer",location))

    def deploy_giant(self,location):
        self.list_.append(("Giant",location))

    def deploy_minion(self,location):
        self.list_.append(("Minion",location))

    def deploy_prince(self,location):
        self.list_.append(("Prince",location))

    def deploy_barbarian(self,location):
        self.list_.append(("Barbarian",location))

    def deploy_knight(self,location):
        self.list_.append(("Knight",location))

    def deploy_princess(self,location):
        self.list_.append(("Princess",location))
        
    def deploy_wizard(self,location):
        self.list_.append(("Wizard",location))


class Utils:

    @staticmethod
    def calculate_distance(A, B, type_troop = False):
        if type_troop:
            return math.sqrt((A.position[0] - B.position[0])**2 + (A.position[1] - B.position[1])**2)
        return math.sqrt((A[0] - B[0])**2 + (A[1] - B[1])**2)
    
    @staticmethod
    def is_in_range(troop1, troop2, troop1_range):
        return Utils.calculate_distance(troop1.position, troop2.position, type_troop = True) <= troop1.size + troop2.size + troop1_range