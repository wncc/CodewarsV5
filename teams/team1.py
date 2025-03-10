from teams.helper_function import Deploy, Utils
team_name = "AGARTALA"
troops = ["Minion", "Knight", "Barbarian", "Prince", "Archer", "Princess", "Giant", "Wizard"]
deploy_list = Deploy([])
team_signal = ""
def deploy(arena_data:dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_
def logic(arena_data:dict):
    """
    WRITE YOUR CODE HERE 
    """
