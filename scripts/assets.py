from scripts.utils import *
import pandas as pd
def load_assets():
    assets = {"Blue":{},"Red":{},
        'left_side_image' : load_image('decor/4.jpg'),
        'right_side_image' : load_image('decor/5.jpg'),
        'middle_map' : load_image('decor/area middle.png'),
        'BlueCannon': load_image('tower/Blue/BlueCannon.png'),
        'RedCannon': load_image('tower/Red/RedCannon.png'), 
        'BlueTower': load_image('tower/Blue/BlueTower.png'),
        'RedTower': load_image('tower/Red/RedTower.png'),
        'BlueTower_shadow': load_image('tower/Blue/BlueTower_shadow.png'),
        'RedTower_shadow': load_image('tower/Red/RedTower_shadow.png'),
        'TowerDamaged': load_image('tower/TowerDamaged.png'),
        'archer_card': load_image('decor/card-png/archers.png'),
        'giant_card': load_image('decor/card-png/giant.png'),
        'dragon_card': load_image('decor/card-png/baby-dragon.png'),
        'prince_card': load_image('decor/card-png/prince.png'),
        'princess_card': load_image('decor/card-png/princess.png'),
        'knight_card': load_image('decor/card-png/knight.png'),
        'minion_card': load_image('decor/card-png/minions.png'),
        'barbarian_card': load_image('decor/card-png/barbarians.png'),
        'skeleton_card': load_image('decor/card-png/skeleton-army.png'),
        'balloon_card': load_image('decor/card-png/balloon.png'),
        'wizard_card': load_image('decor/card-png/wizard.png'),
        'valkyrie_card': load_image('decor/card-png/valkyrie.png'),
        'musketeer_card': load_image('decor/card-png/musketeer.png'),
        'bar_0': load_image('decor/elixir_bar/1.png'),
        'bar_1': load_image('decor/elixir_bar/1.png'),
        'bar_2': load_image('decor/elixir_bar/2.png'),
        'bar_3': load_image('decor/elixir_bar/3.png'),
        'bar_4': load_image('decor/elixir_bar/4.png'),
        'bar_5': load_image('decor/elixir_bar/5.png'),
        'bar_6': load_image('decor/elixir_bar/6.png'),
        'bar_7': load_image('decor/elixir_bar/7.png'),
        'bar_8': load_image('decor/elixir_bar/8.png'),
        'bar_9': load_image('decor/elixir_bar/9.png'),
        'bar_10': load_image('decor/elixir_bar/10.png'),
        'card_slot': load_image('decor/card-png/Deck Plank.png'),}

    directions = ["n", "s", "e", "w", "ne", "nw", "se", "sw"]
    troops = ["barbarian","prince","giant","minion","dragon","skeleton","archer","knight","princess","balloon","wizard","valkyrie","musketeer"]
    for team in ["Blue","Red"]:
        for dir in directions:
            for i in range(6):
                for troop in troops:
                    assets[team][f'{troop}_attack_{dir}_{i+1}'] = load_image(f'troops/{team}/{troop}_attack_{dir}_{i+1}.png')
                    assets[team][f'{troop}_run_{dir}_{i+1}'] = load_image(f'troops/{team}/{troop}_run_{dir}_{i+1}.png')
                    assets[team][f'{troop}_attack_{dir}_{i+1}_shadow'] = load_image(f'troops/{team}_shadows/{troop}_attack_{dir}_{i+1}.png')
                    assets[team][f'{troop}_run_{dir}_{i+1}_shadow'] = load_image(f'troops/{team}_shadows/{troop}_run_{dir}_{i+1}.png')
                                 
    for team in ["Blue","Red"]:
        for i in range(1, 7):
            assets[team][f'{team}King_{i}'] = load_image(f'tower/{team}/king_run{i}.png')
            assets[team][f'{team}KingAttack_{i}'] = load_image(f'tower/{team}/king_attack{i}.png')

    return assets