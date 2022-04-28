# http://www2.fiit.stuba.sk/~kapustik/z2d.html
import copy
import time

"""
Y 1.
|
|   
|
0  0 0 0 0 0 0
1  0 0 0 0 0 0 
2  0 0 0 0 0 0
3  0 0 0 0 0 0 
4  0 0 0 0 0 0 
5  0 0 0 0 0 0
   0 1 2 3 4 5  ------X 2.


"""


class Vehicle:
    x = 0
    y = 0
    w = 0
    rotation = None
    color = None
    number = 0

    def __init__(self, x, y, w, rotation, color, number):
        self.x = x
        self.y = y
        self.w = w
        self.rotation = rotation
        self.color = color
        self.number = number

    def right(self, x):
        self.x += x

    def left(self, x):
        self.x -= x

    def up(self, y):
        self.y -= y

    def down(self, y):
        self.y += y


class Node:
    layer = 0
    parent = None  # prior node
    children = []

    cars: [Vehicle] = []
    state = []
    log = None

    def __init__(self, parent, cars, layer):
        self.parent = parent
        self.cars = cars
        self.layer = layer

    def set(self):
        self.state = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0]]
        for car in self.cars:
            self.state[car.y - 1][car.x - 1] = car.number
            if car.rotation == "h":
                self.state[car.y - 1][car.x] = car.number
            elif car.rotation == "v":
                self.state[car.y][car.x - 1] = car.number
            if car.w == 3:
                if car.rotation == "h":
                    self.state[car.y - 1][car.x + 1] = car.number
                elif car.rotation == "v":
                    self.state[car.y + 1][car.x - 1] = car.number


def bfs(parent):
    edge = [parent]
    finish = False
    done_state = None
    while not finish:
        current = edge[0]
        child = None
        for car in current.cars:
            if car.rotation == "h":

                if car.x < (6 - car.w + 1) and current.state[car.y - 1][car.x - 1 + car.w] == 0:
                    max_move = 1
                    while car.x - 1 + max_move + car.w < 6 and current.state[car.y - 1][
                        car.x - 1 + max_move + car.w] == 0:
                        max_move += 1
                    for i in range(1, max_move + 1):
                        child = Node(current, copy.deepcopy(current.cars), current.layer + 1)
                        child.cars[(car.number - 1)].right(i)
                        child.log = ["right", i, child.cars[(car.number - 1)].color]
                        child.set()
                        if child.state not in states:
                            edge.append(child)
                            states.append(child.state)
                    if child.cars[(car.number - 1)].x == 5 and child.cars[(car.number - 1)].number == 1:
                        finish = True
                        done_state = child
                        break

                if car.x > 1 and current.state[car.y - 1][car.x - 1 - 1] == 0:
                    max_move = 1
                    while car.x - 1 - max_move > 0 and current.state[car.y - 1][car.x - 1 - max_move - 1] == 0:
                        max_move += 1
                    for i in range(1, max_move + 1):
                        child = Node(current, copy.deepcopy(current.cars), current.layer + 1)

                        child.cars[(car.number - 1)].left(i)
                        child.set()
                        child.log = ["left", i, child.cars[(car.number - 1)].color]
                        if child.state not in states:
                            edge.append(child)
                            states.append(child.state)

            if car.rotation == "v":

                if car.y < (6 - car.w + 1) and current.state[car.y - 1 + car.w][car.x - 1] == 0:
                    max_move = 1
                    while car.y - 1 + car.w + max_move < 6 and current.state[car.y - 1 + car.w + max_move][
                        car.x - 1] == 0:
                        max_move += 1
                    for i in range(1, max_move + 1):
                        child = Node(current, copy.deepcopy(current.cars), current.layer + 1)
                        child.cars[(car.number - 1)].down(i)
                        child.set()
                        child.log = ["down", i, child.cars[(car.number - 1)].color]
                        if child.state not in states:
                            edge.append(child)
                            states.append(child.state)

                if car.y > 1 and current.state[car.y - 1 - 1][car.x - 1] == 0:
                    max_move = 1
                    while car.y - 1 - max_move > 0 and current.state[car.y - 1 - max_move - 1][car.x - 1] == 0:
                        max_move += 1
                    for i in range(1, max_move + 1):
                        child = Node(current, copy.deepcopy(current.cars), current.layer + 1)
                        child.cars[(car.number - 1)].up(i)
                        child.set()
                        child.log = ["up", i, child.cars[(car.number - 1)].color]
                        if child.state not in states:
                            edge.append(child)
                            states.append(child.state)

        edge.pop(0)

    return done_state


def dfs(parent):
    edge = [parent]
    finish = False
    done_state = None
    while not finish:
        child = None
        children = []
        current = edge[0]
        for car in current.cars:
            if car.rotation == "h":

                if car.x < (6 - car.w + 1) and current.state[car.y - 1][car.x - 1 + car.w] == 0:
                    max_move = 1
                    while car.x - 1 + max_move + car.w < 6 and current.state[car.y - 1][
                        car.x - 1 + max_move + car.w] == 0:
                        max_move += 1
                    for i in range(1, max_move + 1):
                        child = Node(current, copy.deepcopy(current.cars), current.layer + 1)
                        child.cars[(car.number - 1)].right(i)
                        child.log = ["right", i, child.cars[(car.number - 1)].color]
                        child.set()
                        if child.state not in states:
                            children.append(child)
                            states.append(child.state)

                    if child.cars[(car.number - 1)].x == 5 and child.cars[(car.number - 1)].number == 1:
                        finish = True
                        done_state = child
                        break

                if car.x > 1 and current.state[car.y - 1][car.x - 1 - 1] == 0:
                    max_move = 1
                    while car.x - 1 - max_move > 0 and current.state[car.y - 1][car.x - 1 - max_move - 1] == 0:
                        max_move += 1
                    for i in range(1, max_move + 1):
                        child = Node(current, copy.deepcopy(current.cars), current.layer + 1)
                        child.cars[(car.number - 1)].left(i)
                        child.set()
                        child.log = ["left", i, child.cars[(car.number - 1)].color]
                        if child.state not in states:
                            children.append(child)
                            states.append(child.state)

            if car.rotation == "v":

                if car.y < (6 - car.w + 1) and current.state[car.y - 1 + car.w][car.x - 1] == 0:
                    max_move = 1
                    while car.y - 1 + car.w + max_move < 6 and current.state[car.y - 1 + car.w + max_move][
                        car.x - 1] == 0:
                        max_move += 1
                    for i in range(1, max_move + 1):
                        child = Node(current, copy.deepcopy(current.cars), current.layer + 1)
                        child.cars[(car.number - 1)].down(i)
                        child.set()
                        child.log = ["down", i, child.cars[(car.number - 1)].color]
                        if child.state not in states:
                            children.append(child)
                            states.append(child.state)

                if car.y > 1 and current.state[car.y - 1 - 1][car.x - 1] == 0:
                    max_move = 1
                    while car.y - 1 - max_move > 0 and current.state[car.y - 1 - max_move - 1][car.x - 1] == 0:
                        max_move += 1
                    for i in range(1, max_move + 1):
                        child = Node(current, copy.deepcopy(current.cars), current.layer + 1)
                        child.cars[(car.number - 1)].up(i)
                        child.set()
                        child.log = ["up", i, child.cars[(car.number - 1)].color]
                        if child.state not in states:
                            children.append(child)
                            states.append(child.state)
        edge.pop(0)
        edge = children + edge

    return done_state


if __name__ == '__main__':
    global states
    states = []

    red = Vehicle(2, 3, 2, "h", "red", 1)
    blue = Vehicle(2, 1, 2, "h", "blue", 2)
    green = Vehicle(5, 5, 2, "h", "green", 3)
    orange = Vehicle(4, 3, 2, "v", "orange", 4)
    yellow = Vehicle(6, 2, 2, "v", "yellow", 5)
    pink = Vehicle(4, 1, 2, "v", "pink", 6)
    grey = Vehicle(2, 5, 2, "v", "grey", 7)
    lblue = Vehicle(3, 4, 2, "v", "lblue", 8)
    black = Vehicle(1,4 ,3 , "v" , "black", 9)
    purple = Vehicle(5,1 ,3 ,"v" , "purple", 10)
    brown = Vehicle(3,6 ,2 ,"h" , "brown", 11)
    white = Vehicle(5, 4, 2,"h" , "white", 12)
    start = Node(None, [red,blue, green, orange, yellow,pink ,grey ,lblue ,black,purple, brown, white ], 0)
    start.set()
    for s in start.state:
        print(s)
    print("\n")

    s = time.time()
    done = bfs(start)
    e = time.time()

    steps = []
    while done.parent is not None:
        steps = [done.log] + steps
        done = done.parent
    else:
        print(steps)
        print("BFS: number of steps: "+str(len(steps)) + "    Number of states: "+str(len(states)))
    print("BFS time:", e - s, "sec")
    states = []
    s = time.time()
    done = dfs(start)
    e = time.time()
    print("\nDFS time:", e - s, "sec")
    steps = []
    while done.parent is not None:
        steps = [done.log] + steps
        done = done.parent

    else:
        print("DFS: number of steps: "+str(len(steps)) + "    Number of states: "+str(len(states)))
        print(steps)

