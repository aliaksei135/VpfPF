import heapq

from config import MAP_RESOLUTION, CRUISE_SPEED, DEBUG
from cost_functions import total_marginal_costs, marginal_vehicle_costs, fixed_vehicle_costs


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = (float('inf'), float('inf'))
        self.f = float('inf')
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


def distance(node1, node2):
    # Euclidean distance
    dx = node1.x - node2.x
    dy = node1.y - node2.y
    return ((dx ** 2) + (dy ** 2)) ** 0.5


def reconstruct_path(current, start, grid):
    path = []
    cost_real = fixed_vehicle_costs() + current.g[0]
    cost_img = current.g[1]
    risk = 0
    cumdist = 0
    while current is not start:
        risk += grid[current.y][current.x]
        cumdist += distance(current, current.parent)
        path.append((current.x, current.y))
        current = current.parent
    print("Risk: {}".format(risk))
    return path[::-1], cost_real, cost_img, cumdist * MAP_RESOLUTION, (cumdist * MAP_RESOLUTION) / CRUISE_SPEED


def heuristic(node1, node2):
    time_between = (distance(node1, node2) * MAP_RESOLUTION) / CRUISE_SPEED
    return marginal_vehicle_costs(time_between) / 10
    # return distance(node1, node2)


def _calc_cost(child: Node, best: Node, grid):
    g1_cost = total_marginal_costs(grid, best, child)
    g1_real, g1_img = best.g[0] + g1_cost[0], best.g[1] + g1_cost[1]
    return g1_real, g1_img, best


def run_a_star(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    closed_set = set()

    start_node = Node(start[0], start[1])
    goal_node = Node(goal[0], goal[1])

    start_node.g = (0, 0)
    start_node.f = 0
    start_node.parent = start_node

    heapq.heappush(open_set, start_node)

    while open_set:
        current = heapq.heappop(open_set)

        if current == goal_node:
            # if DEBUG:
            #     from viz import display_node_costs
            #     display_node_costs(closed_set, grid)
            return reconstruct_path(current, start_node, grid)

        closed_set.add(current)

        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                x, y = current.x + dx, current.y + dy
                if 0 <= x < cols and 0 <= y < rows:
                    neighbor = Node(x, y)
                    neighbors.append(neighbor)

        for neighbor in neighbors:
            if neighbor in closed_set:
                continue

            cost_real, cost_img, parent = _calc_cost(neighbor, current, grid)
            neighbor.g = (cost_real, cost_img)
            neighbor.parent = parent
            neighbor.f = cost_real + cost_img + heuristic(neighbor, goal_node)

            # if DEBUG:
            #     # Check heuristic consistency
            #     h_s = heuristic(parent, goal_node)
            #     h_s_prime = heuristic(neighbor, goal_node)
            #     c_s_prime = total_marginal_costs(grid, parent, neighbor)
            #     if h_s > h_s_prime + c_s_prime:
            #         print("Heuristic inconsistency detected!")
            #         print("h(s) = {}, h(s') = {}, c(s, s') = {}".format(h_s, h_s_prime, c_s_prime))
            #
            #     # Check heuristic admissability
            #     c_gs_prime = total_marginal_costs(grid, neighbor, goal_node)
            #     if h_s_prime >= c_gs_prime:
            #         print("Heuristic admissability violated!")
            #         print("h(s') = {}, c(s', g) = {}".format(h_s_prime, c_gs_prime))

            # Calculate the cost from the current node to the neighbor
            tentative_cost = total_marginal_costs(grid, current, neighbor)
            tentative_g = (current.g[0] + tentative_cost[0], current.g[1] + tentative_cost[1])

            if sum(tentative_g) < sum(neighbor.g):
                neighbor.g = tentative_g
                neighbor.f = sum(neighbor.g) + heuristic(neighbor, goal_node)
                neighbor.parent = current

            if neighbor not in open_set:
                heapq.heappush(open_set, neighbor)

    return None  # No path found
