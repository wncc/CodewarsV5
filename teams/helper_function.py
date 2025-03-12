import math

class Troops:

    archer = "Archer"
    giant = "Giant"
    dragon = "Dragon"
    balloon = "Balloon"
    prince = "Prince"
    barbarian = "Barbarian"
    knight = "Knight"
    minion = "Minion"
    skeleton = "Skeleton"
    wizard = "Wizard"
    valkyrie = "Valkyrie"
    musketeer = "Musketeer"

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
        
    def deploy_wizard(self,location):
        self.list_.append(("Wizard",location))

    def deploy_dragon(self,location):
        self.list_.append(("Dragon",location))

    def deploy_balloon(self,location):
        self.list_.append(("Balloon",location))

    def deploy_skeleton(self,location):
        self.list_.append(("Skeleton",location))
        
    def deploy_valkyrie(self,location):
        self.list_.append(("Valkyrie",location))
    
    def deploy_musketeer(self,location):
        self.list_.append(("Musketeer",location))


class Utils:

    @staticmethod
    def calculate_distance(A, B, type_troop = True):
        if type_troop:
            return math.sqrt((A.position[0] - B.position[0])**2 + (A.position[1] - B.position[1])**2)
        return math.sqrt((A[0] - B[0])**2 + (A[1] - B[1])**2)
    
    @staticmethod
    def is_in_range(troop1, troop2, troop1_range):
        return Utils.calculate_distance(troop1, troop2) <= troop1.size + troop2.size + troop1_range
