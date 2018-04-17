from simlib import *

def print_time(time, msg):
    print(time, msg, sep=': ')

# TODO: add new functions below this line
def start_preparing_ingredient(time, sim, ingredient):
    if sim.get_available_chef_count() > 0:
        sim.assign_chef()
        sim.schedule_event(time + sim.get_prep_time(ingredient), finish_preparing_ingredient, ingredient)
        print_time(time, 'Starting to prep ' + ingredient)
    else:
        sim.schedule_event(time + 1, start_preparing_ingredient, ingredient)
    

# TODO: add new functions above this line
def finish_preparing_ingredient(time, sim, ingredient):
    sim.dismiss_chef()
    print_time(time, 'Done prepping ' + ingredient)

def handle_new_order(time, sim, recipe):
    enough_ingredients = True
    # TODO: check if there are enough ingredients//done
    for ingredient in recipe:
        if sim.get_count(ingredient) <= 0:
            enough_ingredients = False

    if enough_ingredients:
        sim.increment_accepted_order_count()
        print_time(time, 'Accepting order')
        # TODO: schedule events for each ingredient
        for ingredient in recipe:
            sim.use_ingredient(ingredient)
            sim.schedule_event(time, start_preparing_ingredient, ingredient)

    else:
        # TODO: handle case where there are not enough ingredients (and delete following line)//done
        sim.increment_rejected_order_count()
        print_time(time, 'Rejecting order')

def setup_simulation(sim):
    sim.set_available_chef_count(2)
    sim.add_ingredient('burger', 10, 8)
    sim.add_ingredient('lettuce', 8, 2)
    sim.add_ingredient('tomato', 15, 2)
    sim.add_ingredient('bun', 20, 5)
