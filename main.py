from game import Game
import inspect
from teams import team1
from teams import team2

def validate_module(module, name):
    attributes = dir(module)
    
    # Expected variables and classes
    expected_variables = {"team_name", "troops", "deploy_list", "team_signal"}
    expected_classes = {"Deploy", "Utils"}
    
    # Extract variables (excluding functions, classes, and modules)
    variables = {
        attr for attr in attributes
        if not callable(getattr(module, attr))
        and not attr.startswith("__")
        and not inspect.ismodule(getattr(module, attr))
        and not inspect.isclass(getattr(module, attr))
    }
    
    # Extract classes
    classes = {
        attr for attr in attributes
        if inspect.isclass(getattr(module, attr))
    }
    
    # Condition 1: Check for exact variables and classes
    if variables != expected_variables:
        print(f"Fail: Variables do not match. Found: {variables} for {name}")
        return False
    
    if classes != expected_classes:
        print(f"Fail: Classes do not match. Found: {classes} for {name}")
        return False
    
    # Condition 3: Check len(team_signal) <= 200
    if len(module.team_signal) > 200:
        print(f"Fail: team_signal length exceeds 200 for {name}")
        return False
    
    # Condition 4: Check len(set(troops)) == 8
    if len(set(module.troops)) != 8:
        print(f"Fail: troops does not contain exactly 8 unique elements for {name}")
        return False
    
    print(f"Pass: All conditions met for {name} : {module.team_name}!")

    return True

team1_test_pass = False
team2_test_pass = False

team1_test_pass = validate_module(team1, "TEAM 1") or team1_test_pass
team2_test_pass = validate_module(team2, "TEAM 2") or team2_test_pass

if team1_test_pass and team2_test_pass:
    Game(team1.troops,team2.troops,team1.team_name,team2.team_name).run()