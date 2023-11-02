import numpy as np
from hmm import HMM
# Implement part 2 here!


class touchscreenHMM:


    # You may add instance variables, but you may not create a
    # custom initializer; touchscreenHMMs will be initialized
    # with no arguments.


    def __init__(self, width=20, height=20):
        """
        Feel free to initialize things in here!
        """
        self.width = width
        self.height = height
        # Write your initialization code here!
        self.num_state = width * height
        self.hmm = HMM(self._sensor_model, self._transition_model, self.num_state)
        self.prev_state = -7

        # self.hm = HMM(self._sensor_model, self._transition_model, width * height)
        # self.width = width
        # self.height = height

    # NOTE: _sensor_model and _transition_model are private helper functions,
    # which means that they will only be called by you. This also means you are
    # free to change the parameters of these functions as you see fit. You may
    # even delete them! They are only here to point you in the right direction.

    def _sensor_model(self, observation: str, state: float) -> float:
        """
        This is the sensor model to get the probability of getting an observation from a state.

        Input:
        - observation: A 2D NumPy array filled with 0s, and a single 1 denoting a touch location.
        - state:       A float, denoting the unique integer alternative of the numpy array

        Output:
        - The probability of observing that observation from that given state, a number.
        """
        # # Write your code here!
        obs = float(observation)
        if self.prev_state == -7:
            if state == obs:
                p = 1
            else:
                p = 0.01
        else:
            p = self._transition_model(state, obs)

        return p

    def _transition_model(self, old_state: float, new_state: float) -> float:
        """
        This will be your transition model to go from the old state to the new state.

        Input:
        - old_state: A float, denoting the unique integer alternative of the numpy array
        - new_state: A float, denoting the unique integer alternative of the numpy array

        Output:
        - The probability of transitioning from the old state to the new state, a number.
        """
        
        #Write your code here!
        p = -7
        vert_dist = abs((old_state//self.width) - (new_state//self.width))
        h_dist = abs((old_state % self.width) - (new_state % self.width))
        diag_dist = pow((pow(vert_dist, 2) + pow(h_dist, 2)), 0.5)
        is_old_border = ((old_state//self.width) == 0) or ((old_state % self.width) == 0) or ((old_state//self.width) == self.height -1) or ((old_state % self.width) == self.width - 1)
        is_corner = (old_state == 0) or (old_state == self.width -1) or (old_state == (self.width * self.height) - self.width) or (old_state == (self.width * self.height) - 1)
        # satifying the 2nd hint abt the finger either staying where it is or moving to one of the 8 adjacent locations.
        if min(vert_dist+h_dist, diag_dist) <= 1:
            if is_old_border and (not(is_corner)):
                p = 1/6
            elif is_corner:
                p = 1/4
            else:
                p = 1/9
        else:
            p = 0.01
        return p

        """
        else:
            p += 1/8
            if (len(self.prev_states) > 0):
                is_prev_border = ((self.prev_states[-1]//self.width) == 0) or ((self.prev_states[-1] % self.width) == 0)
                if is_old_border and (old_state == new_state) and not(is_prev_border):
                    return 1
                elif (new_state - old_state == 1) and (old_state - self.prev_states[-1] == 1):
                    p += 0.25
                    if (len(self.prev_states) > 1):
                        if (self.prev_states[-1] - self.prev_states[-2] == 1):
                            p += 0.25
                elif (new_state - old_state == -1) and (old_state - self.prev_states[-1] == -1):
                    p += 0.25
                    if (len(self.prev_states) > 1):
                        if (self.prev_states[-1] - self.prev_states[-2] == -1):
                            p += 0.25
                elif (new_state - old_state == self.width) and (old_state - self.prev_states[-1] == self.width):
                    p += 0.25
                    if (len(self.prev_states) > 1):
                        if (self.prev_states[-1] - self.prev_states[-2] == self.width):
                            p += 0.25
                elif (new_state - old_state == -self.width) and (old_state - self.prev_states[-1] == -self.width):
                    p += 0.25
                    if (len(self.prev_states) > 1):
                        if (self.prev_states[-1] - self.prev_states[-2] == -self.width):
                            p += 0.25
                elif (new_state - old_state == self.width + 1) and (old_state - self.prev_states[-1] == self.width + 1):
                    p += 0.25
                    if (len(self.prev_states) > 1):
                        if (self.prev_states[-1] - self.prev_states[-2] == self.width + 1):
                            p += 0.25
                elif (new_state - old_state == -self.width - 1) and (old_state - self.prev_states[-1] == -self.width - 1):
                    p += 0.25
                    if (len(self.prev_states) > 1):
                        if (self.prev_states[-1] - self.prev_states[-2] == -self.width - 1):
                            p += 0.25
                elif (new_state - old_state == self.width - 1) and (old_state - self.prev_states[-1] == self.width - 1):
                    p += 0.25
                    if (len(self.prev_states) > 1):
                        if (self.prev_states[-1] - self.prev_states[-2] == self.width - 1):
                            p += 0.25
                elif (new_state - old_state == -self.width + 1) and (old_state - self.prev_states[-1] == -self.width + 1):
                    p += 0.25
                    if (len(self.prev_states) > 1):
                        if (self.prev_states[-1] - self.prev_states[-2] == -self.width + 1):
                            p += 0.25
                elif is_old_border and is_prev_border and (len(self.prev_states) > 1):
                    if (new_state - old_state == 1) and (self.prev_states[-1] - self.prev_states[-2] == -1):
                        p += 0.25
                    if (new_state - old_state == -1) and (self.prev_states[-1] - self.prev_states[-2] == 1):
                        p += 0.25
                    if (new_state - old_state == self.width) and (self.prev_states[-1] - self.prev_states[-2] == -self.width):
                        p += 0.25
                    if (new_state - old_state == -self.width) and (self.prev_states[-1] - self.prev_states[-2] == self.width):
                        p += 0.25
                    if (new_state - old_state == self.width + 1) and (self.prev_states[-1] - self.prev_states[-2] == -self.width + 1):
                        p += 0.25
                    if (new_state - old_state == -self.width + 1) and (self.prev_states[-1] - self.prev_states[-2] == self.width + 1):
                        p += 0.25
                    if (new_state - old_state == self.width - 1) and (self.prev_states[-1] - self.prev_states[-2] == self.width + 1):
                        p += 0.25
        """

    def filter_noisy_data(self, frame: np.ndarray) -> np.ndarray:
        """
        This is the function we will be calling during grading, passing in a noisy simualation. It should return the
        distribution where you think the actual position of the finger is in the same format that it is passed in as.

        DO NOT CHANGE THE FUNCTION PARAMETERS

        Input:
        - frame: A noisy frame to run your HMM on. This is a 2D NumPy array
                 filled with 0s, and a single 1 denoting a touch location.

        Output:
        - A 2D NumPy array with the probabilities of the actual finger location.
        """
        # Write your code here!
        o_int = 0
        fo = frame.flatten()
        for cell in fo:
            if cell == 1:
                break
            o_int += 1
        self.hmm.tell(str(o_int))
        res = self.hmm.ask(self.hmm.timestep) #[0,0,0.25,0.5]
        max_value = max(res)
        for i, item in enumerate(res):
            if item == max_value:
                self.prev_state = i
        return np.asarray(res).reshape((self.width, self.height))


if __name__ == "__main__":
    from touchscreen_helpers.generate_data import create_simulations

    # TODO: Use create_simulations to perform data analysis on several simulations.
    #
    # Here are some questions you may want to find answers for by performing
    # statistics on the simulations:
    #   - How often is the finger position (actual frame) the same as the
    #     observed finger position (noisy frame)?
    #   - If the observation is different frame the actual frame, how far away
    #     is it? Are certain distances more likely than others?
    #   - How likely does the finger continue in the same direction it was going?
    #
    # Come up with your own questions and try to answer them by analyzing the
    # generated simulations. Try to think about which statistics will inform
    # your sensor model, and which ones will inform your transition model!

    pass
