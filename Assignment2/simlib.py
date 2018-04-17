import heapq

class Event:
    def __init__(self, time, func, args, kwargs):
        self.time = time
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __lt__(self, other):
        return self.time < other.time

class IngredientInfo:
    def __init__(self, count, prep_time):
        self.count = count
        self.prep_time = prep_time

class Simulation:
    def __init__(self):
        self.events = list()
        self.time = 0
        self.init_chefs = 0
        self.chefs = 0
        self.ingredients = {}
        self.accepted_orders = 0
        self.rejected_orders = 0

    def simulate(self):
        while len(self.events):
            next_event = heapq.heappop(self.events)
            self.time = next_event.time
            next_event.func(self.time, self, *next_event.args, **next_event.kwargs)

    def add_ingredient(self, ingredient, count, prep_time):
        self.ingredients[ingredient] = IngredientInfo(count, prep_time)

    def set_available_chef_count(self, count):
        self.init_chefs = count
        self.chefs = count

    def schedule_event(self, time, func, *args, **kwargs):
        heapq.heappush(self.events, Event(time, func, args, kwargs))

    def get_count(self, ingredient):
        return self.ingredients[ingredient].count

    def use_ingredient(self, ingredient):
        if self.ingredients[ingredient].count > 0:
            self.ingredients[ingredient].count -= 1
        else:
            raise Exception('Your {} count has gone negative'.format(ingredient))

    def assign_chef(self):
        if self.chefs > 0:
            self.chefs -= 1
        else:
            raise Exception('Available chefs has gone negative')

    def dismiss_chef(self):
        if self.chefs < self.init_chefs:
            self.chefs += 1
        else:
            raise Exception('Available chefs has exceeded the number of chefs you started with')

    def get_available_chef_count(self):
        return self.chefs

    def get_prep_time(self, ingredient):
        return self.ingredients[ingredient].prep_time

    def increment_accepted_order_count(self):
        self.accepted_orders += 1

    def increment_rejected_order_count(self):
        self.rejected_orders += 1
