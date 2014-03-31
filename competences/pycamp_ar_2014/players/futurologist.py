# coding: utf-8
import random
import sys
import codecs

import utils
from things import Player, Zombie, Wall, Box
from utils import closest
from weapons import Rifle, Shotgun


names = """Chen Tuan
Ge Hong
Laozi
Lie Yukou
Yang Xiong
Zhang Daoling
Zhang Jue
Zhang Sanfeng
Zhuangzi
Darni""".split("\n")


class GoalDistanceMap(object):
    def __init__(self, goal, things):
        self.things = things
        mx = max(t[0] for t in things) + 2
        my = max(t[1] for t in things) + 2
        self.size = mx, my
        self.goal = goal
        self.map = [[None] * my for _ in range(mx)]

        self.build()

    def __getitem__(self, item):
        if item[0] < 0 or item[1] < 0:
            return float("+inf")
        try:
            return self.map[item[0]][item[1]]
        except IndexError:
            return float("+inf")

    def build(self):
        #print "goal", self.goal
        #print "size", self.size
        if isinstance(self.goal, list):
            for g in self.goal:
                self.map[g[0]][g[1]] = 0
        else:
            self.map[self.goal[0]][self.goal[1]] = 0
        count = 0
        while True:
            changed = False
            for y in range(self.size[1]):
                for x in range(self.size[0]):
                    thing = self.things.get((x, y), None)

                    if thing is not None:
                        if isinstance(thing, Wall) or isinstance(thing, Box):
                            self.map[x][y] = float("+inf")
                            continue
                    v = self.map[x][y]

                    if v is None:
                        for p in utils.adjacent_positions((x, y)):
                            cv = self[p]

                            if cv == count:
                                self.map[x][y] = cv + 1
                                changed = True

            if not changed:
                break

            count += 1

    def show(self):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if x > 30:
                    continue
                thing = self.things.get((x, y), None)
                if thing is not None:
                    if isinstance(thing, Wall):
                        sys.stdout.write("##|")
                        continue
                    if isinstance(thing, Box):
                        sys.stdout.write("==|")
                        continue
                v = self.map[x][y]

                if isinstance(v, int):
                    if v > 99:
                        sys.stdout.write("**|")
                    else:
                        sys.stdout.write("%02d|" % v)
                else:
                    sys.stdout.write("XX|")
                    #print


class State(object):
    cover_1_map = None
    cover_2_map = None
    cover_3_map = None
    goal_map = None
    tick = 0
    number_players = 0
    played = 0
    last_action = 0
    strategy = None
    next_strategy = "first_strategy"
    strategy_name = None


S = State()


class FuturologistSafehouse(Player):
    """A player that stays still and shoots zombies."""
    futurologist = True

    def next_step(self, things, t=None):

        if S.played == 0:
            # lead a change in strategy
            S.tick += 1
            if S.next_strategy is not None:
                S.strategy = getattr(self, 'build_' + S.next_strategy)(things)
                S.strategy_name = S.next_strategy
                S.next_strategy = None

        S.played += 1
        if S.played == len([x for x in things.values() if isinstance(x, Player)]):
            S.played = 0

        result = S.strategy.get_next_move(self, things)

        self.status = S.strategy_name + "|" + str(S.tick) + "|" + str(result)
        return result

    def build_first_strategy(self, things):
        return RushStrategy(things, (86, 25), "dos")

    def build_dos(self, things):
        return RushStrategy(things, [(93, 15), (94, 15)], "tres")

    def build_tres(self, things):
        return RushStrategy(things, (93, 8), "cuatro")

    def build_cuatro(self, things):
        return RushStrategy(things, (93, 0), "cinco")

    def build_cinco(self, things):
        return RushStrategy(things, (85, 0), "seis")

    def build_seis(self, things):
        return RushStrategy(things, (73, 0), "siete")

    def build_siete(self, things):
        return RushStrategy(things, (61, 0), "ocho")

    def build_ocho(self, things):
        return RushStrategy(things, (49, 0), "nueve")

    def build_nueve(self, things):
        return RushStrategy(things, (37, 0), "diez")

    def build_diez(self, things):
        return RushStrategy(things, (25, 0), "once")

    def build_once(self, things):
        return RushStrategy(things, (13, 0), "goal")

    def build_goal(self, things):
        return RushStrategy(things, (2, 2), "siete")


class FuturologistExtermination(Player):
    """A player that stays still and shoots zombies."""
    futurologist = True

    def next_step(self, things, t=None):

        if S.played == 0:
            # lead a change in strategy
            S.tick += 1
            if S.next_strategy is not None:
                S.strategy = getattr(self, 'build_' + S.next_strategy)(things)
                S.strategy_name = S.next_strategy
                S.next_strategy = None

        S.played += 1
        if S.played == len([x for x in things.values() if isinstance(x, Player)]):
            S.played = 0

        result = S.strategy.get_next_move(self, things)

        self.status = S.strategy_name + "|" + str(S.tick) + "|" + str(result)
        return result

    def build_first_strategy(self, things):
        return RushStrategy(things, (7, 12), "dos", 50)

    def build_dos(self, things):
        return RushStrategy(things, (2, 8), "tres", 50)

    def build_tres(self, things):
        return RushStrategy(things, (27, 13), "cuatro", 50)

    def build_cuatro(self, things):
        return RushStrategy(things, (27, 1), "first_strategy", 50)


class FuturologistEvacuation(Player):
    """A player that stays still and shoots zombies."""
    futurologist = True

    def next_step(self, things, t=None):

        if S.played == 0:
            # lead a change in strategy
            S.tick += 1
            if S.next_strategy is not None:
                S.strategy = getattr(self, 'build_' + S.next_strategy)(things)
                S.strategy_name = S.next_strategy
                S.next_strategy = None

        S.played += 1
        if S.played == len([x for x in things.values() if isinstance(x, Player)]):
            S.played = 0

        result = S.strategy.get_next_move(self, things)

        self.status = S.strategy_name + "|" + str(S.tick) + "|" + str(result)
        return result

    def build_first_strategy(self, things):
        return RushStrategy(things, [(4, 5), (9, 12), (6, 15), (15, 11), (22, 7), (44, 2), (43, 19), (56, 9), (89, 7),
                                     (85, 13)], "dos", 50)


class RushStrategy(object):
    def __init__(self, things, goal, next_strategy, wait=20, timeout=250):
        self.goal = goal
        self.next_strategy = next_strategy
        self.map = GoalDistanceMap(goal, things)
        self.wait = wait
        self.start_t = None
        self.timeout = timeout

    def get_next_move(self, player, things):
        if self.start_t is None:
            self.start_t = S.tick

        result = None
        g = self.map
        current = g[player.position]
        winner = None

        if player.life < 70 and random.random() < 0.3:
            result = ('heal', player)
        #elif player.life < 40:
        #        result = ('heal', player)
        else:
            #print "evaluating", self, self.position
            moves = utils.possible_moves(player, things)
            random.shuffle(moves)
            for pos in moves:
                #print pos, g[pos], current
                if g[pos] < current:
                    winner = pos

            if winner:
                result = ('move', winner)
            else:
                target = closest(player, [x for x in things.values() if isinstance(x, Zombie)])
                if target is not None:
                    if utils.distance(target, player) <= player.weapon.max_range:
                        result = ('attack', target)

        # if result is None:
        #     if random.random() < 0.25:
        #         moves = utils.possible_moves(self, things)
        #         if moves:
        #             pos = random.choice(moves)
        #             result = ('move', pos)

        if result is None:
            result = ('heal', player)

        if result[0] in ('attack', 'move'):
            S.last_action = S.tick

        if S.tick - S.last_action > self.wait:
            S.next_strategy = self.next_strategy
            S.last_action = S.tick

        if S.tick - self.start_t > self.timeout:
            S.next_strategy = self.next_strategy
            S.last_action = S.tick

        return result


class RushRushStrategy(object):
    def __init__(self, goal, wait=10, timeout=100):
        self.goal = goal
        self.map = None
        self.wait = wait
        self.timeout = timeout
        self.start_tick = None

    def get_next_move(self, player, things):
        if self.start_tick is None:
            self.start_tick = S.tick

        if self.map is None:
            self.map = GoalDistanceMap(self.goal, things)

        result = None
        done = False
        g = self.map
        current = g[player.position]
        winner = None

        if player.life < 70 and random.random() < 0.3:
            result = ('heal', player)
        elif player.life < 50:
            result = ('heal', player)
        else:
            #print "evaluating", self, self.position
            moves = utils.possible_moves(player, things)
            random.shuffle(moves)
            for pos in moves:
                #print pos, g[pos], current
                if g[pos] < current:
                    winner = pos

            if winner:
                result = ('move', winner)
            else:
                target = closest(player, [x for x in things.values() if isinstance(x, Zombie)])
                if target is not None:
                    if utils.distance(target, player) <= player.weapon.max_range:
                        result = ('attack', target)


                        # target = closest(player, [x for x in things.values() if isinstance(x, Zombie)])
                        # if target is not None:
                        #     if utils.distance(target, player) <= 1.5:
                        #         result = ('attack', target)


                        # if result is not None:
                        #     moves = utils.possible_moves(player, things)
                        #     random.shuffle(moves)
                        #     for pos in moves:
                        #             #print pos, g[pos], current
                        #             if g[pos] < current:
                        #                 winner = pos

                        #     if winner:
                        #         result = ('move', winner)
                        #     else:
                        #         target = closest(player, [x for x in things.values() if isinstance(x, Zombie)])
                        #         if target is not None:
                        #             if utils.distance(target, player) <= player.weapon.max_range:
                        #                 result = ('attack', target)

        # if result is None:
        #     if random.random() < 0.25:
        #         moves = utils.possible_moves(self, things)
        #         if moves:
        #             pos = random.choice(moves)
        #             result = ('move', pos)

        if result is None:
            result = ('heal', player)

        if result[0] in ('attack', 'move'):
            S.last_action = S.tick

        if S.tick - S.last_action > self.wait:
            done = True
            S.last_action = S.tick

        if S.tick - self.start_tick > self.timeout:
            done = True
        return result, done, "Rush(%s)" % (self.goal,)


class DestroyThingStrategy(object):
    def __init__(self, location):
        self.location = location

    def get_next_move(self, player, things):
        result = None

        if player.life < 70 and random.random() < 0.3:
            result = ('heal', player)
        else:
            target = closest(player, [x for x in things.values() if isinstance(x, Zombie)])
            if target is not None:
                if utils.distance(target, player) <= player.weapon.max_range:
                    result = ('attack', target)

        done = False
        if not self.location in things:
            done = True
        else:
            if result is None:
                result = ('attack', things[self.location])

        return result, done, "Destroy(%s)" % (self.location,)


class WaitStrategy(object):
    def __init__(self):
        pass

    def get_next_move(self, player, things):
        result = None

        if player.life < 70 and random.random() < 0.3:
            result = ('heal', player)
        else:
            target = closest(player, [x for x in things.values() if isinstance(x, Zombie)])
            if target is not None:
                if utils.distance(target, player) <= player.weapon.max_range:
                    result = ('attack', target)

        if result is None:
            result = ('heal', player)

        return result, False, "Waiting"


class ComposerStrategy(object):
    def __init__(self, *strategies):
        self.strategies = strategies
        self.ptr = 0
        self.done = set()
        self.going_for_win = None
        self.win_strategy = None

    def get_next_move(self, player, things):
        if self.going_for_win is not None:
            if self.win_strategy is None:
                self.win_strategy = RushRushStrategy(self.going_for_win)
            s = self.win_strategy
        else:
            s = self.strategies[(self.ptr % len(self.strategies))]
        action, done, status = s.get_next_move(player, things)

        if done:
            done = False
            self.done.add(player.name)

        if len(self.done) >= len([x for x in things.values() if isinstance(x, Player)]):
            self.ptr += 1
            self.done = set()
            self.going_for_win = self.is_winnable(things)
            if self.ptr >= len(self.strategies):
                done = True

        #print self.done, player, s
        #raw_input()
        return action, done, ("{%s/%s}" % (self.ptr, len(self.strategies))) + status

    def is_winnable(self, things):
        def adjacent(one, two):
            ps = utils.adjacent_positions(one)
            if two.position in ps:
                return True
            return False

        players = [x for x in things.values() if isinstance(x, Player)]
        for player in players:
            close = [player]
            for other in players:
                if player == other:
                    continue
                for test in close:
                    if adjacent(test, other):
                        close.append(other)
            if len(close) > 2:
                return close[0].position


class PlayerSpecificStrategies(object):
    def __init__(self, default_strategy, wait_strategy, selector, **kwargs):
        self.default = default_strategy
        self.wait = wait_strategy
        self.selector = selector
        self.specific = kwargs
        self.players = {}
        self.done = set()

    def get_next_move(self, player, things):
        if player.name in self.players:
            strat = self.players[player.name]
        else:
            pk = self.selector.key_for(player)
            strat = self.specific.get(pk, None)
            if strat is None:
                self.done.add(player.name)
                strat = self.default
            self.players[player.name] = strat
        move, done, status = strat.get_next_move(player, things)

        live_names = set([x.name for x in things.values() if isinstance(x, Player)])
        if done:
            done = False
            self.done.add(player.name)
            self.players[player.name] = self.wait
        if live_names.issubset(self.done):
            done = True
        return move, done, "[%s/%s] " % (len(self.done), len(live_names)) + status


class MapReader(object):
    def __init__(self, filename):
        self.lines = [l for l in codecs.open(filename, "r", "utf-8")]

    def __getitem__(self, item):
        x, y = item
        try:
            return self.lines[y][x]
        except IndexError:
            return None

    def key_for(self, player):
        return self[player.position]


class FuturologistEvacuation(Player):
    """A player that stays still and shoots zombies."""
    futurologist = True

    def next_step(self, things, t=None):
        result = None

        if S.played == 0:
            # lead a change in strategy
            S.tick += 1
            if S.next_strategy is not None:
                S.strategy = getattr(self, 'build_' + S.next_strategy)(things)
                S.strategy_name = S.next_strategy
                S.next_strategy = None

        S.played += 1
        if S.played == len([x for x in things.values() if isinstance(x, Player)]):
            S.played = 0

        result, done, status = S.strategy.get_next_move(self, things)
        pos_code = MapReader('players/evacuation.map')[self.position]
        if not 'a' <= pos_code <= 'z':
            pos_code = ""
        self.status = "p" + str(self.position) + pos_code \
                      + "|" + str(status) + "|" + str(result)
        return result

    def build_first_strategy(self, things):
        return self._strategy

    _strategy = ComposerStrategy(
        RushRushStrategy([(4, 5), (9, 12), (9, 14), (15, 11), (22, 7),
                          (44, 2), (43, 19), (62, 9), (89, 7), (85, 13)], 5),

        # H to I
        # PlayerSpecificStrategies(
        #     WaitStrategy(), WaitStrategy(),
        #     MapReader('players/evacuation.map'),
        #     h=RushRushStrategy((62, 11))
        #     ),
        # PlayerSpecificStrategies(
        #     WaitStrategy(), WaitStrategy(),
        #     MapReader('players/evacuation.map'),
        #     h=RushRushStrategy((56, 9))
        #     ),
        # PlayerSpecificStrategies(
        #     WaitStrategy(), WaitStrategy(),
        #     MapReader('players/evacuation.map'),
        #     h=DestroyThingStrategy((56, 8)),
        #     ),
        # PlayerSpecificStrategies(
        #     WaitStrategy(), WaitStrategy(),
        #     MapReader('players/evacuation.map'),
        #     h=RushRushStrategy((56, 8))
        #     ),
        # PlayerSpecificStrategies(
        #     WaitStrategy(), WaitStrategy(),
        #     MapReader('players/evacuation.map'),
        #     h=RushRushStrategy((44, 2))
        #     ),

        # I to J
        PlayerSpecificStrategies(
            WaitStrategy(), WaitStrategy(),
            MapReader('players/evacuation.map'),
            i=DestroyThingStrategy((43, 2)),
        ),
        PlayerSpecificStrategies(
            WaitStrategy(), WaitStrategy(),
            MapReader('players/evacuation.map'),
            i=DestroyThingStrategy((42, 2)),
        ),
        PlayerSpecificStrategies(
            WaitStrategy(), WaitStrategy(),
            MapReader('players/evacuation.map'),
            i=RushRushStrategy((22, 7))
        ),

        # J to A
        PlayerSpecificStrategies(
            WaitStrategy(), WaitStrategy(),
            MapReader('players/evacuation.map'),
            j=DestroyThingStrategy((21, 7)),
        ),
        PlayerSpecificStrategies(
            WaitStrategy(), WaitStrategy(),
            MapReader('players/evacuation.map'),
            j=RushRushStrategy((4, 5))
        ),


        # A to B
        PlayerSpecificStrategies(
            WaitStrategy(), WaitStrategy(),
            MapReader('players/evacuation.map'),
            a=RushRushStrategy((9, 12))
        ),
        PlayerSpecificStrategies(
            WaitStrategy(), WaitStrategy(),
            MapReader('players/evacuation.map'),
            b=DestroyThingStrategy((9, 13)),
        ),
        PlayerSpecificStrategies(
            WaitStrategy(), WaitStrategy(),
            MapReader('players/evacuation.map'),
            b=RushRushStrategy((9, 13))
        ),
        PlayerSpecificStrategies(
            WaitStrategy(), WaitStrategy(),
            MapReader('players/evacuation.map'),
            b=RushRushStrategy((15, 11))
        ),
        PlayerSpecificStrategies(
            WaitStrategy(), WaitStrategy(),
            MapReader('players/evacuation.map'),
            c=RushRushStrategy((44, 20))
        ),
        PlayerSpecificStrategies(
            WaitStrategy(), WaitStrategy(),
            MapReader('players/evacuation.map'),
            e=RushRushStrategy((92, 10))
        ),
        PlayerSpecificStrategies(
            WaitStrategy(), WaitStrategy(),
            MapReader('players/evacuation.map'),
            e=DestroyThingStrategy((92, 11))
        ),
        PlayerSpecificStrategies(
            WaitStrategy(), WaitStrategy(),
            MapReader('players/evacuation.map'),
            e=RushRushStrategy((93, 13)),
        ),
        PlayerSpecificStrategies(
            WaitStrategy(), WaitStrategy(),
            MapReader('players/evacuation.map'),
            d=RushRushStrategy((88, 15)),
        ),
        PlayerSpecificStrategies(
            WaitStrategy(), WaitStrategy(),
            MapReader('players/evacuation.map'),
            f=RushRushStrategy((78, 15)),
        ),
        PlayerSpecificStrategies(
            WaitStrategy(), WaitStrategy(),
            MapReader('players/evacuation.map'),
            h=RushRushStrategy((82, 15)),
        ),
        # PlayerSpecificStrategies(
        #     WaitStrategy(), WaitStrategy(),
        #     MapReader('players/evacuation.map'),
        #     d=DestroyThingStrategy((79, 12))
        #     ),
        PlayerSpecificStrategies(
            WaitStrategy(), WaitStrategy(),
            MapReader('players/evacuation.map'),
            e=RushRushStrategy((56, 11)),
            d=RushRushStrategy((56, 11))
        ),
        RushRushStrategy((44, 20)),
    )


def create(rules, objectives=None):
    random.shuffle(names)
    name = names.pop()
    S.number_players += 1
    if rules == "safehouse":
        return FuturologistSafehouse(name, 'yellow', weapon=Rifle())
    if rules == "extermination":
        return FuturologistExtermination(name, 'yellow', weapon=Rifle())
    if rules == "evacuation":
        return FuturologistEvacuation(name, 'yellow', weapon=Shotgun())


