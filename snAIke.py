from SnakeGame import SnakeGame
import numpy as np
import random
import json


def saveToJSON(array: np.array) -> None:
    array = array.tolist()
    asDict = {}
    for i in range(len(array)):
        asDict[str(i)] = array[i]
    asJson = json.dumps(asDict)
    with open("qtable.txt", "w") as file:
        file.write(asJson)


def importJSON() -> np.array:
    with open("qtable.txt", "r") as file:
        asDict = dict(json.loads(file.read()))
        arr = np.zeros((118784*2, 4))
        row = 0
        col = 0
        for v in asDict.values():
            for a in v:
                arr[row][col] = a
                col += 1
            col = 0
            row += 1
        arr.reshape((118784*2, 4))
        # print(arr)
        return arr


class AI:
    def __init__(self, IMPORT=False):
        self.game = SnakeGame()

        self.currentState = self.game.getStates()

        self.actions = ["UP", "DOWN", "LEFT", "RIGHT"]

        self.epsilon = 0.9
        if IMPORT:
            self.qTable = importJSON()
        else:
            self.qTable = np.zeros((118784*2, 4))

        self.lr = .1

        self.gamma = .85

    def stateToNum(self, state) -> int:
        sum = 0
        for i in range(len(state)):
            sum += 2**i*state[i]
        return int(sum)

    def do_episode(self):
        self.game.reset()
        history = []
        while(True):
            if random.uniform(0, 1) < self.epsilon:
                # do a random action
                action = self.game.takeAction(self.actions[random.randint(0, 3)])
                self.game.update()
                history.append((self.stateToNum(self.currentState),self.actions.index(action),self.stateToNum(self.game.getStates())))
            else:
                # take best known action
                action = self.game.takeAction(self.actions[np.argmax(
                    self.qTable[self.stateToNum(self.currentState), :])])
                self.game.update()
                history.append((self.stateToNum(self.currentState),self.actions.index(action),self.stateToNum(self.game.getStates())))
            self.currentState = self.game.getStates()
            self.game.show()
            if(self.game.reset_next):
                self.learn(history,self.game.timed_out)
                break

        

    def learn(self,history,timed_out):
        
        history = list(reversed(history))

        dist = 0
        prev_dist = 0
        index = 0
        
        for exp in history:
            state = exp[0]
            action = exp[1]
            newState = exp [2]
            dist = newState>>10
            prev_dist = state>>10

            if index == 0:
                if timed_out:
                    reward = 1
                else:
                    reward = -1000
            elif abs(dist-prev_dist) > 1 and index != len(history)-1:
                reward = 500
            else:
                reward = 1

            # print(f'state {state}, action {action}, newState {newState}, dist {dist}, prev {prev_dist} reward {reward}')
            
            self.qTable[state, action] = self.qTable[state,action] + \
                self.lr * (reward + self.gamma * 
                np.max(
                    [self.qTable[newState, x] - \
                    self.qTable[state,action] for x in range(4)]))

            index += 1

        if(self.epsilon > .2):
            self.epsilon -= .01



def main():
    GameAI = AI(True)
    episodes = 1000000
    for currentEp in range(episodes):
        print(f'Game number: {currentEp+1}')
        GameAI.do_episode()
        if(currentEp%100 == 0):
            print("Saving!")
            saveToJSON(GameAI.qTable)


if __name__ == '__main__':
    main()
