import numpy as np
import tensorflow as tf
from tensorflow import keras

def main():
    inp = keras.layers.Input(shape=(14, 8, 8))

    l1 = keras.layers.Conv2D(256, (3, 3), padding='same')(inp)
    Batch1 = keras.layers.BatchNormalization()(l1)
    act1 = keras.layers.Activation('relu')(Batch1)

    l2 = keras.layers.Conv2D(256, (3, 3), padding='same')(act1)
    Batch2 = keras.layers.BatchNormalization()(l2)
    act2 = keras.layers.Activation('relu')(Batch2)

    l3 = keras.layers.Conv2D(256, (3, 3), padding='same')(act2)
    Batch3 = keras.layers.BatchNormalization()(l3)
    act3 = keras.layers.Activation('relu')(Batch3)

    l4 = keras.layers.Conv2D(256, (3, 3), padding='same')(act3)
    Batch4 = keras.layers.BatchNormalization()(l4)
    act4 = keras.layers.Activation('relu')(Batch4)

    l5 = keras.layers.Conv2D(256, (3, 3), padding='same')(act4)
    Batch5 = keras.layers.BatchNormalization()(l5)
    act5 = keras.layers.Activation('relu')(Batch5)

    l6 = keras.layers.Conv2D(256, (3, 3), padding='same')(act5)
    Batch6 = keras.layers.BatchNormalization()(l6)
    act6 = keras.layers.Activation('relu')(Batch6)


    policy_conv = keras.layers.Conv2D(2, kernel_size=(1, 1), strides=1, activation='relu')(act6)
    policyt_flatten = keras.layers.Flatten()(policy_conv)
    policyOut = keras.layers.Dense(4208, name='policyHead', activation= 'softmax')(policyt_flatten)

    value_conv = keras.layers.Conv2D(1, kernel_size=(1, 1), strides=1, activation='relu')(act6)
    value_flatten = keras.layers.Flatten()(value_conv)
    valueOut_1 = keras.layers.Dense(256, activation='relu')(value_flatten)
    valueOut_2 = keras.layers.Dense(1, name='valueHead', activation='tanh')(valueOut_1)

    bce = tf.keras.losses.CategoricalCrossentropy(from_logits=False)
    model = keras.Model(inp, [policyOut, valueOut_2])
    model.compile(optimizer='SGD', loss={'valueHead':'mean_squared_error', 'policyHead':bce})

    print(model.summary())

    model.save('Chess/networks/random_model_GPT.keras')

if __name__ == "__main__":
    main()


