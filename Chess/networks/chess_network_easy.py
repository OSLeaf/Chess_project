import numpy as np
import tensorflow as tf
from tensorflow import keras
from output_dic import OUTPUTINDEX, REVERSEINDEX, INDEX

def main():
    inp = keras.layers.Input(shape=(14, 8, 8))

    flat = keras.layers.Flatten()(inp)
    l1 = keras.layers.Dense(256, activation='relu')(flat)
    l2 = keras.layers.Dense(256, activation='relu')(l1)
    l3 = keras.layers.Dense(256, activation='relu')(l2)
    l4 = keras.layers.Dense(256, activation='relu')(l3)
    l5 = keras.layers.Dense(256, activation='relu')(l4)
    l6 = keras.layers.Dense(256, activation='relu')(l5)

    policyOut = keras.layers.Dense(INDEX, name='policyHead', activation= 'softmax')(l6)

    valueOut_1 = keras.layers.Dense(256, activation='relu')(l6)
    valueOut_2 = keras.layers.Dense(1, name='valueHead', activation='tanh')(valueOut_1)

    bce = tf.keras.losses.CategoricalCrossentropy(from_logits=False)
    model = keras.Model(inp, [policyOut, valueOut_2])
    model.compile(optimizer='SGD', loss={'valueHead':'mean_squared_error', 'policyHead':bce})

    print(model.summary())

    model.save('Chess/networks/random_model_easy.keras')

if __name__ == "__main__":
    main()


