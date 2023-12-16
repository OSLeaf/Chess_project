import numpy as np
import tensorflow as tf
from tensorflow import keras
import random

def main():
    inp = keras.layers.Input(shape=(18, 8, 8))

    l1 = keras.layers.Conv2D(129, kernel_size=(3, 3), strides=1, activation='relu', padding='same')(inp)
    l2 = keras.layers.Conv2D(129, kernel_size=(3, 3), strides=1, activation='relu', padding='same')(l1)
    l3 = keras.layers.Conv2D(129, kernel_size=(3, 3), strides=1, activation='relu', padding='same')(l2)
    #l4 = keras.layers.Conv2D(256, kernel_size=(3, 3), strides=1, activation='relu', padding='same')(l3)
    #l5 = keras.layers.Conv2D(256, kernel_size=(3, 3), strides=1, activation='relu', padding='same')(l4)
    #l6 = keras.layers.Conv2D(256, kernel_size=(3, 3), strides=1, activation='relu', padding='same')(l5)

    up1 = keras.layers.Conv2D(129, kernel_size=(3, 3), strides=1, activation = 'relu', padding = 'same')(keras.layers.UpSampling2D(size = (1,1))(l3))
    merge1 = keras.layers.concatenate([l3,up1], axis = 1)
    up2 = keras.layers.Conv2D(129, kernel_size=(3, 3), strides=1, activation = 'relu', padding = 'same')(keras.layers.UpSampling2D(size = (1,1))(merge1))
    merge2 = keras.layers.concatenate([l2,up2], axis = 1)
    up3 = keras.layers.Conv2D(129, kernel_size=(3, 3), strides=1, activation = 'relu', padding = 'same')(keras.layers.UpSampling2D(size = (1,1))(merge2))
    merge3 = keras.layers.concatenate([l1,up3], axis = 1)
    #up4 = keras.layers.Conv2D(256, kernel_size=(3, 3), strides=1, activation = 'relu', padding = 'same')(keras.layers.UpSampling2D(size = (1,1))(merge3))
    #merge4 = keras.layers.concatenate([l2,up4], axis = 1)
    #up5 = keras.layers.Conv2D(256, kernel_size=(3, 3), strides=1, activation = 'relu', padding = 'same')(keras.layers.UpSampling2D(size = (1,1))(merge4))
    #merge5 = keras.layers.concatenate([l1,up5], axis = 1)


    policy_conv = keras.layers.Conv2D(2, kernel_size=(1, 1), strides=1, activation='relu')(merge3)
    policyt_flatten = keras.layers.Flatten()(policy_conv)
    policyOut = keras.layers.Dense(4544, name='policyHead', activation= 'softmax')(policyt_flatten)

    value_conv = keras.layers.Conv2D(1, kernel_size=(1, 1), strides=1, activation='relu')(merge3)
    value_flatten = keras.layers.Flatten()(value_conv)
    valueOut_1 = keras.layers.Dense(129, activation='relu')(value_flatten)
    valueOut_2 = keras.layers.Dense(1, name='valueHead', activation='tanh')(valueOut_1)

    bce = tf.keras.losses.CategoricalCrossentropy(from_logits=False)
    model = keras.Model(inp, [policyOut, valueOut_2])
    model.compile(optimizer='SGD', loss={'valueHead':'mean_squared_error', 'policyHead':bce})

    print(model.summary())

    model.save('Chess/networks/random_model.keras')

if __name__ == "__main__":
    main()


