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
class AI:
    def __init__(self):
        self.game = SnakeGame()
        
        self.currentState = self.game.getStates()

        self.actions = ["UP", "DOWN", "LEFT", "RIGHT"]

        self.epsilon = 0.9

        self.qTable = np.zeros((1024,4))

        self.lr = 1e-2

        self.gamma = .85

        self.nextSave = 5000

    def stateToNum(self,state) -> int:
            sum = 0
            for i in range(len(state)):
                sum += 2**i*state[i]
            return int(sum)
            
    def learn(self):
        print(f'self.epsilon {self.epsilon} \nself.currentState {self.currentState}\nbest score: {self.game.bestScore}')
        if random.uniform(0,1)<self.epsilon:
            #do a random action
            self.game.takeAction(self.actions[random.randint(0,3)])
            self.game.update()
        else:
            #take best known action
            self.game.takeAction(self.actions[np.argmax(self.qTable[self.stateToNum(self.currentState),:])])
            self.game.update()
        
        # print(self.actions.index(self.game.change_to))
        newState = self.game.getStates()
        self.qTable[self.stateToNum(self.currentState),self.actions.index(self.game.change_to)] = self.qTable[self.stateToNum(self.currentState)][self.actions.index(self.game.change_to)] 
        + self.lr * (self.game.getScore() + self.gamma * np.max(self.qTable[self.stateToNum(newState),:] - self.qTable[self.stateToNum(self.currentState)][self.actions.index(self.game.change_to)]))
    
        # self.game.show()
        self.currentState = self.game.getStates()
        if(self.epsilon > .2):
            self.epsilon -= .0001
        self.nextSave -= 1
        if self.nextSave == 0:
            saveToJSON(self.qTable)
            self.nextSave=5000




   

def main():
    GameAI = AI()

    while(True):
        GameAI.learn()
        #game.update()
        #game.show()
        #GameAI.states = game.getStates()


if __name__ == '__main__':
    main()
