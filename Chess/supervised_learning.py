import numpy as np
import tensorflow as tf
from tensorflow import keras
from output_dic import INDEX, OUTPUTINDEX

model = keras.models.load_model('Chess/networks/random_model_Deep.keras')

'''for i in range(0, 496, 100):
    print(i)
    gPos = []
    gProb = []
    gVal = []
    for j in range(1, 501):
        positions = np.load(f"stockfish/games/movesAndPositions{i + j}.npy", allow_pickle=True)
        for p in range(0, len(positions[2])):
            gPos.append(positions[0][p])
            gProbtemp = positions[1][p]
            gVal.append(positions[2][p])

            masked_output = np.zeros(INDEX)
            min = 1000
            for k in gProbtemp:
                if k[1] != None:
                    if k[1] < min:
                        min = k[1]
            sum = 0
            for k in gProbtemp:
                if k[1] != None:
                    sum += (k[1] - min)
            if sum != 0:
                for k in gProbtemp:
                    m_idx = OUTPUTINDEX[str(k[0])]
                    if k[1] != None:
                        masked_output[m_idx] = (k[1] - min) / sum
            gProb.append(masked_output)

    model.fit(np.array(gPos),[np.array(gProb), np.array(gVal)], epochs = 256, batch_size = 256, verbose = 0)

    if((i + j)%100 == 0):
        model.save('Chess/networks/sd_full_' + str(i + j) + '.keras')'''

#tahn activation
'''for i in range(0, 1):
    print(i)
    gPos = []
    gProb = []
    gVal = []
    for j in range(1, 501):
        positions = np.load(f"stockfish/games/movesAndPositions{i + j}.npy", allow_pickle=True)
        for p in range(0, len(positions[2])):
            gPos.append(positions[0][p])
            gProbtemp = positions[1][p]
            gVal.append(positions[2][p])

            masked_output = np.zeros(INDEX)
            min = 1000
            max = -1000
            for k in gProbtemp:
                if k[1] != None:
                    if k[1] < min:
                        min = k[1]
                    if k[1] > max:
                        max = k[1]

            if max > (min * -1):
                scale = max
            else:
                scale = min
                        
            if sum != 0:
                for k in gProbtemp:
                    m_idx = OUTPUTINDEX[str(k[0])]
                    if k[1] != None and scale != 0:
                        masked_output[m_idx] = (k[1]) / scale
            gProb.append(masked_output)
    print(i + j)
    model.fit(np.array(gPos),[np.array(gProb), np.array(gVal)], epochs = 256, batch_size = 256, verbose = 0)

    if((i + j)%100 == 0):
        model.save('Chess/networks/sd_tahn_' + str(i + j) + '.keras')'''

for i in range(0, 1, 500):
    print(i)
    gPos = []
    gProb = []
    gVal = []
    for j in range(1, 1036):
        positions = np.load(f"stockfish/games/movesAndPositions{i + j}.npy", allow_pickle=True)
        for p in range(0, len(positions[2])):
            gPos.append([positions[0][p].reshape(14, 64)])
            gProbtemp = positions[1][p]
            gVal.append(positions[2][p])

            masked_output = np.zeros(INDEX)
            min = 1000
            for k in gProbtemp:
                if k[1] != None:
                    if k[1] < min:
                        min = k[1]
            sum = 0
            for k in gProbtemp:
                if k[1] != None:
                    sum += (k[1] - min)
            if sum != 0:
                for k in gProbtemp:
                    m_idx = OUTPUTINDEX[str(k[0])]
                    if k[1] != None:
                        masked_output[m_idx] = (k[1] - min) / sum
            gProb.append(masked_output)

    max = 0
    for k in gVal:
        if k > 0:
            if k > max:
                max = k
        else:
            if -k > max:
                max = -k

    gVal = [x / max for x in gVal]              

    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='policyHead_loss', factor=0.1, patience=3, min_lr=0)
    model.fit(np.array(gPos),[np.array(gProb), np.array(gVal)], epochs = 128, batch_size = 256, callbacks=reduce_lr)

    if((i + j)%1035 == 0):
        model.save('Chess/networks/sd_deep4_' + str(i + j) + '.keras')