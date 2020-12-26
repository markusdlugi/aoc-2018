from collections import deque, defaultdict
from timeit import default_timer as timer


def marble_game(player_count, marble_count):
    scores = defaultdict(int)
    marbles = deque()
    marbles.appendleft(0)
    for marble in range(1, marble_count + 1):
        if marble % 23 != 0:
            # Move 2 marbles to the right
            marbles.append(marbles.popleft())
            marbles.append(marbles.popleft())
            # Insert new marble
            marbles.appendleft(marble)
        else:
            # Score new marble for current player
            player = marble % player_count
            scores[player] += marble
            # Move 7 marbles to the left
            for i in range(7):
                marbles.appendleft(marbles.pop())
            # Remove marble and score it
            scores[player] += marbles.popleft()

    return max(scores.values())


words = open("input/09.txt").read().split()
player_count = int(words[0])
marble_count = int(words[6])

start = timer()
print(marble_game(player_count, marble_count))
print(marble_game(player_count, marble_count * 100))
end = timer()

print(f'Took {end - start} seconds.')
