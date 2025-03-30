from teams.helper_function import Troops, Utils

team_name = "Harshit Somani"
troops = [Troops.skeleton, Troops.wizard, Troops.dragon, Troops.minion,
          Troops.archer, Troops.valkyrie, Troops.barbarian, Troops.prince]
deploy_list = Troops([])
team_signal = "Team Signal? TS?? TS foorrrrrr.... TANMAY SOMANI!!! ;;;3e;cccccccc"  # Slogan;ours;opps;opp_elixir;opp_deployed


def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUNCTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal


def logic(arena_data: dict):
    from teams.helper_function import Troops, Utils

    class CONSTANTS:
        STANDARD_ARENA_WIDTH = 375
        FRAMES = 6
        DOCS_OUR = (1 / 12) * 2.25 * 50

        ELIXIR_UPDATE_RATE = 0.05

    AllTroops = ["Archer", "Giant", "Dragon", "Balloon", "Prince", "Barbarian", "Knight", "Minion", "Skeleton",
                 "Wizard",
                 "Valkyrie", "Musketeer"]

    MeleeTroops = ["Archer", "Prince", "Barbarian", "Knight", "Minion", "Skeleton", "Valkyrie"]

    class Translate:
        keyboard = "0123456789" + "abcdefghijklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz".upper()
        base = len(keyboard)

        def encode(self, num):
            s = ""
            if num == 0:
                return "0"
            while num > 0:
                digit = num % self.base
                num //= self.base
                s = self.keyboard[digit] + s

            return s

        def decode(self, s):
            num = 0
            mul = 1
            for char in s[::-1]:
                num += mul * self.keyboard.find(char)
                mul *= self.base
            return num

    class TroopData:
        SLOW_ATTACK = 3
        MEDIUM_ATTACK = 2
        FAST_ATTACK = 1

        SLOW_SPEED = 1
        MEDIUM_SPEED = 3
        FAST_SPEED = 5

        DATA = [
            dict(name="Archer", elixir=3,
                 health=334, damage=118, velocity=MEDIUM_SPEED, type_="ground", attack_range=5, discovery_range=8,
                 target_type={"air": True, "ground": True, "building": True}, splash_range=0, size=0.15,
                 attack_speed=FAST_ATTACK,
                 number=2),
            dict(name="Giant", elixir=5,
                 health=5423, damage=337, velocity=SLOW_SPEED, type_="ground", attack_range=0, discovery_range=7,
                 target_type={"air": False, "ground": False, "building": True}, splash_range=0, size=0.5,
                 attack_speed=SLOW_ATTACK,
                 number=1),
            dict(name="Dragon", elixir=4,
                 health=1267, damage=176, velocity=FAST_SPEED, type_="air", attack_range=3.5, discovery_range=5,
                 target_type={"air": True, "ground": True, "building": True}, splash_range=1, size=0.4,
                 attack_speed=FAST_ATTACK,
                 number=1),
            dict(name="Balloon", elixir=5,
                 health=2226, damage=424, velocity=MEDIUM_SPEED, type_="air", attack_range=0, discovery_range=5,
                 target_type={"air": False, "ground": False, "building": True}, splash_range=1, size=0.4,
                 attack_speed=MEDIUM_ATTACK,
                 number=1),
            dict(name="Prince", elixir=5,
                 health=1920, damage=392, velocity=FAST_SPEED, type_="ground", attack_range=0, discovery_range=5,
                 target_type={"air": False, "ground": True, "building": False}, splash_range=0, size=0.3,
                 attack_speed=FAST_ATTACK,
                 number=1),
            dict(name="Barbarian", elixir=3,
                 health=736, damage=161, velocity=MEDIUM_SPEED, type_="ground", attack_range=0, discovery_range=5,
                 target_type={"air": False, "ground": True, "building": False}, splash_range=0, size=0.25,
                 attack_speed=MEDIUM_ATTACK,
                 number=3),
            dict(name="Knight", elixir=3,
                 health=1938, damage=221, velocity=MEDIUM_SPEED, type_="ground", attack_range=0, discovery_range=7,
                 target_type={"air": False, "ground": True, "building": True}, splash_range=0, size=0.3,
                 attack_speed=FAST_ATTACK,
                 number=1),
            dict(name="Minion", elixir=3,
                 health=252, damage=129, velocity=FAST_SPEED, type_="air", attack_range=2, discovery_range=4,
                 target_type={"air": True, "ground": True, "building": True}, splash_range=0, size=0.15,
                 attack_speed=FAST_ATTACK,
                 number=3),
            dict(name="Skeleton", elixir=3,
                 health=89, damage=89, velocity=FAST_SPEED, type_="ground", attack_range=0, discovery_range=4,
                 target_type={"air": False, "ground": True, "building": True}, splash_range=0, size=0.15,
                 attack_speed=FAST_ATTACK,
                 number=10),
            dict(name="Wizard", elixir=5,
                 health=1100, damage=410, velocity=MEDIUM_SPEED, type_="ground", attack_range=5.5, discovery_range=8,
                 target_type={"air": True, "ground": True, "building": True}, splash_range=1, size=0.25,
                 attack_speed=FAST_ATTACK,
                 number=1),
            dict(name="Valkyrie", elixir=4,
                 health=2097, damage=195, velocity=MEDIUM_SPEED, type_="ground", attack_range=0, discovery_range=7,
                 target_type={"air": False, "ground": True, "building": False}, splash_range=1, size=0.20,
                 attack_speed=FAST_ATTACK,
                 number=1),
            dict(name="Musketeer", elixir=4,
                 health=792, damage=239, velocity=MEDIUM_SPEED, type_="ground", attack_range=6, discovery_range=8,
                 target_type={"air": True, "ground": True, "building": True}, splash_range=0, size=0.20,
                 attack_speed=MEDIUM_ATTACK,
                 number=1)
        ]

        for D in DATA:
            D["attack_range"] *= CONSTANTS.DOCS_OUR / 5
            D["discovery_range"] *= CONSTANTS.DOCS_OUR / 5
            D["splash_range"] *= CONSTANTS.DOCS_OUR / 5
            D["size"] *= CONSTANTS.DOCS_OUR
            D["velocity"] *= 50 / CONSTANTS.STANDARD_ARENA_WIDTH

        # for d in DATA:
        #     print(d["name"])

    class Troop:
        def __init__(self, troop_name):
            self.name = troop_name
            self.elixir = 0
            self.total_health = 0
            self.damage = 0
            self.velocity = 0
            self.type = "ground"
            self.attack_range = 0
            self.discovery_range = 0
            self.target_type = {}
            self.splash_range = 0
            self.size = 0
            self.attack_speed = 0
            self.number = 1

            troops_data = TroopData.DATA
            for troop_data in troops_data:
                if troop_data["name"] == troop_name:
                    self.elixir = troop_data["elixir"]
                    self.total_health = troop_data["health"]
                    self.damage = troop_data["damage"]
                    self.velocity = troop_data["velocity"]
                    self.type = troop_data["type_"]
                    self.attack_range = troop_data["attack_range"]
                    self.discovery_range = troop_data["discovery_range"]
                    self.target_type = troop_data["target_type"]
                    self.splash_range = troop_data["splash_range"]
                    self.size = troop_data["size"]
                    self.attack_speed = troop_data["attack_speed"]
                    self.number = troop_data["number"]
                    break

        def __repr__(self):
            return self.name

    class DeployedTroop(Troop):
        def __init__(self, troop):
            super().__init__(troop.name)
            self.position = troop.position
            self.health = troop.health
            self.target = troop.target  # dummy troop of what its targetting
            self.uid = troop.uid

    class Gang:
        position = (0, 0)
        troops = []

        def __repr__(self):
            return self.troops.__repr__()

    FightResults = {
        'Archer': {'Archer': 0, 'Giant': 1, 'Dragon': 0, 'Balloon': 1, 'Prince': 0, 'Barbarian': 0.25898203592814373,
                   'Knight': 0,
                   'Minion': 0.11377245508982035, 'Skeleton': 0, 'Wizard': 0, 'Valkyrie': 0,
                   'Musketeer': 0.14221556886227546},
        'Giant': {'Archer': 0, 'Giant': 0, 'Dragon': 0, 'Balloon': 0, 'Prince': 0, 'Barbarian': 0, 'Knight': 0,
                  'Minion': 0, 'Skeleton': 0, 'Wizard': 0, 'Valkyrie': 0, 'Musketeer': 0},
        'Dragon': {'Archer': 0.44119968429360695, 'Giant': 1, 'Dragon': 0, 'Balloon': 1, 'Prince': 1, 'Barbarian': 1,
                   'Knight': 1,
                   'Minion': 0.4909234411996843, 'Skeleton': 1, 'Wizard': 0, 'Valkyrie': 1,
                   'Musketeer': 0.4340962904498816},
        'Balloon': {'Archer': 0, 'Giant': 1, 'Dragon': 0, 'Balloon': 0, 'Prince': 0, 'Barbarian': 0,
                    'Knight': 0, 'Minion': 0, 'Skeleton': 0, 'Wizard': 0, 'Valkyrie': 0, 'Musketeer': 0},
        'Prince': {'Archer': 0.4875, 'Giant': 1, 'Dragon': 0, 'Balloon': 0, 'Prince': 0,
                   'Barbarian': 0.6645833333333333,
                   'Knight': 0.4244791666666667,
                   'Minion': 0, 'Skeleton': 0, 'Wizard': 0, 'Valkyrie': 0.390625, 'Musketeer': 0.7510416666666667},
        'Barbarian': {'Archer': 0, 'Giant': 1, 'Dragon': 0, 'Balloon': 0, 'Prince': 0, 'Barbarian': 0,
                      'Knight': 0, 'Minion': 0, 'Skeleton': 0, 'Wizard': 0, 'Valkyrie': 0,
                      'Musketeer': 0.5584239130434783},
        'Knight': {'Archer': 0.2693498452012384, 'Giant': 1, 'Dragon': 0, 'Balloon': 0, 'Prince': 0,
                   'Barbarian': 0.33539731682146545, 'Knight': 0,
                   'Minion': 0, 'Skeleton': 0, 'Wizard': 0, 'Valkyrie': 0, 'Musketeer': 0.5067079463364293},
        'Minion': {'Archer': 0, 'Giant': 1, 'Dragon': 0, 'Balloon': 1, 'Prince': 1, 'Barbarian': 1, 'Knight': 1,
                   'Minion': 0, 'Skeleton': 1, 'Wizard': 0, 'Valkyrie': 1, 'Musketeer': 0.6666666666666666},
        'Skeleton': {'Archer': 0.6, 'Giant': 1, 'Dragon': 0, 'Balloon': 0, 'Prince': 0.7, 'Barbarian': 0.8,
                     'Knight': 0.7, 'Minion': 0, 'Skeleton': 0, 'Wizard': 0, 'Valkyrie': 0, 'Musketeer': 0.5},
        'Wizard': {'Archer': 1, 'Giant': 1, 'Dragon': 0.52, 'Balloon': 1, 'Prince': 0.2872727272727273, 'Barbarian': 1,
                   'Knight': 0.7990909090909091,
                   'Minion': 1, 'Skeleton': 0.9190909090909091, 'Wizard': 0, 'Valkyrie': 0.6454545454545455,
                   'Musketeer': 0.7827272727272727},
        'Valkyrie': {'Archer': 0.2684787792083929, 'Giant': 1, 'Dragon': 0, 'Balloon': 0, 'Prince': 0,
                     'Barbarian': 0.5393419170243204,
                     'Knight': 0, 'Minion': 0, 'Skeleton': 0.9151168335717692, 'Wizard': 0, 'Valkyrie': 0,
                     'Musketeer': 0.5441106342393897},
        'Musketeer': {'Archer': 0, 'Giant': 1, 'Dragon': 0, 'Balloon': 1, 'Prince': 0, 'Barbarian': 0,
                      'Knight': 0, 'Minion': 0, 'Skeleton': 0, 'Wizard': 0, 'Valkyrie': 0, 'Musketeer': 0}}

    FightResults["Dragon"]["Prince"] = 0.5
    FightResults["Minion"]["Prince"] = 0.5

    WizardCounters = ['Valkyrie', 'Prince', 'Wizard', 'Knight', 'Skeleton', 'Barbarian']

    TowerResults = {
        'Archer': 118,
        'Giant': 1348,
        'Dragon': 1056,
        'Balloon': 1696,
        'Prince': 3136,
        'Barbarian': 322,
        'Knight': 1105,
        'Minion': 258,
        'Skeleton': 1513,
        'Wizard': 1640,
        'Valkyrie': 1365,
        'Musketeer': 478,
    }

    Attacks = [
        [
            [
                (Troops.barbarian, (0, 0)),
                (Troops.wizard, (0, -15))
            ],
            []
        ],
        [
            [
                (Troops.dragon, (0, 0)),
                (Troops.prince, (0, -5)),
            ],
            [Troops.wizard]
        ],
        [
            [
                (Troops.valkyrie, (0, 0)),
                (Troops.wizard, (0, -5)),
            ],
            []
        ],
        [
            [
                (Troops.prince, (0, 0)),
                (Troops.minion, (0, -5)),
            ],
            [Troops.wizard]
        ],
        [
            [
                (Troops.dragon, (0, 0)),
                (Troops.minion, (0, -5)),
            ],
            [Troops.wizard]
        ],
        [
            [
                (Troops.prince, (0, 0)),
                (Troops.skeleton, (0, -5)),
            ],
            [Troops.wizard, Troops.valkyrie, Troops.dragon]
        ],

    ]

    import random
    import math
    global team_signal

    # print(team_signal)

    translator = Translate()

    ours = list(map(DeployedTroop, arena_data["MyTroops"]))
    opps = list(map(DeployedTroop, arena_data["OppTroops"]))

    winning = arena_data["MyTower"].health > arena_data["OppTower"].health
    double_elixir = arena_data["MyTower"].game_timer >= 1200

    # print("My tower:", arena_data["MyTower"].health)
    # print("Opptower:", arena_data["OppTower"].health)
    # print()

    team_signal_data = team_signal.split(';')

    def get_existed(s):
        """
        gets list of list of uids acc to team_signal
        """
        if s == '':
            existed = []
        else:
            existed = list(map(lambda x: list(range(translator.decode(x.split('-')[0]),
                                                    translator.decode(x.split('-')[0]) + translator.decode(
                                                        x.split('-')[1]))), s.split(',')))
        return existed

    our_existed = get_existed(team_signal_data[1])  # uids list
    opp_existed = get_existed(team_signal_data[2])
    opp_elixir = translator.decode(team_signal_data[3]) / 20
    opp_deployed = list(map(translator.decode, list(team_signal_data[4])))

    def get_new_existed(opps, opp_existed):
        """
        gets new troops and returns them, and also updates existing uid list of list
        """
        new_uids = []
        for opp in opps:
            for exist in opp_existed:
                if opp.uid in exist:
                    break
            else:
                new_uids.append((opp.name, opp.uid, opp))

        try:
            new_uids = sorted(new_uids)
        except BaseException as e:
            print(e)

        _new_opps = []
        i = 0
        while i < len(new_uids):
            opp = new_uids[i][2]
            _new_opps.append(opp)
            i += opp.number
            opp_existed.append(list(range(opp.uid, opp.uid + opp.number)))

        return _new_opps

    new_ours = get_new_existed(ours, our_existed)  # object first
    new_opps = get_new_existed(opps, opp_existed)

    def update_opp_elixir():
        nonlocal opp_elixir
        nonlocal new_opps
        nonlocal team_signal_data

        if double_elixir:
            elixir_mux = 2
        else:
            elixir_mux = 1
        opp_elixir = min(opp_elixir + elixir_mux * CONSTANTS.ELIXIR_UPDATE_RATE, 10)

        for new_opp in new_opps:
            opp_elixir -= new_opp.elixir

        team_signal_data[3] = translator.encode(round(opp_elixir * 20))

    update_opp_elixir()

    def update_existed(old_existed, current):
        """
        removes uids that are no longer on the field, all existing groups ka one object returned
        """
        new_existed_uids = []
        groups = []
        for exist in old_existed:
            for t in current:
                if t.uid in exist:
                    new_existed_uids.append(exist)
                    groups.append(t)
                    break

        return new_existed_uids, groups

    new_ours_existed, our_groups = update_existed(our_existed, ours)
    new_opps_existed, opp_groups = update_existed(opp_existed, opps)

    def format_existed(existed):
        return ','.join(['-'.join([translator.encode(new_exist[0]), translator.encode(len(new_exist))]) for new_exist in
                         existed])

    team_signal_data[1] = format_existed(new_ours_existed)
    team_signal_data[2] = format_existed(new_opps_existed)

    def update_opp_deployed():
        nonlocal new_opps
        nonlocal opp_deployed
        for opp in new_opps:
            opp_deployed.append(AllTroops.index(opp.name))

        opp_deployed = opp_deployed[-16:]

    update_opp_deployed()

    def format_opp_deployed():
        return "".join(list(map(translator.encode, opp_deployed)))

    team_signal_data[4] = format_opp_deployed()

    if arena_data["MyTower"].game_timer <= 2:
        team_signal = ';'.join(team_signal_data)
        return

    our_groups = sorted(our_groups, key=lambda x: -x.position[1])
    opp_groups = sorted(opp_groups, key=lambda x: x.position[1])

    engaging_pairs = []
    unengaging_opps = []
    enganged_ours = []
    future_unengaging_opps = []

    for i, opp in enumerate(opp_groups):
        enganged = False
        for j, our in enumerate(our_groups):
            if j in enganged_ours:
                continue
            if (our.position[1] < opp.position[1] + opp.size + our.size and abs(our.position[0] - opp.position[0]) <
                    max(opp.discovery_range, our.discovery_range)):  # ignoring sizes for buffer
                enganged = True
                enganged_ours.append(j)
                engaging_pairs.append((our, opp))
                break

        if not enganged:
            if opp.position[1] <= 50:
                unengaging_opps.append(opp)
            else:
                future_unengaging_opps.append(opp)

    if winning:
        attack = False
    else:
        attack = True

        frames_passed = 0
        for opp in opps:
            if opp.position[1] < 50:
                starting_pos = Utils.calculate_distance(opp.position, (0, 0), False) - opp.velocity * frames_passed
                tower_shooting_pos = arena_data["MyTower"].attack_range + arena_data["MyTower"].size + opp.size
                if starting_pos > tower_shooting_pos:
                    frames_passed += (starting_pos - tower_shooting_pos) / opp.velocity
                    starting_pos = tower_shooting_pos

                distance = starting_pos - (opp.attack_range + arena_data["MyTower"].size + opp.size)
                reach_frames = math.floor(distance / opp.velocity)
                hits = math.ceil(opp.health / arena_data["MyTower"].damage)
                kill_frames = hits * TroopData.FAST_ATTACK * CONSTANTS.FRAMES

                # print(reach_frames, kill_frames)
                if reach_frames < kill_frames:
                    attack = False
                    break
                else:
                    frames_passed += kill_frames

    # print(attack)

    def strike():
        for combo in Attacks:
            attack = combo[0]
            troopies = [a[0] for a in attack]
            if all(i in arena_data["MyTower"].deployable_troops for i in troopies):
                if arena_data["MyTower"].total_elixir >= sum(Troop(troop).elixir for troop in troopies):
                    # print("\nGO")
                    for avoid in combo[1]:
                        for opp in opps:
                            if opp.name == avoid:
                                if opp.position[0] < 0:
                                    base_position = (20, 50)
                                else:
                                    base_position = (-20, 50)
                                break
                        else:
                            continue
                        break
                    else:
                        base_position = random.choice([(-20, 50), (20, 50)])

                    for t, p in attack:
                        deploy_list.list_.append((t, (base_position[0] + p[0], base_position[1] + p[1])))

                    return False
                # else:
                #     if double_elixir:
                #         return True # wait for it
            if len(attack) == 2:
                for t1, t2 in (attack, attack[::-1]):
                    # print(t1, t2)
                    for our in ours:
                        if our.name == t1[0]:
                            buffer = 5
                            if 50 + t1[1][1] - buffer <= our.position[1] <= 50 + t1[1][1] + buffer:
                                if t2[0] in arena_data["MyTower"].deployable_troops:
                                    if arena_data["MyTower"].total_elixir >= Troop(t2[0]).elixir:
                                        # print("\nCON")
                                        deploy_list.list_.append((t2[0], (our.position[0], 50 + t2[1][1])))
                                        return False
                                        # print("our", our.position)
                                        # print("new", 50 + t2[1][1])
        return False

    def neutralize(deployable, new_opp):
                if deployable.attack_range < new_opp.attack_range:
                    pos = new_opp.position
                else:
                    pos = (new_opp.position[0],
                           new_opp.position[1] - new_opp.size - deployable.size - deployable.attack_range)

                for engager_our, engager_opp in engaging_pairs:  # if already boom boom, place behind our engaged troop
                    if engager_our.position[1] < new_opp.position[1]:
                        if (pos[1] < engager_opp.position[1] + engager_opp.size + deployable.size +
                                max(engager_opp.discovery_range, deployable.discovery_range) and
                                abs(pos[0] - engager_opp.position[0]) <
                                engager_opp.size + deployable.size +
                                max(engager_opp.discovery_range, deployable.discovery_range)):
                            frames_until_encounter = math.ceil((engager_opp.position[1] - engager_our.position[1] -
                                                                max(engager_our.attack_range, engager_opp.attack_range)) /
                                                               (engager_opp.velocity + engager_our.velocity))
                            position_at_encounter = engager_our.position[1] + engager_our.velocity * frames_until_encounter
                            deployable_position_at_encounter = position_at_encounter - 10
                            pos = (pos[0], deployable_position_at_encounter - deployable.velocity * frames_until_encounter)

                if pos[0] < -25:
                    pos = (-25, pos[1])
                elif pos[0] > 25:
                    pos = (25, pos[1])

                if pos[1] < 0:
                    pos = (pos[0], 0)
                elif pos[1] > 50:
                    pos = (pos[0], 50)

                if arena_data["MyTower"].total_elixir >= deployable.elixir:
                    # print(deployable.name, new_opp.name, macks[0])
                    deploy_list.list_.append((deployable.name, pos))
                    # print(deployable.name, new_opp.name)
                    return True # successful
                else:
                    return False # unsuccessful

    def defend(opp_side=False):
        ppl_to_beat_up = future_unengaging_opps if opp_side else unengaging_opps
        # ppl_to_beat_up = unengaging_opps

        # print(ppl_to_beat_up)
        for new_opp in ppl_to_beat_up:
            # print(new_opp.name)

            urgent = (Utils.calculate_distance(new_opp.position, (0, 0), False) <
                      new_opp.attack_range + arena_data["MyTower"].size + new_opp.size + 5)

            if not urgent:
                if not opp_side:
                    for wiz in opps:
                        if wiz.name == Troops.wizard and wiz.position[1] < 50:
                            for counter in WizardCounters:
                                if counter in arena_data["MyTower"].deployable_troops:
                                    if arena_data["MyTower"].total_elixir >= Troop(counter).elixir:
                                        deploy_list.list_.append((counter, wiz.position))
                                        break

            macks = (-69, None)
            for deployable_name in arena_data["MyTower"].deployable_troops:

                if urgent and Troop(deployable_name).elixir > arena_data["MyTower"].total_elixir:
                    continue
                enemy_health = FightResults[new_opp.name][deployable_name]
                my_health = FightResults[deployable_name][new_opp.name]
                macks = max(macks, (my_health - enemy_health, deployable_name))

            if macks[1] is None:
                return

            # if opp_side:
            #     if macks[0] < -0.5 or (not winning and arena_data["MyTower"].game_timer > 1200):
            #         return

            if macks[0] < -0.5:
                if (Utils.calculate_distance(new_opp.position, (0, 0), False) >
                        arena_data["MyTower"].attack_range + arena_data["MyTower"].size + new_opp.size):   #if not in tower range, leave
                    if arena_data["MyTower"].total_elixir < 10: # unless elixir >= 10
                        return True

            if True:  # opp_side or Utils.calculate_distance(new_opp.position, (0, 0), False) < arena_data["MyTower"].attack_range + arena_data["MyTower"].size + new_opp.size:
                deployable = Troop(macks[1])
                if not neutralize(deployable, new_opp):
                    return True # defence pending

        return False

    def backup():
        if len(opp_groups) == 0:
            return
        new_opp = opp_groups[0]

        macks = (-69, None)
        for deployable_name in arena_data["MyTower"].deployable_troops:
            enemy_health = FightResults[new_opp.name][deployable_name]
            my_health = FightResults[deployable_name][new_opp.name]
            macks = max(macks, (my_health - enemy_health, deployable_name))

        deployable = Troop(macks[1])
        if not neutralize(deployable, new_opp):
            return

    def random_attack():
        macks = (-69, None)
        for deployable_name in arena_data["MyTower"].deployable_troops:
            macks = max(macks, (TowerResults[deployable_name], deployable_name))

        deploy_list.list_.append((macks[1], (0, 50)))

    strike()
    if attack:
        if not winning:
            strike()
        defence_pending = defend(opp_side=True)

    else:
        defence_pending = defend(opp_side=False)

    if not defence_pending:
        if arena_data["MyTower"].total_elixir >= 10 or (winning and arena_data["MyTower"].total_elixir >= opp_elixir + 3):
            backup()

        if len(opps) == 0:
            random_attack()

    # print(engaging_pairs)
    # print(unengaging_opps)
    # print(future_unengaging_opps)
    # print()

    # print(*list(map(lambda x: AllTroops[x] if x < 12 else "NA", opp_deployed)))

    team_signal = ';'.join(team_signal_data)
    if len(team_signal) > 200:
    	team_signal = "Team Signal? TS?? TS foorrrrrr.... TANMAY SOMANI!!! ;;;3e;cccccccc"