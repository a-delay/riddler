"""
github/a-delay
8/24/2018: https://fivethirtyeight.com/features/how-many-hoops-will-kids-jump-through-to-play-rock-paper-scissors/
simulate the hoops game and find average time to completion

there's a little bit of a problem with how the rules are described:
if the left player starts on position 0 and the right player starts on position 1,
then if the right player wins, a new player shows up at position 0 instantaneously
and the cycle continues for as long as the right player continues to win. thus, i
have made the assumption that in such a scenario, if the right player wins in rps,
they advance a step and win the entire game.
"""
import random

memo = {}

# here, we assume lower and upper to be integers
# and func such that for all integer x, y in [lower, upper]
# where x < y, func(x) < func(y)
# we want to return some value r such that |func(r)-goal| < error
def binary_search(lower, upper, func, goal, error):
    def difference(attempt):
        return abs(func(attempt) - goal)
    def close_enough(attempt):
        return difference(attempt) < error
    def result(attempt):
        return attempt, func(attempt)
    
    # some base cases, only need to test once
    if close_enough(lower):
        return result(lower)
    if close_enough(upper):
        return result(upper)
    
    while True:
        # base cases to test multiple times
        if upper - lower <= 1:
            return result(upper) if difference(upper) < difference(lower) else result(lower)
        if func(upper) < goal:
            return None
        if func(lower) > goal:
            return None
        
        mid = (upper + lower) // 2
        if close_enough(mid):
            return result(mid)
        elif func(mid) > goal:
            upper = mid
        else:
            lower = mid

def simulate_many(hoops, n=10000):
    if (hoops, n) in memo:
        return memo[(hoops, n)]
    total = 0
    for _ in range(n):
        total += simulate(hoops)
    avg_time = total/n
    memo[(hoops, n)] = avg_time
    return avg_time

def simulate(hoops):
    left = 0
    right = hoops-1
    time = 0

    while left != hoops-1 or right != 0:
        new_left = (left + right) // 2
        new_right = new_left if (left + right) % 2 == 0 else new_left + 1
        time += new_left - left

        games, winner = simulate_rps()
        time += games
        if winner: #if left won
            # a check for the last step of the game
            if left == hoops-2:
                time += 1
                break
            left = new_left
            right = hoops-1
        else: #if right won
            # a check for the last step of the game
            if right == 1:
                time += 1
                break
            left = 0
            right = new_right
    return time

# return number of games and True if left won
def simulate_rps():
    # 1/3 time tie, 1/3 time left wins, 1/3 time right wins
    n = random.randint(0,2)
    if n == 0:
        return 1, True
    if n == 1:
        return 1, False
    if n == 2:
        time, winner = simulate_rps()
        return time + 1, winner

# for eight hoops
print(simulate_many(8, 100000))

# for a half hour game
print(binary_search(1, 50, simulate_many, 30*60, 1))
print(simulate_many(41, 100000))