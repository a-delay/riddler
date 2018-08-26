"""
github/a-delay
8/24/2018: https://fivethirtyeight.com/features/how-many-hoops-will-kids-jump-through-to-play-rock-paper-scissors/
simulate the hoops game and find average time to completion
"""
import random

def simulate(hoops):
    left = 0
    right = hoops-1
    time = 0

    while left != hoops-1 or right != 0:
        #print("left: " + str(left))
        #print("right: " + str(right))
        new_left = (left + right) // 2
        new_right = new_left if (left + right) % 2 == 0 else new_left + 1
        time += new_left - left

        games, winner = simulate_rps()
        #print("games: " + str(games))
        #print("winner is left: " + str(winner))
        time += games
        if winner: #if left won
            if left == hoops-2:
                time += 1
                break
            left = new_left
            right = hoops-1
        else: #if right won
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

total_time = 0
n = 10000
for i in range(n):
    total_time += simulate(8)
print(total_time/n)