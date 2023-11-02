from typing import Callable, List

import numpy as np

# Implement your HMM for Part 1 here!


class HMM:

    # You may add instance variables, but you may not change the
    # initializer; HMMs will be initialized with the given __init__
    # function when grading.

    def __init__(
        self,
        sensor_model: Callable[[str, int], float],
        transition_model: Callable[[int, int], float],
        num_states: int,
    ):
        """
        Inputs:
        - sensor_model: the sensor model of the HMM.
          This is a function that takes in an observation E
          (represented as a string 'A', 'B', ...) and a state S
          (reprensented as a natural number 0, 1, ...) and
          outputs the probability of observing E in state S.

        - transition_model: the transition model of the HMM.
          This is a function that takes in two states, s and s',
          and outputs the probability of transitioning from
          state s to state s'.

        - num_states: this is the number of hidden states in the HMM, an integer
        """
        # Initialize your HMM here!
        self.observations = []
        self.timestep = 0
        self.pd = []
        for i in range(num_states):
          self.pd.append(1 / num_states)
        self.sensor_model = sensor_model
        self.transition_model = transition_model
        self.num_states = num_states

    def tell(self, observation: str):
        """
        Takes in an observation and records it.
        You will need to keep track of the current timestep and increment
        it for each observation.

        Input:
        - observation: The observation at the current timestep, a string

        Output:
        - None
        """
        # Write your code here!
        self.observations.append(observation)
        new_pd = []
        for ts in range(self.num_states):
          add = 0
          for s in range(self.num_states):
            add += self.transition_model(s, ts) *  self.pd[s]
          add *= self.sensor_model(observation, ts)
          new_pd.append(add)
        sum = 0
        for i in range(self.num_states):
          sum += new_pd[i]
        for i in range(self.num_states):
          if sum != 0:
            new_pd[i] /= sum
        self.timestep += 1
        self.pd = new_pd

    def ask(self, time: int) -> List[float]:
        """
        Takes in a timestep that is greater than or equal to
        the current timestep and outputs a probability distribution
        (represented as a list) over states for that timestep.
        The index of the probability is the state it corresponds to.

        Input:
        - time: the timestep to get the observation distribution for, an integer

        Output:
        - a probability distribution over the hidden state for the given timestep, a list of numbers
        """
        # Write your code here!
        if time == self.timestep:
          return self.pd
        else:
          new_pd = []
          last_pd = self.ask(time - 1)
          for ts in range(self.num_states):
            add = 0
            for s in range(self.num_states):
              add += self.transition_model(s, ts) * last_pd[s]
            new_pd.append(add)
          sum = 0
          for i in range(self.num_states):
            sum += new_pd[i]
          for i in range(self.num_states):
            new_pd[i] /= sum
          return new_pd
