import numpy as np
import tensorflow as tf
from tensorflow import keras
import random

def main():
    inp = keras.layers.Input((21,))

    l1 = keras.layers.Dense(128, activation='relu')(inp)
    l2 = keras.layers.Dense(128, activation='relu')(l1)
    l3 = keras.layers.Dense(128, activation='relu')(l2)
    l4 = keras.layers.Dense(128, activation='relu')(l3)
    l5 = keras.layers.Dense(128, activation='relu')(l4)

    policyOut = keras.layers.Dense(28, name='policyHead', activation='softmax')(l5)
    valueOut = keras.layers.Dense(1, name='valueHead', activation='tanh')(l5)

    bce = tf.keras.losses.CategoricalCrossentropy(from_logits=False)
    model = keras.Model(inp, [policyOut, valueOut])
    model.compile(optimizer='SGD', loss={'valueHead':'mean_squared_error', 'policyHead':bce})

    print(model.summary())
    model.save('Hexapawn/networks/random_model.keras')

if __name__ == "__main__":
    main()
