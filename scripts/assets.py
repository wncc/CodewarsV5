from scripts.utils import *
import pandas as pd
def load_assets():
    assets = {"Blue":{},"Red":{},
        'left_side_image' : load_image('decor/left.png'),
        'right_side_image' : load_image('decor/right.png'),
        'middle_map' : load_image('decor/Arena-1 Middle.png'),
        'BlueCannon': load_image('tower/Blue/BlueCannon.png'),
        'RedCannon': load_image('tower/Red/RedCannon.png'), 
        'BlueTower': load_image('tower/Blue/BlueTower.png'),
        'RedTower': load_image('tower/Red/RedTower.png'),
        'TowerDamaged': load_image('tower/TowerDamaged.png'),
        'archer_card': load_image('decor/card-png/archers.png'),
        'giant_card': load_image('decor/card-png/giant.png'),
        'dragon_card': load_image('decor/card-png/baby-dragon.png'),
        'prince_card': load_image('decor/card-png/prince.png'),
        'princes_card': load_image('decor/card-png/princess.png'),
        'knight_card': load_image('decor/card-png/knight.png'),
        'minion_card': load_image('decor/card-png/minions.png'),
        'barbarian_card': load_image('decor/card-png/barbarians.png'),
        'skeleton_card': load_image('decor/card-png/skeleton-army.png'),
        'balloon_card': load_image('decor/card-png/balloon.png'),}

    directions = ["n", "s", "e", "w", "ne", "nw", "se", "sw"]
    troops = ["barbarian","prince","giant","minion","dragon","skeleton","archer","knight","princess","balloon"]
    for team in ["Blue","Red"]:
        for dir in directions:
            for i in range(6):
                for troop in troops:
                    assets[team][f'{troop}_attack_{dir}_{i+1}'] = load_image(f'troops/{team}/{troop}_attack_{dir}_{i+1}.png')
                    assets[team][f'{troop}_run_{dir}_{i+1}'] = load_image(f'troops/{team}/{troop}_run_{dir}_{i+1}.png')
                                 
    for team in ["Blue","Red"]:
        for i in range(1, 7):
            assets[team][f'{team}King_{i}'] = load_image(f'tower/{team}/king_run{i}.png')
            assets[team][f'{team}KingAttack_{i}'] = load_image(f'tower/{team}/king_attack{i}.png')

    return assets