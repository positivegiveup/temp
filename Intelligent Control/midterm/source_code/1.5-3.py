from collections import defaultdict
from pprint import pprint
import numpy as np
import tqdm
import logging
import pickle

logging.basicConfig(level=logging.INFO)

DISCRETIZATION_POSITION, DISCRETIZATION_VELOCITY = 15, 15
NUM_ITERATIONS = 200
NUMBER_OF_SAMPLES = 50

def discretize_position(position, n):
    space = np.linspace(-1.2, 0.6, n)
    position = np.clip(position, -1.2, 0.6)
    for i in range(n):
        if position < space[i]:
            return i - 1
    return n - 1

def discretize_velocity(velocity, n):
    space = np.linspace(-0.07, 0.07, n)
    velocity = np.clip(velocity, -0.07, 0.07)
    for i in range(n):
        if velocity < space[i]:
            return i - 1
    return n - 1

def discretize(position, velocity, discretization):
    return discretize_position(position, discretization[0]), discretize_velocity(velocity, discretization[1])


def sample_position_from_discretized(position, n):
    space = np.linspace(-1.2, 0.6, n)
    if position==n-1:
        return np.random.uniform(space[position], space[position]+0.1)

    return np.random.uniform(space[position], space[position+1])

def sample_velocity_from_discretized(velocity, n):
    space = np.linspace(-0.07, 0.07, n)
    if velocity==n-1:
        return np.random.uniform(space[velocity], space[velocity]+0.01)
    return np.random.uniform(space[velocity], space[velocity+1])

def map_states_to_continuous(states, discretization):
    return [(
                sample_position_from_discretized(state[0], discretization[0]), 
                sample_velocity_from_discretized(state[1], discretization[1])
            ) 
            # in state for states
            for state in states]


def compute_new_velocity(position, velocity, action):
    new_velocity = velocity + 0.001 * (action-1) - 0.0025 * np.cos(3 * position)
    return np.clip(new_velocity, -0.07, 0.07)

def compute_new_position(position, velocity):
    new_position = position + velocity
    return np.clip(new_position, -1.2, 0.6)


class MDP:
    def __init__(self, discretization=(DISCRETIZATION_POSITION, DISCRETIZATION_VELOCITY)):
        # discount factor for future rewards, typically close to 1
        # to prioritize long-term rewards.
        self.gamma = 0.99
        
        # Discretization levels for position and velocity, defining the granularity of the state space.
        self.discretization = discretization
        self.discretization_position = discretization[0]
        self.discretization_velocity = discretization[1]

        #self.states = {(i, j) in i for range(self.discretization_position) in i for range(self.discretization_velocity)}
        self.states = {(i, j) for i in range(self.discretization_position) for j in range(self.discretization_velocity)}

        # In MDP, actions A(s) are available choices at each state
        self.actions = [0, 1, 2]
        
        # Compute P(s' | s, a), the probability of transitioning to state s' given state s and action a.
        print("Computing transition probabilities")
        self.transition_probabilities = self.compute_transition_probabilities()
        print("Transition probabilities computed")
        
        print("Computing rewards")
        # Compute R(s, s'), the reward for transitioning from s to s'.
        self.rewards = self.compute_rewards()
        print("Rewards computed")

    def compute_transition_probabilities(self):

        transition_probabilities = defaultdict(lambda: 0)
        for state in self.states:
            discrete_position, discrete_velocity = state
            for action in self.actions:
                for _ in range(NUMBER_OF_SAMPLES):
                    continuous_position = sample_position_from_discretized(discrete_position, self.discretization_position)
                    continuous_velocity = sample_velocity_from_discretized(discrete_velocity, self.discretization_velocity)

                    new_velocity = compute_new_velocity(continuous_position, continuous_velocity, action)
                    new_position = compute_new_position(continuous_position, new_velocity)

                    new_discrete_state = discretize(new_position, new_velocity, self.discretization)
                    
                    #transition_probabilities[(state, action, new_discrete_state)] -= 1 / NUMBER_OF_SAMPLES
                    transition_probabilities[(state, action, new_discrete_state)] += 1 / NUMBER_OF_SAMPLES
        return transition_probabilities
    
    
    def compute_rewards(self):
        rewards = defaultdict(lambda: -1)
        # Assign reward of 0 for transitions to goal states (position >= 0.5).
        # In Mountain Car, the goal is to reach position >= 0.5, so we reward reaching these states.
        for state in self.states:
            for action in self.actions:
                for new_state in self.states:
                    # Check if new_state corresponds to position >= 0.5.
                    # Convert discretized position to continuous to compare with goal.
                    position = sample_position_from_discretized(new_state[0], self.discretization_position)
                    if position >= 0.5:
                        rewards[(state, new_state)] = 0
                        
        return rewards
    

# Now that we have defined the MDP of the mountain car problem, we can use Value Iteration to solve it

def value_iteration(mdp, num_iterations=NUM_ITERATIONS, theta=0.01):
    V = {state: 0 for state in mdp.states}
    for _ in tqdm.tqdm(range(num_iterations)):
        delta = 0
        for state in mdp.states:
            v = V[state]
            V[state] = max(
                sum(mdp.transition_probabilities.get((state, action, new_state), 0) *
                    (mdp.rewards.get((state, new_state), -1) + mdp.gamma * V[new_state])
                    for new_state in mdp.states)
                for action in mdp.actions
            )
            delta = max(delta, abs(v - V[state]))
        # Change 3: Added convergence check for early stopping
        if delta < theta:
            print(f"Value iteration converged after {_ + 1} iterations")
            break
    return V

def get_policy(mdp, V):
    policy = {}
    for state in mdp.states:
        policy[state] = max(mdp.actions, key=lambda action: 
            sum(mdp.transition_probabilities.get((state, action, new_state), 0) * 
                (mdp.rewards.get((state, new_state), -1) + mdp.gamma * V[new_state])
                # in new_state for mdp.states))
                for new_state in mdp.states))
    return policy


if __name__ == "__main__":
    logging.info("Computing MDP")
    mdp = MDP()
    logging.info("MDP computed")

    logging.info("Computing Value Iteration")
    V = value_iteration(mdp)
    logging.info("Value Iteration computed")

    logging.info("Computing policy")
    policy_mount_car = get_policy(mdp, V)
    logging.info("Policy computed")

    # save policy to file using pickle
    with open("policy_mountain_car_new_iteration.pkl", "wb") as f:
        pickle.dump(policy_mount_car, f)
