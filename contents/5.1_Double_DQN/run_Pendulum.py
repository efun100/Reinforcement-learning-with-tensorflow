"""
Double DQN & Natural DQN comparison,
The Pendulum example.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/

Using:
Tensorflow: 1.0
gym: 0.8.0
"""


import gym
from RL_brain import DoubleDQN
import numpy as np


env = gym.make('Pendulum-v0')
env = env.unwrapped
env.seed(1)
MEMORY_SIZE = 3000
ACTION_SPACE = 11

natural_DQN = DoubleDQN(
    n_actions=ACTION_SPACE, n_features=3, memory_size=MEMORY_SIZE,
    e_greedy_increment=0.001, double_q=False)


double_DQN = DoubleDQN(
    n_actions=ACTION_SPACE, n_features=3, memory_size=MEMORY_SIZE,
    e_greedy_increment=0.001, double_q=True)


def train(RL):
    total_steps = 0
    observation = env.reset()
    while True:
        # if total_steps - MEMORY_SIZE > 8000:
        env.render()

        action = RL.choose_action(observation)

        f_action = (action-(ACTION_SPACE-1)/2)/((ACTION_SPACE-1)/4)   # convert to [-2 ~ 2] float actions
        observation_, reward, done, info = env.step(np.array([f_action]))

        reward /= 10     # normalize to a range of (-1, 0). r = 0 when get upright
        # the Q target at upright state will be 0, because Q_target = r + gamma * Qmax(s', a') = 0 + gamma * 0
        # so when Q at this state is greater than 0, the agent overestimates the Q. Please refer to the final result.

        RL.store_transition(observation, action, reward, observation_)

        if total_steps > MEMORY_SIZE:   # learning
            RL.learn()

        if total_steps - MEMORY_SIZE > 20000:   # stop game
            break

        observation = observation_
        total_steps += 1
    return RL.q

#q_natural = train(natural_DQN)
#natural_DQN.save_model("natural_DQN.h5")

q_double = train(double_DQN)
double_DQN.save_model("double_DQN.h5")
