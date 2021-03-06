from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

import numpy as np
import random
from collections import deque


rotate_location = [4, 9, 14, 19, 24, 3, 8, 13, 18, 23, 2, 7, 12, 17, 22, 1, 6, 11, 16, 21, 0, 5, 10, 15, 20]


def rotate(board):
    rotated_board = []
    for location in rotate_location:
        rotated_board.append(int(board[location]))
    if len(board) > 25:
        rotated_board.append(int(board[25]))
    return rotated_board


def get_rotate_boards(s, t):
    states, targets = [], []
    for i in range(len(s)):
        os = s.popleft()
        ot = t.popleft()
        states.append(os[:])
        targets.append(ot[:])
        for rotation in range(3):
            os = rotate(os)
            ot = rotate(ot)
            states.append(os[:])
            targets.append(ot[:])
    return states, targets


class Agent:
    def __init__(self, state_size, action_size, model_name=None):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.memory2 = []
        self.model_name = model_name
        self.gamma = 0.95
        self.data = 1_500_000
        self.epsilon = 1.0
        self.epsilon_min = .25
        self.epsilon_decay = float(np.e)**float(np.log(self.epsilon_min/self.epsilon)/self.data)
        print('stat:', self.data, self.epsilon_decay)
        if model_name:
            try:
                print('loading model')
                self.model = load_model(f'keras_model/{model_name}')
            except:
                print('fail to load model, creating new model')
                self.model = self.model()
        else:
            print('creating new model')
            self.model = self.model()

    def model(self):
        model = Sequential()
        model.add(Dense(units=512, input_dim=self.state_size, activation="relu"))
        model.add(Dense(units=512, activation="relu"))
        model.add(Dense(units=512, activation="relu"))
        model.add(Dense(units=512, activation="relu"))
        model.add(Dense(units=256, activation="relu"))
        model.add(Dense(units=256, activation="relu"))
        model.add(Dense(units=128, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=0.001))
        return model

    def act(self, state):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            if random.random() <= self.epsilon:
                empty_index = []
                for i in range(25):
                    if not state[0][i]:
                        empty_index.append(i)
                return empty_index[random.randrange(len(empty_index))]
        output = self.model.predict(state)
        # print(np.round(output[0][0:5], 2))
        # print(np.round(output[0][5:10], 2))
        # print(np.round(output[0][10:15], 2))
        # print(np.round(output[0][15:20], 2))
        # print(np.round(output[0][20:25], 2))
        return np.argmax(output)

    def exp_replay(self):
        states = []
        target_fs = []
        next_states = []
        # current_states = []
        for event in self.memory:
            # current_states.append(event[0][0][0])
            for [_, _, _, next_state, done] in event:
                if not done:
                    next_states.append(next_state[0])
        next_outputs = deque(self.model.predict(np.array(next_states), verbose=1))  # .tolist()
        # state_outputs = deque(self.model.predict(np.array(current_states), verbose=1))  # .tolist()
        for event in self.memory:
            state = event[0][0]
            # target_f = state_outputs.popleft()
            target_f = [0] * 25
            for [_, action, reward, _, done] in event:
                if done:
                    target = reward
                else:
                    # target = reward + (self.gamma * max(next_outputs.popleft()))
                    target = max(min(reward + (self.gamma * max(next_outputs.popleft())), 1), -1)
                target_f[action] = target
            states.append(np.array(state[0][:]))
            target_fs.append(np.array(target_f[:]))
        for [s, t] in self.memory2:
            states.append(s[0][:])
            target_fs.append(t[:])

        states, target_fs = get_rotate_boards(deque(states), deque(target_fs))

        self.model.fit([states], [target_fs], epochs=1, verbose=1, batch_size=8192)
