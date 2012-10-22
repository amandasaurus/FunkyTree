from collections import defaultdict
from functools import wraps
from pprint import pprint
from copy import copy

class State(object):

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)

    def _tests(self):
        return [getattr(self, x) for x in dir(self) if x.startswith('test')]

def state_change_to(*states):

    def decorator(func):
        func.is_state_change = True
        func.states = states

        return func
    return decorator

def main(initial_state):
    # run tests
    assert issubclass(initial_state, State)

    state_changes = defaultdict(lambda :defaultdict(set))

    # calculate state changes
    processed_states = set()
    unprocessed_states = set([initial_state])

    while len(unprocessed_states) > 0:
        state = unprocessed_states.pop()


        state_change_funcs = [getattr(state, x) for x in dir(state) if getattr(getattr(state, x), 'is_state_change', False)]
        for state_change_func in state_change_funcs:
            destination_states = [getattr(__import__(state.__module__), x) for x in state_change_func.states]
            #import pdb ; pdb.set_trace()
            for destination_state in destination_states:
                if destination_state not in processed_states:
                    unprocessed_states.add(destination_state)
                # TODO support >1 state
                state_changes[state][state_change_func.__name__].add(destination_state)

                    
    # calculate all walks of the tree
    # ea. walk: [Stateclass, 'func_name', newstateclass, 'func_name']
    walks = set([(initial_state,)])

    unprocessed_walks = set([(initial_state,)])

    while len(unprocessed_walks) > 0:
        walk = unprocessed_walks.pop()

        end_state = walk[-1]

        for state_change_func in state_changes[end_state]:
            for new_state in state_changes[end_state][state_change_func]:
                if new_state in walk:
                    # no cycles
                    continue

                new_walk = list(copy(walk))
                new_walk.append(state_change_func)
                new_walk.append(new_state)
                new_walk = tuple(new_walk)

                unprocessed_walks.add(new_walk)
                walks.add(new_walk)

    _run_walks(walks)


def _run_walks(walks):

    # Run the tests
    for walk in sorted(walks, key=lambda x: len(x)):
        assert len(walk) % 2 == 1

        walk_so_far = []

        position_in_walk = 0
        state = walk[position_in_walk]()


        while True:
                
            # how far have we gone?
            walk_so_far.append(state.__class__.__name__)

            # run tests on this state
            for test in state._tests():
                try:
                    test()
                except Exception as ex:
                    # error
                    print "Exception when going on walk {walk}".format(walk=" -> ".join(walk_so_far))
                    print ex

            # Everything OK, so let's take the next step
            position_in_walk += 1
            if position_in_walk >= len(walk):
                break
            func_name = walk[position_in_walk]
            state = getattr(state, func_name)()
            position_in_walk += 1
            walk_so_far.append(func_name)


