from SnakeGame import SnakeGame
import tensorflow as tf
import numpy as np
import tensorflow.keras as k


class AI:
    def __init__(self):
        self.states = np.array(dtype=tf.int8)
        # ()
        self.actions = ["UP", "DOWN", "LEFT", "RIGHT"]

        self.model = [
            k.Dense(12),
            k.Dense(32, activation='relu'),
            k.Dense(4)
        ]

        self.model.compile(
            optimizer=k.optimizers.Adam(learning_rate=0.001),
            loss=k.losses.MeanSquaredError(from_logits=True)
        )


def main():
    game = SnakeGame()

    while(True):
        game.update()
        game.show()


if __name__ == '__main__':
    main()
