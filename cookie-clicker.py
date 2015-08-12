"""
Cookie Clicker Simulator. Must be run inside Codeskulptor environment: http://www.codeskulptor.org/
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._cookies_held = 0.0
        self._current_time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return 'Total cookies produced: ' + str(self._total_cookies) + '\n' + 'Total cookies held: ' + str(self._cookies_held) + '\n' + 'Current time: ' + str(self._current_time) + '\n' + 'Cookies per second: ' + str(self._cps)
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._cookies_held
    
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
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies <= self._cookies_held:
            return 0.0
        else:
            cookies_remaining = cookies - self._cookies_held
            return math.ceil(cookies_remaining / self._cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time > 0:
            self._current_time += time
            self._cookies_held += (self._cps * time)
            self._total_cookies += (self._cps * time)
        else:
            return
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._cookies_held >= cost:
            self._cookies_held -= cost
            self._cps += additional_cps
            self._history.append((self._current_time, item_name, cost, self._total_cookies))
        else:
            return
            
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """

    new_build_info = build_info.clone()
    new_clicker_state = ClickerState()
    loop_break = False
    time_left = 0.0
    next_item = ''
    time_until = 0.0
    while loop_break != True:
        time_left = duration - new_clicker_state.get_time()
        if new_clicker_state.get_time() == duration:
            loop_break = True
        next_item = strategy(new_clicker_state.get_cookies(), new_clicker_state.get_cps(), time_left, new_build_info)
        if next_item != None:
            time_until = new_clicker_state.time_until(new_build_info.get_cost(next_item))
            if time_until > time_left:
                loop_break = True
            else:
                new_clicker_state.wait(time_until)
                new_clicker_state.buy_item(next_item, new_build_info.get_cost(next_item), new_build_info.get_cps(next_item))
                new_build_info.update_item(next_item)
        else:
            loop_break = True
    new_clicker_state.wait(time_left)
    time_left = 0.0
    while next_item != None:
        next_item = strategy(new_clicker_state.get_cookies(), new_clicker_state.get_cps(), time_left, new_build_info)
        time_until = new_clicker_state.time_until(new_build_info.get_cost(next_item))
        if time_until == 0.0:
            new_clicker_state.buy_item(next_item, new_build_info.get_cost(next_item), new_build_info.get_cps(next_item))
            new_build_info.update_item(next_item)
        else:
            next_item = None
    return new_clicker_state


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Strategy that always chooses the cheapest item
    buildable in the time remaining
    """
    cheapest_item = None
    item_list = build_info.build_items()
    cookies_remaining = cookies + (cps * time_left)
    for item in item_list:
        if cheapest_item == None:
            cheapest_item = item
        elif build_info.get_cost(item) < build_info.get_cost(cheapest_item):
            cheapest_item = item
    if build_info.get_cost(cheapest_item) <= cookies_remaining:
        return cheapest_item
    else:
        return None 

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Strategy that always chooses the most expensive item
    buildable in the time remaining
    """
    best_item = None
    item_list = build_info.build_items()
    cookies_remaining = cookies + (cps * time_left)
    for item in item_list:
        if best_item == None:
            best_item = item
        elif build_info.get_cost(item) > build_info.get_cost(best_item):
            best_item = item
    if build_info.get_cost(best_item) <= cookies_remaining:
        return best_item
    else:
        return None 

def strategy_best(cookies, cps, time_left, build_info):
    """
    Strategy that always compares the cost and potential cps
    benefit to choose the best item buildable 
    in the time remaining
    """
    best_item = None
    item_list = build_info.build_items()
    cookies_remaining = cookies + (cps * time_left)
    for item in item_list:
        if best_item == None:
            best_item = item
        else:
            old_cost_benefit = build_info.get_cost(best_item) / build_info.get_cps(best_item)
            new_cost_benefit = build_info.get_cost(item) / build_info.get_cps(item)
            if new_cost_benefit < old_cost_benefit:
                best_item = item
    if build_info.get_cost(best_item) <= cookies_remaining:
        return best_item
    else:
        return None
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    #history = state.get_history()
    #history = [(item[0], item[3]) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
#run()
    

