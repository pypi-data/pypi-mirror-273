def tic_tac_toe():
    code = """
def print_board(board):
    print(f'{board[0]} | {board[1]} | {board[2]}')
    print('---------')
    print(f'{board[3]} | {board[4]} | {board[5]}')
    print('---------')
    print(f'{board[6]} | {board[7]} | {board[8]}')
def check_win(board):
    win_condition=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for condition in win_condition:
        if board[condition[0]]==board[condition[1]]==board[condition[2]]!=" ":
            return True
    return False
def tic_tac_toe():
    board=[" "]*9
    current_player="X"
    while " " in board:
        print_board(board)
        move=int(input(f'player {current_player}, enter your move (1-9)'))-1
        if board[move]==" ":
            board[move]=current_player
            if check_win(board):
                print_board(board)
                print(f'Player {current_player} wins!')
                break
            current_player="O" if current_player=="X" else "X"
    else:
        print_board(board)
        print("Its a draw")
tic_tac_toe() 
            """
    return code

def Monte_Carlo():
    code = """
import gym
import numpy as np

def random_policy(state):
    return np.random.choice(env.action_space.n)

def monte_carlo_prediction(env, policy, num_episodes, discount_factor):
    returns_sum = {}
    returns_count = {}
    V = {}

    for _ in range(num_episodes):
        episode = []
        state = env.reset()
        for t in range(100):
            action = policy(state)
            next_state, reward, done, _ = env.step(action)
            episode.append((state, action, reward))
            if done:
                break
            state = next_state

        for t, (state, _, _) in enumerate(episode):
            G = sum([x[2] * (discount_factor ** i) for i,x in enumerate(episode[t:])])
            if state in returns_sum:
                returns_sum[state] += G
                returns_count[state] += 1
            else:
                returns_sum[state] = G
                returns_count[state] = 1
            V[state] = returns_sum[state] / returns_count[state]

    return V

# Example usage:
env = gym.make('FrozenLake-v1')
V = monte_carlo_prediction(env, random_policy, num_episodes=10000, discount_factor=0.9)

# Print the estimated value function
print("Estimated Value Function:")
for state, value in V.items():
    print(f"State: {state}, Value: {value}")
           """
    return code 
    
def Off_Policy_Importance_sampling_montecarlo():
    code = """
import numpy as np
import gym

def generate_episode(env, behavior_policy):
    episode = []
    state = env.reset()
    while True:
        action = behavior_policy[state]
        next_state, reward, done, _ = env.step(action)
        episode.append((state, action, reward))
        if done:
            break
        state = next_state
    return episode

def off_policy_mc_control_importance_sampling(env, num_episodes, behavior_policy, target_policy, discount_factor=1.0):
    nA = env.action_space.n
    Q = np.zeros((env.observation_space.n, nA))
    C = np.zeros((env.observation_space.n, nA))

    for _ in range(num_episodes):
        episode = generate_episode(env, behavior_policy)
        G = 0.0
        W = 1.0

        for t in range(len(episode) - 1, -1, -1):
            state, action, reward = episode[t]
            G = discount_factor * G + reward
            C[state][action] += W
            Q[state][action] += (W / C[state][action]) * (G - Q[state][action])

            if action != target_policy[state]:
                break

            W /= behavior_policy[state]

    return Q

# Define behavior policy (e.g., random policy)
def random_policy(env):
    return np.random.randint(0, env.action_space.n, env.observation_space.n)

# Define target policy (e.g., greedy policy)
def greedy_policy(Q):
    return np.argmax(Q, axis=1)

# Example usage:
env = gym.make('FrozenLake-v1')
behavior_policy = random_policy(env)
target_policy = behavior_policy.copy()  # Initialize target policy with behavior policy
Q = off_policy_mc_control_importance_sampling(env, num_episodes=10000, behavior_policy=behavior_policy, target_policy=target_policy)
target_policy = greedy_policy(Q)

print("Target Policy:")
print(target_policy)
           """
    return code

def SARSA():
    code = """
import numpy as np
import gym

def epsilon_greedy_policy(Q, state, epsilon):
    if np.random.rand() < epsilon:
        return np.random.randint(Q.shape[1])  # Choose a random action
    else:
        return np.argmax(Q[state])  # Choose the action with the highest Q-value

def sarsa(env, num_episodes, alpha, gamma, epsilon):
    Q = np.zeros((env.observation_space.n, env.action_space.n))

    for _ in range(num_episodes):
        state = env.reset()
        action = epsilon_greedy_policy(Q, state, epsilon)

        while True:
            next_state, reward, done, _ = env.step(action)
            next_action = epsilon_greedy_policy(Q, next_state, epsilon)

            # Update Q-values using SARSA update rule
            Q[state][action] += alpha * (reward + gamma * Q[next_state][next_action] - Q[state][action])

            if done:
                break

            state = next_state
            action = next_action

    return Q

# Example usage:
env = gym.make('FrozenLake-v1')
num_episodes = 10000
alpha = 0.1
gamma = 0.99
epsilon = 0.1

Q = sarsa(env, num_episodes, alpha, gamma, epsilon)

# Extract the optimal policy from Q-values
optimal_policy = np.argmax(Q, axis=1)
print("Optimal Policy (0: Left, 1: Down, 2: Right, 3: Up):")
print(optimal_policy.reshape((4, 4)))
           """
    return code

def off_policy_Qlearning():
    code = """
import numpy as np
import gym

def epsilon_greedy_policy(Q, state, epsilon):
    if np.random.rand() < epsilon:
        return np.random.randint(Q.shape[1])  # Choose a random action
    else:
        return np.argmax(Q[state])  # Choose the action with the highest Q-value

def q_learning(env, num_episodes, alpha, gamma, epsilon):
    Q = np.zeros((env.observation_space.n, env.action_space.n))

    for _ in range(num_episodes):
        state = env.reset()

        while True:
            action = epsilon_greedy_policy(Q, state, epsilon)
            next_state, reward, done, _ = env.step(action)

            # Update Q-value using Q-learning update rule
            best_next_action = np.argmax(Q[next_state])
            Q[state][action] += alpha * (reward + gamma * Q[next_state][best_next_action] - Q[state][action])

            if done:
                break

            state = next_state

    return Q

# Example usage:
env = gym.make('FrozenLake-v1')
num_episodes = 10000
alpha = 0.1
gamma = 0.99
epsilon = 0.1

Q = q_learning(env, num_episodes, alpha, gamma, epsilon)

# Extract the optimal policy from Q-values
optimal_policy = np.argmax(Q, axis=1)
print("Optimal Policy (0: Left, 1: Down, 2: Right, 3: Up):")
print(optimal_policy.reshape((4, 4)))

           """
    return code

def Qlearning_linear_approx():
    code = """
import gym
import numpy as np

# Define environment
env = gym.make('FrozenLake-v1')

# Hyperparameters
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
num_episodes = 1000  # Number of training episodes

# State and action dimensions
state_size = env.observation_space.n
action_size = env.action_space.n

# Weights for linear function approximation (initialize randomly)
weights = np.random.rand(state_size, action_size)


def epsilon_greedy(state, epsilon):
  if np.random.rand() < epsilon:
    # Explore: choose random action
    return env.action_space.sample()
  else:
    # Exploit: choose action with highest Q-value
    q_values = weights[state]
    return np.argmax(q_values)


def update_weights(state, action, reward, next_state, done):
  if done:
    target = reward
  else:
    # Bellman equation with linear function approximation
    next_q_values = weights[next_state]
    target = reward + gamma * np.max(next_q_values)

  # TD error
  td_error = target - np.dot(weights[state], np.eye(action_size)[action])

  # Update weights
  weights[state, action] += alpha * td_error * state

for episode in range(num_episodes):
  # Reset environment
  state = env.reset()

  # Set initial epsilon (decaying over episodes)
  epsilon = 0.5 * (1 - episode / num_episodes)

  while True:
    # Choose action based on epsilon-greedy policy
    action = epsilon_greedy(state, epsilon)

    # Take action, observe reward and next state
    next_state, reward, done, _ = env.step(action)

    # Update weights
    update_weights(state, action, reward, next_state, done)

    # Update state for next iteration
    state = next_state

    if done:
      break

# Print optimal policy (argmax over Q-values for each state)
optimal_policy = np.argmax(weights, axis=1)
print("Optimal Policy:")
print(optimal_policy.reshape((4,4)))

# You can use the optimal_policy array to play the environment optimally
# (e.g., by selecting the action corresponding to the optimal_policy[state])

env.close()
           """
    return code

def grid_world_three():
    code = """
class GridGame:
    def __init__(self):
        self.grid_size = 3
        self.player_position = (0, 0)  # Initial player position at the top-left corner
        self.goal_position = (2, 2)    # Goal position at the bottom-right corner
        self.obstacle_positions = [(1, 1)]  # Obstacle positions, you can add more if needed

    def print_grid(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if (row, col) == self.player_position:
                    print('P', end=' ')
                elif (row, col) == self.goal_position:
                    print('G', end=' ')
                elif (row, col) in self.obstacle_positions:
                    print('X', end=' ')
                else:
                    print('-', end=' ')
            print()

    def is_valid_move(self, new_position):
        return 0 <= new_position[0] < self.grid_size and 0 <= new_position[1] < self.grid_size \
               and new_position not in self.obstacle_positions

    def make_move(self, direction):
        row, col = self.player_position

        if direction == 'up':
            new_position = (row - 1, col)
        elif direction == 'down':
            new_position = (row + 1, col)
        elif direction == 'left':
            new_position = (row, col - 1)
        elif direction == 'right':
            new_position = (row, col + 1)
        else:
            print("Invalid move. Use 'up', 'down', 'left', or 'right'.")
            return

        if self.is_valid_move(new_position):
            self.player_position = new_position
            print("Move successful!")
        else:
            print("Invalid move. Try a different direction.")

    def play_game(self):
        print("Welcome to the 3x3 Grid Game!")
        print("Reach the goal 'G' while avoiding obstacles 'X'.")
        self.print_grid()

        while self.player_position != self.goal_position:
            direction = input("Enter your move ('up', 'down', 'left', 'right'): ")
            self.make_move(direction)
            self.print_grid()

        print("Congratulations! You reached the goal!")

if __name__ == "__main__":
    game = GridGame()
    game.play_game()
           """
    return code

def Armed_Bandit():
    code = """
import random
import pandas as pd

num_arms = 5

num_rounds = 1000

true_means = [0.1, 0.2, 0.3, 0.4, 0.5]

means = {i: 0 for i in range(num_arms)}
counts = {i: 0 for i in range(num_arms)}

def e_greedy(ε):
    if random.random() < ε:
        return random.randint(0, num_arms - 1)
    else:
        return max(means, key=means.get)
for _ in range(num_rounds):
    arm = e_greedy(0.1)
    reward = random.gauss(true_means[arm], 1)
    counts[arm] += 1
    means[arm] = (means[arm] * (counts[arm] - 1) + reward) / counts[arm]
results = pd.DataFrame({
    'Arm': list(range(num_arms)),
    'True Mean': true_means,
    'Estimated Mean': list(means.values()),
    'Count': list(counts.values())
})
print(results.to_string(index=False))
           """
    return code

def Grid_world():
    code = """
# EXPERIMENT 10
# Simulate Grid game using suitable reinforcement approach and analyze the results of the model
import numpy as np

class GridWorld:
    def __init__(self, width, height, start, goal, obstacles):
        self.width = width
        self.height = height
        self.start = start
        self.goal = goal
        self.obstacles = obstacles
        self.state = start

    def reset(self):
        self.state = self.start

    def step(self, action):
        x, y = self.state
        if action == 0:  # Up
            y = max(0, y - 1)
        elif action == 1:  # Down
            y = min(self.height - 1, y + 1)
        elif action == 2:  # Left
            x = max(0, x - 1)
        elif action == 3:  # Right
            x = min(self.width - 1, x + 1)

        if (x, y) in self.obstacles:
            reward = -10
            done = True
            next_state = self.state
        elif (x, y) == self.goal:
            reward = 10
            done = True
            next_state = self.goal
        else:
            reward = -1
            done = False
            next_state = (x, y)

        self.state = next_state
        return next_state, reward, done

class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.99):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.q_table = np.zeros((state_size, action_size))

    def choose_action(self, state):
        if np.random.rand() < self.exploration_rate:
            return np.random.choice(self.action_size)
        return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state, best_next_action]
        td_error = td_target - self.q_table[state, action]
        self.q_table[state, action] += self.learning_rate * td_error

        if self.exploration_rate > 0.01:
            self.exploration_rate *= self.exploration_decay

def train_agent(agent, env, episodes):
    rewards = []
    for episode in range(episodes):
        state = env.start
        done = False
        total_reward = 0
        while not done:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.update_q_table(state, action, reward, next_state)
            state = next_state
            total_reward += reward
        rewards.append(total_reward)
        if (episode + 1) % 100 == 0:
            print(f"Episode {episode + 1}/{episodes}, Total Reward: {total_reward}")
    return rewards

# Define the grid world
width = 5
height = 5
start = (0, 0)
goal = (4, 4)
obstacles = [(1, 1), (2, 2), (3, 3)]

# Initialize the environment and agent
env = GridWorld(width, height, start, goal, obstacles)
agent = QLearningAgent(width * height, 4)  # 4 possible actions (up, down, left, right)

# Train the agent
rewards = train_agent(agent, env, episodes=1000)

# Analyze the results
print("Average reward per episode:", np.mean(rewards))
print("Maximum reward per episode:", np.max(rewards))
print("Minimum reward per episode:", np.min(rewards))
           """
    return code

def MonteCarlo_pie_estimation():
    code = """
import random

def estimate_pi(num_samples):
    inside_circle = 0

    for _ in range(num_samples):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        distance = x**2 + y**2

        if distance <= 1:
            inside_circle += 1

    return (inside_circle / num_samples) * 4

if __name__ == "__main__":
    num_samples = 1000000
    pi_estimate = estimate_pi(num_samples)
    print("Estimated value of π using Monte Carlo Prediction:", pi_estimate)
           """
    return code

def MDP_policy_improvements():
    code = """
import numpy as np

# Define the grid world environment
# 'S' represents the start state
# 'G' represents the goal state
# 'H' represents a hole state with negative reward
# 'F' represents a free state with no reward
grid_world = np.array([
    ['F', 'F', 'F', 'G'],
    ['F', 'H', 'F', 'H'],
    ['F', 'F', 'F', 'H'],
    ['S', 'H', 'F', 'F']
])

# Define rewards for each state
rewards = {
    'S': 0,  # Start state
    'G': 10,  # Goal state
    'H': -10,  # Hole state
    'F': -1  # Free state
}

# Define policy (initially random)
policy = {
    (0, 0): 'RIGHT', (0, 1): 'RIGHT', (0, 2): 'DOWN', (0, 3): None,
    (1, 0): 'DOWN', (1, 1): None, (1, 2): 'DOWN', (1, 3): None,
    (2, 0): 'RIGHT', (2, 1): 'RIGHT', (2, 2): 'RIGHT', (2, 3): None,
    (3, 0): None, (3, 1): 'DOWN', (3, 2): 'DOWN', (3, 3): 'LEFT'
}

# Define transition probabilities
transition_probs = {
    'UP': (-1, 0),
    'DOWN': (1, 0),
    'LEFT': (0, -1),
    'RIGHT': (0, 1)
}

# Perform Policy Improvement
def policy_improvement(grid_world, policy, rewards, transition_probs):
    new_policy = policy.copy()
    for i in range(grid_world.shape[0]):
        for j in range(grid_world.shape[1]):
            state = (i, j)
            if grid_world[i, j] != 'G' and grid_world[i, j] != 'H':
                best_action = None
                best_value = float('-inf')
                for action in transition_probs.keys():
                    next_state = tuple(np.array(state) + np.array(transition_probs[action]))
                    if 0 <= next_state[0] < grid_world.shape[0] and 0 <= next_state[1] < grid_world.shape[1]:
                        value = rewards[grid_world[next_state]]  # Reward of next state
                        if grid_world[next_state] != 'G':
                            value += rewards[grid_world[next_state]]  # Transition reward
                        if value > best_value:
                            best_value = value
                            best_action = action
                new_policy[state] = best_action
    return new_policy
# Example usage:
new_policy = policy_improvement(grid_world, policy, rewards, transition_probs)
print("Improved Policy:")
print(new_policy)
           """
    return code

def MDP_policy_improvements():
    code = """
import numpy as np

# Define the grid world environment
# 'S' represents the start state
# 'G' represents the goal state
# 'H' represents a hole state with negative reward
# 'F' represents a free state with no reward
grid_world = np.array([
    ['F', 'F', 'F', 'G'],
    ['F', 'H', 'F', 'H'],
    ['F', 'F', 'F', 'H'],
    ['S', 'H', 'F', 'F']
])

# Define rewards for each state
rewards = {
    'S': 0,  # Start state
    'G': 10,  # Goal state
    'H': -10,  # Hole state
    'F': -1  # Free state
}

# Define policy (initially random)
policy = {
    (0, 0): 'RIGHT', (0, 1): 'RIGHT', (0, 2): 'DOWN', (0, 3): None,
    (1, 0): 'DOWN', (1, 1): None, (1, 2): 'DOWN', (1, 3): None,
    (2, 0): 'RIGHT', (2, 1): 'RIGHT', (2, 2): 'RIGHT', (2, 3): None,
    (3, 0): None, (3, 1): 'DOWN', (3, 2): 'DOWN', (3, 3): 'LEFT'
}

# Define transition probabilities
transition_probs = {
    'UP': (-1, 0),
    'DOWN': (1, 0),
    'LEFT': (0, -1),
    'RIGHT': (0, 1)
}

# Perform Value Iteration
def value_iteration(grid_world, policy, rewards, transition_probs, gamma=0.9, theta=0.0001):
    V = np.zeros(grid_world.shape)
    while True:
        delta = 0
        for i in range(grid_world.shape[0]):
            for j in range(grid_world.shape[1]):
                state = (i, j)
                if grid_world[i, j] != 'G' and grid_world[i, j] != 'H':
                    v = V[i, j]
                    action = policy[state]
                    if action is not None:  # Check if action is not None
                        next_state = tuple(np.array(state) + np.array(transition_probs[action]))
                        if 0 <= next_state[0] < grid_world.shape[0] and 0 <= next_state[1] < grid_world.shape[1]:
                            reward = rewards[grid_world[next_state]]
                            V[i, j] = reward + gamma * V[next_state[0], next_state[1]]
                            delta = max(delta, np.abs(v - V[i, j]))
        if delta < theta:
            break
    return V
optimal_values = value_iteration(grid_world, policy, rewards, transition_probs)
print("\nOptimal Values:")
print(optimal_values)
           """
    return code

def Randomarray():
    code = """
import numpy as np

# Set the seed for reproducibility
np.random.seed(42)

# Generate a 5x5 array with random values between 0.66 and 1
random_array = np.random.uniform(0.66, 1, size=(5, 5))

print("Random 5x5 array:")
print(random_array)

values=[1, 0.81, 0.73, 0.66,1, 0.81, 0.73, 0.66,1, 0.81, 0.73, 0.66,1, 0.81, 0.73, 0.66,1, 0.81, 0.73, 0.66,1, 0.81, 0.66,1, 0.81]
np.random.shuffle(values)
array=np.zeros((5,5))
for value in values:
    row, col = np.random.randint(0, 5), np.random.randint(0, 5)
    while array[row, col] != 0:
        row, col = np.random.randint(0, 5), np.random.randint(0, 5)
    array[row, col] = value
print(array)
           """
    return code

def policy_evaluation_iteration():
    code = """
# Function to perform policy evaluation
def policy_evaluation(states, actions, transition_probs, rewards, policy, gamma, theta):
    V = {s: 0 for s in states}  # Initialize value function arbitrarily
    while True:
        delta = 0
        for s in states:
            v = V[s]
            new_v = 0
            for a in actions:
                if a in transition_probs[s]:
                    for next_state in transition_probs[s][a]:
                        prob = transition_probs[s][a][next_state]
                        reward = rewards[s][a][next_state]
                        new_v += policy[s][a] * prob * (reward + gamma * V[next_state])
            V[s] = new_v
            delta = max(delta, abs(v - V[s]))
        if delta < theta:
            break
    return V

# Function to perform policy iteration
def policy_iteration(states, actions, transition_probs, rewards, gamma, theta):
    policy = {s: {a: 1 / len(actions) for a in actions} for s in states}  # Initialize policy arbitrarily
    while True:
        V = policy_evaluation(states, actions, transition_probs, rewards, policy, gamma, theta)
        policy_stable = True
        for s in states:
            old_action = max(policy[s], key=policy[s].get)
            new_action_values = {}
            for a in actions:
                action_value = 0
                if a in transition_probs[s]:
                    for next_state in transition_probs[s][a]:
                        prob = transition_probs[s][a][next_state]
                        reward = rewards[s][a][next_state]
                        action_value += prob * (reward + gamma * V[next_state])
                    new_action_values[a] = action_value
            if new_action_values:
                new_action = max(new_action_values, key=new_action_values.get)
                if old_action != new_action:
                    policy_stable = False
                policy[s] = {a: (1 if a == new_action else 0) for a in actions}
        if policy_stable:
            break
    return policy
    
# Example usage
states = [0, 1, 2, 3]
actions = ['left', 'right', 'up', 'down']
transition_probs = {
    0: {'right': {1: 1}},
    1: {'left': {0: 1}, 'right': {2: 1}},
    2: {'left': {1: 1}, 'right': {3: 1}},
    3: {'left': {2: 1}}
}
rewards = {
    0: {'right': {1: 1}},
    1: {'left': {0: 1}, 'right': {2: 1}},
    2: {'left': {1: 1}, 'right': {3: 1}},
    3: {'left': {2: 1}}
}
gamma = 0.9
theta = 0.0001

optimal_policy = policy_iteration(states, actions, transition_probs, rewards, gamma, theta)
print("Optimal Policy:")
for s in states:
    print(f"State {s}: {max(optimal_policy[s], key=optimal_policy[s].get)}")```
           """
    return code