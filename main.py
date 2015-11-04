#!/usr/bin/env python3

import enum
import itertools
import multiprocessing
import random
import time

import rules

NUM_WIRES = 8
MIN_CUTS = 6
MAX_CUTS = 7

THREADS = 4
PROGRESS_INTERVAL = 10 # seconds

NonSolution = enum.Enum("NonSolution", "too_easy not_possible")

def generate_games(colors):
    # Start with a cartesian product
    games = itertools.product(colors, repeat=NUM_WIRES)

    # Filter out games that don't use all colors
    games = [x for x in games if set(colors) == set(x)]

    # Randomize the order
    random.shuffle(games)

    return (games, len(games))

def solve(game):
    for num_cuts in range(MAX_CUTS + 1):
        for cuts in itertools.permutations(range(NUM_WIRES), num_cuts):
            if is_solution(game, cuts):
                if num_cuts >= MIN_CUTS:
                    return (game, cuts)
                else:
                    return (game, NonSolution.too_easy)
    else:
        return (game, NonSolution.not_possible)

def is_solution(game, cuts):
    wires = list(game)

    for cut in cuts:
        if rules.victory(wires):
            # No extra cuts after victory allowed
            return False

        if all((not x(wires, cut) for x in rules.actions())):
            # There must be an action rule for the cut
            return False

        wires[cut] = None

    return rules.victory(wires)

def solve_interruptable(game):
    try:
        return solve(game)
    except KeyboardInterrupt:
        pass

def print_game(game, solution):
    print()
    print_wires(game)
    print("Solution: {}".format(" ".join(map(str, solution))))

def print_wires(wires):
    for i, wire in enumerate(wires):
        print("{}: {}".format(i, wire.name))

def rate(games, start_time):
    value = games / (time.time() - start_time)
    return "{:.2f} games per second".format(value)

def print_stats(games, accepted, too_easy):
    impossible = games - accepted - too_easy

    print_stat("accepted", accepted, games)
    print_stat("too easy", too_easy, games)
    print_stat("impossible", impossible, games)

def print_stat(label, number, games):
    print("- {} games {} ({:.2f} %)"
          .format(number, label, 100 * number / games))

def list_games(pool):
    print("Generating game configurations...")
    games, num_games = generate_games(rules.wire_colors())

    print("Searching for acceptable games from {} configurations..."
          .format(num_games))

    accepted = 0
    too_easy = 0
    start_time = time.time()
    progress_time = time.time()

    solutions = pool.imap_unordered(solve_interruptable, games)
    for i, (game, solution) in enumerate(solutions):
        if solution in NonSolution:
            if solution == NonSolution.too_easy:
                too_easy += 1
        else:
            accepted += 1
            print_game(game, solution)

        if time.time() - progress_time > PROGRESS_INTERVAL:
            progress_time = time.time()

            print()
            print("Progress: {:.1f} % at {}"
                  .format(100 * i / num_games, rate(i, start_time)))
            print_stats(i, accepted, too_easy)

    print()
    print("Checked {} games at {}"
          .format(num_games, rate(num_games, start_time)))
    print_stats(num_games, accepted, too_easy)

if __name__ == "__main__":
    with multiprocessing.Pool(THREADS) as pool:
        try:
            list_games(pool)
        except KeyboardInterrupt:
            print()
            print("Aborting...")
            pool.terminate()
