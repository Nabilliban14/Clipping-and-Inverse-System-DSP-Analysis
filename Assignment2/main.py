import as2
import simlib
import sys

def main():
    if len(sys.argv) != 2:
        print('supply file with orders as argument')
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()

    if not lines:
        print('nothing in {}'.format(sys.argv[1]))
        sys.exit(1)

    sim = simlib.Simulation()
    as2.setup_simulation(sim)
    chef_count = sim.get_available_chef_count()
    ingredients = sim.ingredients.copy()

    for line in lines:
        parts = line.strip().split(',')
        try:
            sim.schedule_event(int(parts[0]), as2.handle_new_order, parts[1:])
        except:
            print('invalid line: {}'.format(line))

    sim.simulate()

    print('-----------------')
    print('- Kitchen had {} chef(s) and the following ingredient counts:'.format(chef_count))
    for ingredient, info in ingredients.items():
        print('  - {}: {}'.format(ingredient.title(), info.count))

    total_orders = len(lines)
    accepted_orders = sim.accepted_orders
    rejected_orders = sim.rejected_orders
    print('- Accepted orders: {} ({:0.2f}%)'.format(accepted_orders, (accepted_orders / total_orders) * 100))
    print('- Rejected orders: {} ({:0.2f}%)'.format(rejected_orders, (rejected_orders / total_orders) * 100))
    print('- Total time: {} minute(s)'.format(sim.time))

if __name__ == '__main__':
    main()
