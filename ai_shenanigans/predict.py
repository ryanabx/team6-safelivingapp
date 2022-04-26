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
    sample_cols = 10
    inputs = Input((sample_rows * sample_cols))
    hide1 = Dense(32, activation='relu', kernel_initializer='he_normal')(inputs)
    drop1 = Dropout(0.5)(hide1)
    hide2 = Dense(16, activation='relu', kernel_initializer='he_normal')(drop1)
    drop2 = Dropout(0.5)(hide2)
    hide3 = Dense(8, activation='relu', kernel_initializer='he_normal')(drop2)
    out = Dense(2, activation='linear', kernel_initializer='he_normal')(hide3)
    model = Model(inputs=inputs, outputs=out)
    model.compile(optimizer=Adam(lr=1e-4), loss='msle')
    return model
def train():
    x_train = np.load('x_train.npy')
    y_train = np.load('y_train.npy')
    model = get_network()
    model_checkpoint = ModelCheckpoint('model1.hdf5', monitor='val_loss', verbose=1, save_best_only=True)
    hist = model.fit(x_train, y_train, batch_size=4, epochs=20, verbose=1, validation_split=0.1,
                     shuffle=True, callbacks=[model_checkpoint])
    print('hist')
    print(hist)

def test():
    x_test = np.load('x_test.npy')
    y_test = np.load('y_test.npy')
    model = load_model('model1.hdf5')
    y_pred = model.predict(x_test, batch_size=1, verbose=1)
    mse = MeanSquaredError()(y_test, y_pred).numpy()
    print('mse')
    print(mse)
    y_pred_list = y_pred.tolist()
    y_true_list = y_test.tolist()
    json.dump(y_pred_list, open('y_pred.json', 'w'))
    json.dump(y_true_list, open('y_true.json', 'w'))

def predict():
    x = np.load('x.npy')
    print(x.shape)
    g = np.load('g.npy')
    g = g[:, :, [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
    g = np.reshape(g, (g.shape[0], g.shape[1] * g.shape[2]))
    print(g.shape)
    g_labels = np.load('g_label.npy')
    model = load_model('model1.hdf5')
    g_pred = model.predict(g, batch_size=1, verbose=1)
    g_dict = {g_label: gg.tolist() for g_label, gg in zip(g_labels, g_pred)}
    json.dump(g_dict, open('ori_future_preds.json', 'w'))

def old_train():
    model = get_network()
    data_dir = 'backend/backend_server/datasets/'
    x = np.load('x.npy')
    x = x[:, :, [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
    x = np.reshape(x, (x.shape[0], x.shape[1] * x.shape[2]))
    print('x')
    print(x.shape)
    y = np.load('y.npy')
    y = y[:, [0, 1]]
    print('y')
    print(y.shape)
    g = np.load('g.npy')
    g = g[:, :, [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
    g = np.reshape(g, (g.shape[0], g.shape[1] * g.shape[2]))
    print('g')
    print(g.shape)
    g_lable = np.load('g_label.npy')

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    np.save('x_train.npy', x_train)
    np.save('x_test.npy', x_test)
    np.save('y_train.npy', y_train)
    np.save('y_test.npy', y_test)
    print(x_train.shape)
    print(x_test.shape)
    print(y_train.shape)
    print(y_test.shape)

    #model_checkpoint = ModelCheckpoint('model1.hdf5', monitor='val_loss', verbose=1, save_best_only=True)
    #hist = model.fit(x_train, y_train, batch_size=4, epochs=20, verbose=1, validation_split=0.1,
    #                 shuffle=True, callbacks=[model_checkpoint])
    #y_pred = model.predict(x_test, batch_size=1, verbose=1)
    #mse = MeanSquaredError()(y_test, y_pred).numpy()

    #print('hist')
    #print(hist)
    #print('mse')
    #print(mse)
    #y_pred_list = y_pred.tolist()
    #y_true_list = y_test.tolist()
    #json.dump(y_pred_list, open('y_pred.json', 'w'))
    #json.dump(y_true_list, open('y_true.json', 'w'))
    pass


def main():
    #old_train()
    #train()
    test()
    predict()

if __name__ == "__main__":
    main()
