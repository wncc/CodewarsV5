from teams.helper_function import Troops, Utils
team_name = "MUMBAI"
troops = [Troops.minion]
deploy_list = Troops([])
team_signal = "h"
def deploy(arena_data:dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal
def logic(arena_data:dict):
    global team_signal
    """
    WRITE YOUR CODE HERE 
    """
