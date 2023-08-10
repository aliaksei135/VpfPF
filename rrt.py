import numpy as np
import matplotlib.pyplot as plt

class Node:
    def __init__(self, state):
        self.state = state
        self.cost = 0
        self.parent = None

class RRTStar:
    def __init__(self, start, goal, costmap, max_iter, step_size, goal_sample_rate, min_cost_to_goal):
        self.start = Node(start)
        self.goal = Node(goal)
        self.costmap = costmap
        self.bounds = costmap.shape
        self.max_iter = max_iter
        self.step_size = step_size
        self.goal_sample_rate = goal_sample_rate
        self.min_cost_to_goal = min_cost_to_goal

        self.nodes = [self.start]
        self.path_found = False

    def generate_random_node(self):
        if np.random.rand() < self.goal_sample_rate:
            return Node(self.goal.state)
        else:
            rand_state = np.random.uniform(self.bounds[0], self.bounds[1])
            return Node(rand_state)

    def find_nearest_node(self, node):
        distances = [np.linalg.norm(node.state - n.state) for n in self.nodes]
        min_index = np.argmin(distances)
        return self.nodes[min_index]

    def get_cost(self, state):
        x, y = state.astype(int)
        return self.costmap[y, x]

    def extend(self, from_node, to_node):
        new_state = from_node.state + self.step_size * (to_node.state - from_node.state) / np.linalg.norm(to_node.state - from_node.state)
        new_node = Node(new_state)
        new_node.cost = from_node.cost + self.get_cost(new_state)
        return new_node

    def rewire(self, new_node):
        for node in self.nodes:
            if node == new_node or node.parent is None:
                continue
            if np.linalg.norm(node.state - new_node.state) > self.step_size:
                continue
            cost = new_node.cost + np.linalg.norm(node.state - new_node.state)
            if cost < node.cost:
                node.parent = new_node
                node.cost = cost

    def find_final_path(self):
        if self.path_found:
            path = []
            node = self.goal
            while node is not None:
                path.insert(0, node.state)
                node = node.parent
            return path
        return None

    def plan(self):
        for _ in range(self.max_iter):
            rand_node = self.generate_random_node()
            nearest_node = self.find_nearest_node(rand_node)
            new_node = self.extend(nearest_node, rand_node)
            if new_node:
                self.nodes.append(new_node)
                self.rewire(new_node)
                if np.linalg.norm(new_node.state - self.goal.state) < self.min_cost_to_goal:
                    self.goal.parent = new_node
                    self.goal.cost = new_node.cost + np.linalg.norm(self.goal.state - new_node.state)
                    self.path_found = True
        return self.find_final_path()

# Example usage:
if __name__ == "__main__":
    costmap = np.array([
        [1, 2, 2, 1],
        [1, 3, 2, 2],
        [1, 1, 1, 2],
        [1, 2, 2, 1]
    ])  # Example costmap with varying costs

    start = np.array([0, 0])
    goal = np.array([3, 3])
    bounds = [np.array([0, 0]), np.array([3, 3])]
    max_iter = 1000
    step_size = 1.0
    goal_sample_rate = 0.1
    min_cost_to_goal = 2.0

    rrt_star = RRTStar(start, goal, costmap, bounds, max_iter, step_size, goal_sample_rate, min_cost_to_goal)
    path = rrt_star.plan()

    if path is not None:
        print("Path found!")
        print(path)
        plt.plot([node[0] for node in path], [node[1] for node in path], '-r')
    else:
        print("Path not found!")


