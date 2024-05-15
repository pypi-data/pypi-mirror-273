def tic_tac_toe():
    code = """
def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def is_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

def game_over(board):
    return is_winner(board, 'X') or is_winner(board, 'O') or is_full(board)

def get_empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']

def minimax(board, depth, maximizing_player):
    if is_winner(board, 'X'):
        return -1
    elif is_winner(board, 'O'):
        return 1
    elif is_full(board):
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for i, j in get_empty_cells(board):
            board[i][j] = 'O'
            eval = minimax(board, depth + 1, False)
            board[i][j] = ' '
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i, j in get_empty_cells(board):
            board[i][j] = 'X'
            eval = minimax(board, depth + 1, True)
            board[i][j] = ' '
            min_eval = min(min_eval, eval)
        return min_eval

def find_best_move(board):
    best_val = float('-inf')
    best_move = None

    for i, j in get_empty_cells(board):
        board[i][j] = 'O'
        move_val = minimax(board, 0, False)
        board[i][j] = ' '

        if move_val > best_val:
            best_move = (i, j)
            best_val = move_val

    return best_move

def play_tic_tac_toe():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    player_turn = True

    while not game_over(board):
        print_board(board)

        if player_turn:
            row = int(input("Enter the row (0, 1, or 2): "))
            col = int(input("Enter the column (0, 1, or 2): "))
            if board[row][col] == ' ':
                board[row][col] = 'X'
                player_turn = False
            else:
                print("Cell already occupied. Try again.")
        else:
            print("AI is making a move...")
            best_move = find_best_move(board)
            board[best_move[0]][best_move[1]] = 'O'
            player_turn = True

    print_board(board)

    if is_winner(board, 'X'):
        print("You win!")
    elif is_winner(board, 'O'):
        print("AI wins!")
    else:
        print("It's a tie!")

"""
    return code

def bandit():

    code = """
import numpy as np
import random

class Bandit:
    def __init__(self, arms, probabilities):
        self.arms = arms
        self.probabilities = probabilities

    def pull_arm(self, arm):
        return np.random.choice([0, 1], p=[1 - self.probabilities[arm], self.probabilities[arm]])

def epsilon_greedy(bandit, epsilon, num_pulls):
    num_arms = len(bandit.arms)
    total_rewards = [0] * num_arms
    num_pulls_each_arm = [0] * num_arms

    for _ in range(num_pulls):
        if random.random() < epsilon:
            arm = random.randint(0, num_arms - 1)
        else:
            arm = np.argmax([reward / (num_pulls_each_arm[i] + 1e-6) for i, reward in enumerate(total_rewards)])

        reward = bandit.pull_arm(arm)
        total_rewards[arm] += reward
        num_pulls_each_arm[arm] += 1

    return total_rewards


arms = ["Arm 1", "Arm 2", "Arm 3", "Arm 4", "Arm 5","Arm 6"]
probabilities = [0.3, 0.5, 0.8, 0.2, 0.6,0.1]
bandit = Bandit(arms, probabilities)


epsilon = 0.1
num_pulls = 1000

total_rewards = epsilon_greedy(bandit, epsilon, num_pulls)


for i, arm in enumerate(arms):
    print(f"Arm {i+1}: Total Reward = {total_rewards[i]}, Average Reward = {total_rewards[i] / num_pulls}")
"""
    return code

def policy_evaluation():

    code = """
import numpy as np

class Environment:
    def __init__(self, n_states, n_actions, transition_probabilities, rewards):
        self.n_states = n_states
        self.n_actions = n_actions
        self.transition_probabilities = transition_probabilities
        self.rewards = rewards

def policy_evaluation(env, policy, gamma=0.9, epsilon=1e-6, max_iterations=1000):
    V = np.zeros(env.n_states)
    for _ in range(max_iterations):
        prev_V = np.copy(V)
        for s in range(env.n_states):
            action = policy[s]
            V[s] = sum(env.transition_probabilities[s, action, next_state] *
                        (env.rewards[s, action, next_state] + gamma * prev_V[next_state])
                        for next_state in range(env.n_states))
        if np.max(np.abs(V - prev_V)) < epsilon:
            break
    return V

def policy_iteration(env, gamma=0.9, epsilon=1e-6, max_iterations=1000):
    policy = np.random.randint(env.n_actions, size=env.n_states)  # Initialize policy randomly
    for _ in range(max_iterations):
        old_policy = np.copy(policy)
        V = policy_evaluation(env, policy, gamma, epsilon)
        for s in range(env.n_states):
            policy[s] = np.argmax([sum(env.transition_probabilities[s, a, next_state] *
                                        (env.rewards[s, a, next_state] + gamma * V[next_state])
                                        for next_state in range(env.n_states))
                                   for a in range(env.n_actions)])
        if np.array_equal(policy, old_policy):
            break
    return policy

# Example usage:
n_states = 3
n_actions = 2
transition_probabilities = np.array([[[0.7, 0.3, 0.0], [0.1, 0.8, 0.1]],
                                     [[0.0, 0.2, 0.8], [0.4, 0.4, 0.2]],
                                     [[0.2, 0.7, 0.1], [0.6, 0.3, 0.1]]])
rewards = np.array([[[10, 0, 0], [0, 0, 0]],
                    [[0, 0, 0], [0, 0, 0]],
                    [[0, 0, 0], [0, 0, -50]]])
gamma = 0.9

env = Environment(n_states, n_actions, transition_probabilities, rewards)

policy = policy_iteration(env)
print("Optimal Policy:", policy)
"""
    return code

def MDP():

    code = """
import numpy as np

class MDP:
    def __init__(self, n_states, n_actions, transition_probabilities, rewards, gamma):
        self.n_states = n_states
        self.n_actions = n_actions
        self.transition_probabilities = transition_probabilities  # shape: (n_states, n_actions, n_states)
        self.rewards = rewards  # shape: (n_states, n_actions, n_states)
        self.gamma = gamma  # discount factor

    def value_iteration(self, epsilon=1e-6, max_iterations=1000):
        V = np.zeros(self.n_states)  # Initialize value function to zeros
        for i in range(max_iterations):
            prev_V = np.copy(V)
            for s in range(self.n_states):
                # Compute the value of each action from state s
                action_values = np.zeros(self.n_actions)
                for a in range(self.n_actions):
                    action_values[a] = np.sum(self.transition_probabilities[s, a] *
                                               (self.rewards[s, a] + self.gamma * prev_V))
                # Update the value function
                V[s] = np.max(action_values)
            # Check for convergence
            if np.max(np.abs(V - prev_V)) < epsilon:
                break
        return V

    def extract_policy(self, value_function):
        policy = np.zeros(self.n_states, dtype=int)
        for s in range(self.n_states):
            action_values = np.zeros(self.n_actions)
            for a in range(self.n_actions):
                action_values[a] = np.sum(self.transition_probabilities[s, a] *
                                          (self.rewards[s, a] + self.gamma * value_function))
            policy[s] = np.argmax(action_values)
        return policy

# Example usage:
n_states = 3
n_actions = 2
transition_probabilities = np.array([[[0.7, 0.3, 0.0], [0.1, 0.8, 0.1]],
                                     [[0.0, 0.2, 0.8], [0.4, 0.4, 0.2]],
                                     [[0.2, 0.7, 0.1], [0.6, 0.3, 0.1]]])
rewards = np.array([[[10, 0, 0], [0, 0, 0]],
                    [[0, 0, 0], [0, 0, 0]],
                    [[0, 0, 0], [0, 0, -50]]])
gamma = 0.9

mdp = MDP(n_states, n_actions, transition_probabilities, rewards, gamma)
value_function = mdp.value_iteration()
policy = mdp.extract_policy(value_function)

print("Optimal Value Function:")
print(value_function)
print("\nOptimal Policy:")
print(policy)
"""
    return code

def policy_improvement():

    code = """
import numpy as np

class MDPSolver:
    def __init__(self, n_states, n_actions, transition_probabilities, rewards, gamma=0.9):
        self.n_states = n_states
        self.n_actions = n_actions
        self.transition_probabilities = transition_probabilities
        self.rewards = rewards
        self.gamma = gamma

    def policy_improvement(self, epsilon=1e-6):
        policy = np.random.randint(0, self.n_actions, size=self.n_states)  # Randomly initialize policy
        while True:
            V = self.policy_evaluation(policy, epsilon=epsilon)  # Pass epsilon here
            policy_stable = True
            for s in range(self.n_states):
                old_action = policy[s]
                policy[s] = np.argmax([np.sum(self.transition_probabilities[s, a, :] *
                                               (self.rewards[s, a, :] + self.gamma * V)) for a in range(self.n_actions)])
                if old_action != policy[s]:
                    policy_stable = False
            if policy_stable:
                break
        return policy

    def policy_evaluation(self, policy, epsilon=1e-6, max_iterations=1000):  # Define epsilon here
        V = np.zeros(self.n_states)
        for _ in range(max_iterations):
            prev_V = np.copy(V)
            for s in range(self.n_states):
                action = policy[s]
                V[s] = np.sum(self.transition_probabilities[s, action, :] *
                              (self.rewards[s, action, :] + self.gamma * prev_V))
            if np.max(np.abs(V - prev_V)) < epsilon:
                break
        return V

    def value_iteration(self, epsilon=1e-6):
        V = np.zeros(self.n_states)  # Initialize value function to zeros
        while True:
            prev_V = np.copy(V)
            for s in range(self.n_states):
                action_values = np.zeros(self.n_actions)
                for a in range(self.n_actions):
                    action_values[a] = np.sum(self.transition_probabilities[s, a, :] *
                                               (self.rewards[s, a, :] + self.gamma * prev_V))
                V[s] = np.max(action_values)
            if np.max(np.abs(V - prev_V)) < epsilon:
                break
        policy = np.zeros(self.n_states, dtype=int)
        for s in range(self.n_states):
            action_values = np.zeros(self.n_actions)
            for a in range(self.n_actions):
                action_values[a] = np.sum(self.transition_probabilities[s, a, :] *
                                          (self.rewards[s, a, :] + self.gamma * V))
            policy[s] = np.argmax(action_values)
        return policy, V

# Example usage:
n_states = 3
n_actions = 2
transition_probabilities = np.array([[[0.7, 0.3, 0.0], [0.1, 0.8, 0.1]],
                                     [[0.0, 0.2, 0.8], [0.4, 0.4, 0.2]],
                                     [[0.2, 0.7, 0.1], [0.6, 0.3, 0.1]]])
rewards = np.array([[[10, 0, 0], [0, 0, 0]],
                    [[0, 0, 0], [0, 0, 0]],
                    [[0, 0, 0], [0, 0, -50]]])
gamma = 0.9

mdp_solver = MDPSolver(n_states, n_actions, transition_probabilities, rewards, gamma)

policy_pi = mdp_solver.policy_improvement()
print("Optimal Policy (Policy Improvement):", policy_pi)

policy_vi, value_vi = mdp_solver.value_iteration()
print("Optimal Policy (Value Iteration):", policy_vi)
print("Optimal Value Function (Value Iteration):", value_vi)
"""

    return code

def q_learning():

    code = """
import numpy as np
import random

class QLearning:
    def __init__(self, num_states, num_actions, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        self.num_states = num_states
        self.num_actions = num_actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = np.zeros((num_states, num_actions))

    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.randint(0, self.num_actions - 1)
        else:
            return np.argmax(self.q_table[state, :])

    def update_q_table(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state, :])
        td_target = reward + self.discount_factor * self.q_table[next_state, best_next_action]
        td_error = td_target - self.q_table[state, action]
        self.q_table[state, action] += self.learning_rate * td_error

    def train(self, env, num_episodes):
        for _ in range(num_episodes):
            state = env.reset()
            done = False
            while not done:
                action = self.choose_action(state)
                next_state, reward, done, _ = env.step(action)
                self.update_q_table(state, action, reward, next_state)
                state = next_state

    def test(self, env, num_episodes):
        total_rewards = []
        for _ in range(num_episodes):
            state = env.reset()
            done = False
            total_reward = 0
            while not done:
                action = np.argmax(self.q_table[state, :])
                next_state, reward, done, _ = env.step(action)
                total_reward += reward
                state = next_state
            total_rewards.append(total_reward)
        return total_rewards

# Example usage:

# Define environment (e.g., a simple gridworld)
class SimpleGridWorld:
    def __init__(self):
        self.num_states = 16
        self.num_actions = 4
        self.current_state = 0
        self.goal_state = 15

    def reset(self):
        self.current_state = 0
        return self.current_state

    def step(self, action):
        if action == 0:  # Move right
            self.current_state = min(self.current_state + 1, self.num_states - 1)
        elif action == 1:  # Move left
            self.current_state = max(self.current_state - 1, 0)
        elif action == 2:  # Move down
            self.current_state = min(self.current_state + 4, self.num_states - 1)
        elif action == 3:  # Move up
            self.current_state = max(self.current_state - 4, 0)

        if self.current_state == self.goal_state:
            reward = 1
            done = True
        else:
            reward = 0
            done = False

        return self.current_state, reward, done, {}

# Create Q-Learning agent
num_states = 16
num_actions = 4
q_learning_agent = QLearning(num_states, num_actions)

# Train the agent
env = SimpleGridWorld()
q_learning_agent.train(env, num_episodes=1000)

# Test the agent
test_rewards = q_learning_agent.test(env, num_episodes=100)
average_reward = np.mean(test_rewards)
print("Average reward:", average_reward)
"""
    return code

def monte_carlo():

    code = """
import numpy as np

# Define grid world dimensions
GRID_SIZE = (4, 4)
START_STATE = (2, 0)
GOAL_STATE = (0, 3)
ACTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

# Define behavior policy: equiprobable random policy
def behavior_policy(state):
    return np.random.choice(len(ACTIONS))

# Define target policy: greedy policy w.r.t. Q
def target_policy(state, Q):
    return np.argmax(Q[state[0], state[1]])

# Generate episode using given policy
def generate_episode(Q):
    episode = []
    state = START_STATE
    while state != GOAL_STATE:
        action = behavior_policy(state)
        next_state = (state[0] + ACTIONS[action][0], state[1] + ACTIONS[action][1])
        if next_state[0] < 0 or next_state[0] >= GRID_SIZE[0] or next_state[1] < 0 or next_state[1] >= GRID_SIZE[1]:
            next_state = state
        reward = -1  # Reward of moving to any state
        episode.append((state, action, reward))
        state = next_state
    return episode

# Monte Carlo Off-Policy Control with Importance Sampling
def off_policy_mc_control(num_episodes):
    Q = np.zeros((GRID_SIZE[0], GRID_SIZE[1], len(ACTIONS)))  # Action-value function
    C = np.zeros((GRID_SIZE[0], GRID_SIZE[1], len(ACTIONS)))  # Cumulative sum of importance sampling ratios

    for _ in range(num_episodes):
        episode = generate_episode(Q)
        G = 0  # Return
        W = 1  # Importance sampling ratio
        for t in range(len(episode) - 1, -1, -1):
            state, action, reward = episode[t]
            G = G + reward
            C[state[0], state[1], action] += W
            Q[state[0], state[1], action] += (W / C[state[0], state[1], action]) * (G - Q[state[0], state[1], action])
            if action != target_policy(state, Q):
                break
            W = W * 1 / 0.25  # Importance sampling ratio for equiprobable random policy

    return Q

# Test the algorithm
def test():
    num_episodes = 10
    Q = off_policy_mc_control(num_episodes)
    optimal_policy = np.argmax(Q, axis=2)
    print("Optimal policy:")
    print(optimal_policy)
"""
    return code

def sarsa():

    code = """
import numpy as np

class Environment:
    def __init__(self):
        self.num_states = 5
        self.num_actions = 2
        self.state = 2

    def reset(self):
        self.state = 2
        return self.state

    def step(self, action):
        if action == 0:
            self.state -= 1
        else:
            self.state += 1

        if self.state == 0:
            reward = -1
            done = True
        elif self.state == 4:
            reward = 1
            done = True
        else:
            reward = 0
            done = False

        return self.state, reward, done


class SARSA:
    def __init__(self, num_states, num_actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha  # learning rate
        self.gamma = gamma  # discount factor
        self.epsilon = epsilon  # exploration rate
        self.q_table = np.zeros((num_states, num_actions))

    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            # Explore: choose a random action
            return np.random.choice(self.num_actions)
        else:
            # Exploit: choose the action with highest Q-value for the current state
            return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state, next_action):
        predict = self.q_table[state, action]
        target = reward + self.gamma * self.q_table[next_state, next_action]
        self.q_table[state, action] += self.alpha * (target - predict)

    def train(self, env, episodes):
        for episode in range(episodes):
            state = env.reset()
            action = self.choose_action(state)

            while True:
                next_state, reward, done = env.step(action)
                next_action = self.choose_action(next_state)
                self.update_q_table(state, action, reward, next_state, next_action)

                state = next_state
                action = next_action

                if done:
                    break

            if episode % 100 == 0:
                print(f"Episode {episode}")

        print("Training finished.")

if __name__ == "__main__":
    env = Environment()
    agent = SARSA(env.num_states, env.num_actions)
    agent.train(env, episodes=1000)
"""
    return code