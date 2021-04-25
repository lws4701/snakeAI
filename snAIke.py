from SnakeGame import SnakeGame
import tensorflow as tf
import numpy as np
import tensorflow.keras as k


class AI:
    def __init__(self):
        self.states = np.array()
        # ()
        self.actions = ["UP", "DOWN", "LEFT", "RIGHT"]

        self.model = k.models.Sequential([
            k.layers.Dense(10),
            k.layers.Dense(32, activation='relu'),
            k.layers.Dense(4)
        ])

        self.model.compile(
            optimizer=k.optimizers.Adam(learning_rate=0.001),
        )

    def fit_model(self):
        self.model.fit(self.states)


def main():
    game = SnakeGame()
    GameAI = AI()

    while(True):
        game.update()
        game.show()
        GameAI.states = game.getStates()
        GameAI.fit_model()


if __name__ == '__main__':
    main()
