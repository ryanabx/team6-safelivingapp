import json
import numpy as np
from sklearn.model_selection import train_test_split
from keras.optimizers import Adam
from keras.losses import MeanSquaredError
from keras.callbacks import ModelCheckpoint
from keras.models import *
from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, Dropout
from keras.layers import Dense

def get_network():
    sample_rows = 5
    sample_cols = 12
    inputs = Input((sample_rows * sample_cols))
    hide1 = Dense(32, activation='relu', kernel_initializer='he_normal')(inputs)
    hide2 = Dense(16, activation='relu', kernel_initializer='he_normal')(hide1)
    hide3 = Dense(8, activation='relu', kernel_initializer='he_normal')(hide2)
    out = Dense(1, activation='linear', kernel_initializer='he_normal')(hide3)
    model = Model(inputs=inputs, outputs=out)
    model.compile(optimizer=Adam(lr=1e-4), loss='mse')
    return model

def main():
    model = get_network()
    data_dir = 'backend/backend_server.datasets/'
    x = np.load(data_dir + 'x.npy')
    y = np.load(data_dir + 'y.npy')
    g = np.load(data_dir + 'g.npy')
    g_lable = np.load(data_dir + 'g_label.npy')

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    model_checkpoint = ModelCheckpoint('model location', monitor='val_loss', verbose=1, save_best_only=True)
    hist = model.fit(x_train, y_train, batch_size=4, epochs=20, verbose=1, validation_split=0.1,
                     shuffle=True, callbacks=[model_checkpoint])
    y_pred = model.predict(x_test, batch_size=1, verbose=1)
    mse = MeanSquaredError()(y_test, y_pred).numpy()

    print('hist')
    print(hist)
    print('mse')
    print(mse)

if __name__ == "__main__":
    main()
