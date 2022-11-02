import random

try:
    while True:
        print(random.randrange(20, 50, 3))
except KeyboardInterrupt:
    print('You cancelled the operation')