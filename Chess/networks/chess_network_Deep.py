import numpy as np
import tensorflow as tf
from tensorflow import keras

def main():
    inp = keras.layers.Input(shape=(1, 14, 64))

    def Block(input):
        l = keras.layers.Conv2D(256, (3, 3), padding='same')(input)
        Batch = keras.layers.BatchNormalization()(l)
        act = keras.layers.Activation('relu')(Batch)
        l2 = keras.layers.Conv2D(256, (3, 3), padding='same')(act)
        Batch2 = keras.layers.BatchNormalization()(l2)
        skip = keras.layers.Add()([input,Batch2])
        act2 = keras.layers.Activation('relu')(skip)
        return act2
    def Blockwithoutskip(input):
        l = keras.layers.Conv2D(256, (3, 3), padding='same')(input)
        Batch = keras.layers.BatchNormalization()(l)
        act = keras.layers.Activation('relu')(Batch)
        l2 = keras.layers.Conv2D(256, (3, 3), padding='same')(act)
        Batch2 = keras.layers.BatchNormalization()(l2)
        act2 = keras.layers.Activation('relu')(Batch2)
        return act2

    block1 = Blockwithoutskip(inp)
    block2 = Block(block1)
    block3 = Block(block2)
    block4 = Block(block3)
    block5 = Block(block4)
    block6 = Block(block5)
    block7 = Block(block6)
    block8 = Block(block7)
    block9 = Block(block8)
    block10 = Block(block9)
    block11 = Block(block10)
    block12 = Block(block11)
    block13 = Block(block12)
    block14 = Block(block13)
    block15 = Block(block14)
    #block16 = Block(block15)
    #block17 = Block(block16)
    #block18 = Block(block17)
    #block19 = Block(block18)


    policy_conv = keras.layers.Conv2D(2, kernel_size=(1, 1), strides=1, activation='relu')(block15)
    policyt_flatten = keras.layers.Flatten()(policy_conv)
    policyOut = keras.layers.Dense(4208, name='policyHead', activation= 'softmax')(policyt_flatten)

    value_conv = keras.layers.Conv2D(1, kernel_size=(1, 1), strides=1, activation='relu')(block15)
    value_flatten = keras.layers.Flatten()(value_conv)
    valueOut_1 = keras.layers.Dense(256, activation='relu')(value_flatten)
    valueOut_2 = keras.layers.Dense(1, name='valueHead', activation='tanh')(valueOut_1)

    bce = tf.keras.losses.CategoricalCrossentropy(from_logits=False)
    model = keras.Model(inp, [policyOut, valueOut_2])
    model.compile(optimizer='ADAM', loss={'valueHead':'mean_squared_error', 'policyHead':bce})

    print(model.summary())

    model.save('Chess/networks/random_model_Deep.keras')

if __name__ == "__main__":
    main()


