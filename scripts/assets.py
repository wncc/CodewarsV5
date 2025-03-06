from scripts.utils import *
def load_assets():
    assets = {"Blue":{},"Red":{},
        'arena' : load_image('decor/arena.png'),
        'middle_map' : load_image('decor/Arena-1 Middle.png'),
        'BlueCannon': load_image('tower/BlueCannon.png'),
        'RedCannon': load_image('tower/RedCannon.png'), 
        'BlueKing': load_image('tower/BlueKing.png'),
        'RedKing': load_image('tower/RedKing.png'),
        'BlueKingAttack': load_image('tower/BlueKingAttack.png'),
        'RedKingAttack': load_image('tower/RedKingAttack.png'),
        'BlueTower': load_image('tower/BlueTower.png'),
        'RedTower': load_image('tower/RedTower.png'),
        'TowerDamaged': load_image('tower/TowerDamaged.png'),}
    directions = ["n", "s", "e", "w", "ne", "nw", "se", "sw"]
    troops = ["barbarian","prince","giant","minion","dragon","skeleton"]
    for team in ["Blue","Red"]:
        for dir in directions:
            for i in range(6):
                for troop in troops:
                    assets[team][f'{troop}_attack_{dir}_{i+1}'] = load_image(f'troops/{team}/{troop}_attack_{dir}_{i+1}.png')
                    assets[team][f'{troop}_run_{dir}_{i+1}'] = load_image(f'troops/{team}/{troop}_run_{dir}_{i+1}.png')
    # assets = {
    #     # "Blue":{
    #     #     'ArcherBack': load_image('troops/Blue/BlueArcherBack.png'),
    #     #     'ArcherFront': load_image('troops/Blue/BlueArcherFront.png'),
    #     #     'BarbarianBack': load_image('troops/Blue/BlueBarbarianBack.png'),
    #     #     'BarbarianFront': load_image('troops/Blue/BlueBarbarianFront.png'),
    #     #     'BombTower': load_image('troops/Blue/BlueBombTower.png'),
    #     #     'DragonBack': load_image('troops/Blue/BlueDragonBack.png'),
    #     #     'DragonFront': load_image('troops/Blue/BlueDragonFront.png'),
    #     #     'GiantBack': load_image('troops/Blue/BlueGiantBack.png'),
    #     #     'GiantFront': load_image('troops/Blue/BlueGiantFront.png'),
    #     #     'MinionBack': load_image('troops/Blue/BlueMinionBack.png'),
    #     #     'MinionFront': load_image('troops/Blue/BlueMinionFront.png'),
    #     #     'PrinceBack': load_image('troops/Blue/BluePrinceBack.png'),
    #     #     'PrinceFront': load_image('troops/Blue/BluePrinceFront.png'),
    #     #     'PrincessBack': load_image('troops/Blue/BluePrincessBack.png'),
    #     #     'PrincessFront': load_image('troops/Blue/BluePrincessFront.png'),
    #     #     'ArcherBackAttack': load_image('troops/Blue/BlueArcherBackAttack.png'),
    #     #     'ArcherFrontAttack': load_image('troops/Blue/BlueArcherFrontAttack.png'),
    #     #     'BarbarianBackAttack': load_image('troops/Blue/BlueBarbarianBackAttack.png'),
    #     #     'BarbarianFrontAttack': load_image('troops/Blue/BlueBarbarianFrontAttack.png'),
    #     #     'BombTowerAttack': load_image('troops/Blue/BlueBombTowerAttack.png'),
    #     #     'DragonBackAttack': load_image('troops/Blue/BlueDragonBackAttack.png'),
    #     #     'DragonFrontAttack': load_image('troops/Blue/BlueDragonFrontAttack.png'),
    #     #     'GiantBackAttack': load_image('troops/Blue/BlueGiantBackAttack.png'),
    #     #     'GiantFrontAttack': load_image('troops/Blue/BlueGiantFrontAttack.png'),
    #     #     'MinionBackAttack': load_image('troops/Blue/BlueMinionBackAttack.png'),
    #     #     'MinionFrontAttack': load_image('troops/Blue/BlueMinionFrontAttack.png'),
    #     #     'PrinceBackAttack': load_image('troops/Blue/BluePrinceBackAttack.png'),
    #     #     'PrinceFrontAttack': load_image('troops/Blue/BluePrinceFrontAttack.png'),
    #     #     'PrincessBackAttack': load_image('troops/Blue/BluePrincessBackAttack.png'),
    #     #     'PrincessFrontAttack': load_image('troops/Blue/BluePrincessFrontAttack.png')
    #     # },

    #     # "Red":{
    #     #     'ArcherBack': load_image('troops/Red/RedArcherBack.png'),
    #     #     'ArcherFront': load_image('troops/Red/RedArcherFront.png'),
    #     #     'BarbarianBack': load_image('troops/Red/RedBarbarianBack.png'),
    #     #     'BarbarianFront': load_image('troops/Red/RedBarbarianFront.png'),
    #     #     'BombTower': load_image('troops/Red/RedBombTower.png'),
    #     #     'DragonBack': load_image('troops/Red/RedDragonBack.png'),
    #     #     'DragonFront': load_image('troops/Red/RedDragonFront.png'),
    #     #     'GiantBack': load_image('troops/Red/RedGiantBack.png'),
    #     #     'GiantFront': load_image('troops/Red/RedGiantFront.png'),
    #     #     'MinionBack': load_image('troops/Red/RedMinionBack.png'),
    #     #     'MinionFront': load_image('troops/Red/RedMinionFront.png'),
    #     #     'PrinceBack': load_image('troops/Red/RedPrinceBack.png'),
    #     #     'PrinceFront': load_image('troops/Red/RedPrinceFront.png'),
    #     #     'PrincessBack': load_image('troops/Red/RedPrincessBack.png'),
    #     #     'PrincessFront': load_image('troops/Red/RedPrincessFront.png'),
    #     #     'ArcherBackAttack': load_image('troops/Red/RedArcherBackAttack.png'),
    #     #     'ArcherFrontAttack': load_image('troops/Red/RedArcherFrontAttack.png'),
    #     #     'BarbarianBackAttack': load_image('troops/Red/RedBarbarianBackAttack.png'),
    #     #     'BarbarianFrontAttack': load_image('troops/Red/RedBarbarianFrontAttack.png'),
    #     #     'BombTowerAttack': load_image('troops/Red/RedBombTowerAttack.png'),
    #     #     'DragonBackAttack': load_image('troops/Red/RedDragonBackAttack.png'),
    #     #     'DragonFrontAttack': load_image('troops/Red/RedDragonFrontAttack.png'),
    #     #     'GiantBackAttack': load_image('troops/Red/RedGiantBackAttack.png'),
    #     #     'GiantFrontAttack': load_image('troops/Red/RedGiantFrontAttack.png'),
    #     #     'MinionBackAttack': load_image('troops/Red/RedMinionBackAttack.png'),
    #     #     'MinionFrontAttack': load_image('troops/Red/RedMinionFrontAttack.png'),
    #     #     'PrinceBackAttack': load_image('troops/Red/RedPrinceBackAttack.png'),
    #     #     'PrinceFrontAttack': load_image('troops/Red/RedPrinceFrontAttack.png'),
    #     #     'PrincessBackAttack': load_image('troops/Red/RedPrincessBackAttack.png'),
    #     #     'PrincessFrontAttack': load_image('troops/Red/RedPrincessFrontAttack.png')
    #     # },

    #     'tiles': load_image('tiles/tile.png'),
    #     'rock' : load_image('tiles/rock.png'),
    #     'BlueCannon': load_image('tower/BlueCannon.png'),
    #     'RedCannon': load_image('tower/RedCannon.png'), 
    #     'BlueKing': load_image('tower/BlueKing.png'),
    #     'RedKing': load_image('tower/RedKing.png'),
    #     'BlueKingAttack': load_image('tower/BlueKingAttack.png'),
    #     'RedKingAttack': load_image('tower/RedKingAttack.png'),
    #     'BlueTower': load_image('tower/BlueTower.png'),
    #     'RedTower': load_image('tower/RedTower.png'),
    #     'TowerDamaged': load_image('tower/TowerDamaged.png'),
    # }

    return assets