# this project has to be run in codeskulptor.org
"""
Cookie Clicker Simulator
"""

# import simpleplot
import poc_clicker_provided as provided

from math import ceil

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

# Constants
SIM_TIME = 10000000000.0


class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._cookies = 0.0
        self._current_cookies = 0.0
        self._time = 0.0
        self._cps = 1.0

        # (time, item, cost of item, total cookies)
        self._history = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        return "Total number of cookies: " + str(self._cookies) + '\n' + \
               "Current number of cookies: " + str(self.get_cookies()) + '\n' + \
               "Game time: " + str(self.get_time()) + '\n' + \
               "Cookies per second: " + str(self.get_cps())

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return self._current_cookies

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self._history)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies <= self.get_cookies():
            return 0.0
        return ceil((cookies - self.get_cookies()) / self.get_cps())

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._time += time
            self._current_cookies += time * self._cps
            self._cookies += time * self._cps

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:

            self._history.append((self.get_time(),
                                  item_name,
                                  cost,
                                  self._cookies))

            self._current_cookies -= cost
            self._cps += additional_cps


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState

    object corresponding to the final state of the game.
    """

    info = build_info.clone()
    game = ClickerState()
    game_time = game.get_time()
    time_left = duration - game_time
    item_to_buy = strategy(game.get_cookies(), game.get_cps(), game.get_history(), time_left, info)
    while duration > 0:
        if not (item_to_buy):
            break
        time_to_purchase = game.time_until(info.get_cost(item_to_buy))
        if time_to_purchase <= time_left:
            game.wait(time_to_purchase)
            game.buy_item(item_to_buy, info.get_cost(item_to_buy), info.get_cps(item_to_buy))
            info.update_item(item_to_buy)

            game_time = game.get_time()
            time_left = duration - game_time
            item_to_buy = strategy(game.get_cookies(), game.get_cps(), game.get_history(), time_left, info)
        else:
            break
    game.wait(time_left)
    return game


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"


def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None


def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    cookies += time_left * cps
    costs = []
    for idx, item in enumerate(build_info.build_items()):
        if build_info.get_cost(item) <= cookies:
            costs.append((idx, build_info.get_cost(item)))
    costs.sort(key=lambda item: item[1])
    if costs:
        return build_info.build_items()[costs[0][0]]
    return None


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    cookies += time_left * cps
    costs = []
    for idx, item in enumerate(build_info.build_items()):
        if build_info.get_cost(item) <= cookies:
            costs.append((idx, build_info.get_cost(item)))
    costs.sort(key=lambda item: item[1])
    if costs:
        return build_info.build_items()[costs[-1][0]]
    return None

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """

    item_list = build_info.build_items()
    cookies_to_use = cookies + cps * time_left
    buyable_items = filter(lambda item: build_info.get_cost(item) <= cookies_to_use, item_list)

    if len(buyable_items) > 0:
        item_costs = [build_info.get_cost(item) for item in buyable_items]
        item_cps = [build_info.get_cps(item) for item in buyable_items]
        max_ratio = max([(item_cps[idx] * time_left) / item_costs[idx] for idx in range(len(buyable_items))])
        item_to_buy = filter(lambda item: (build_info.get_cps(item) * time_left) / build_info.get_cost(item) == max_ratio, buyable_items)

        return item_to_buy[0]

    return None

    # Another implementation (Not very good)
    
    # all_cookies = cookies + time_left * cps
    # costs = []
    # for idx, item in enumerate(build_info.build_items()):
    #     if build_info.get_cost(item) <= all_cookies:
    #         costs.append((idx, build_info.get_cost(item)))
    # costs.sort(key=lambda item: item[1])

    # possible_purchases = []
    # for item in costs:
    #     possible_purchases.append(build_info.build_items()[item[0]])

    # for item in possible_purchases:
    #     num = 0
    #     for entry in history:
    #         if item in entry:
    #             num += 1
    #     if item != "Time Machine" or item != 'Cursor':
    #         if num < 100:
    #             return item
    #     else:
    #         if item == "Time Machine":
    #             if num < 50:
    #                 return item
    #         elif item == 'Cursor':
    #             if num < 200:
    #                 return item


def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":\n", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)


def run():
    """
    Run the simulator.
    """
    # run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)

# run()
