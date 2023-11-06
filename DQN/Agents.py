import tensorflow as tf
import numpy as np

class DQNAgent:
    def __init__(self, state_dim, action_dim,gamma):
        self.state_size = state_dim
        self.action_size = action_dim
        self.gamma = gamma
        self.model = self._build_model()  # Build the neural network model

    def _build_model(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(64, input_dim=self.state_size, activation='relu'))
        model.add(tf.keras.layers.Dense(64, activation='relu'))
        model.add(tf.keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3))
        return model

    def get_action(self, states):
        return np.argmax(self.model.predict(states),axis=1)

    def update(self,states,actions,next_states,rewards,dones):
        """
        Update Actor and Critic Networks

        Parameters
        ----------
            state: The states from 0 to n-1
            action: The actions the agent made at each state
            next_state: The states from 1 to n
            reward: Reward received by agent at each step
            done: An array showing a 1 if at that step the agent completed moving throught he environment else 0

        Returns
        -------
            A tuple: (actor_loss,critic_loss)
        """
        Q = self.model.predict(states)
        Q[np.arange(len(states)),actions] = rewards + self.gamma * np.max(self.model.predict(next_states),axis=1)
        return self.model.fit(states,Q,epochs=1,verbose=0).history['loss'][0]
