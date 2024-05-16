from types import NoneType
from typing import Union

import pathlib as paths
import zipfile

import json
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras as ktf
import keras
from keras import models as mktf
from keras import layers as lktf
from keras import optimizers as oktf
from keras import preprocessing as ppktf
from keras import utils as uktf
from keras import losses as lsktf
import tensorflow.keras.preprocessing.image as tkpi
import sklearn.base as sk_base
import sklearn.model_selection as sk_modsel

from keras import regularizers

from PIL import Image as pillow_images

from IPython.display import display


class CNNCustomClassifier(sk_base.BaseEstimator, sk_base.ClassifierMixin):
    def __init__(self,
                 num_classes, input_shape,
                 epochs, batch_size,
                 optimizer, loss,
                 validation_split,

                 file_path_column_name,
                 label_column_name,

                 conv_layer_array,
                 conv_kernel_size_default,
                 conv_activation, conv_activation_parameter,
                 conv_pool_size, conv_dropout,

                 dense_layer_array,
                 dense_activation, dense_activation_parameter,
                 dense_dropout):
        self.num_classes = num_classes
        self.input_shape = input_shape
        self.epochs = epochs
        self.batch_size = batch_size
        self.optimizer = optimizer
        self.loss = loss
        self.validation_split=validation_split

        self.file_path_column_name = file_path_column_name
        self.label_column_name = label_column_name

        self.conv_layer_array = conv_layer_array
        self.conv_kernel_size_default = conv_kernel_size_default
        self.conv_activation = conv_activation
        self.conv_activation_parameter = conv_activation_parameter
        self.conv_pool_size = conv_pool_size
        self.conv_dropout = conv_dropout

        self.dense_layer_array = dense_layer_array
        self.dense_activation = dense_activation
        self.dense_activation_parameter = dense_activation_parameter
        self.dense_dropout = dense_dropout

        self.model = None

    def create_cnn_model(self):
        model = keras.Sequential()
        model.add(lktf.Input(shape=self.input_shape, name='input'))

        for i, conv_layer_config in list(enumerate(self.conv_layer_array)):
            conv_filters_i, conv_kernel_i, layers_i = conv_layer_config
            assert 'c' in layers_i
#             if i == 0:
#                 model.add(lktf.Conv2D(filters=conv_filters_i, kernel_size=(1, 1), padding='same'))

            print(f"Conv Layer config: {conv_layer_config}")

            model.add(lktf.Conv2D(
                filters=conv_filters_i, kernel_size=conv_kernel_i,
                padding='same',
#                 kernel_regularizer=regularizers.L2(1e-3),
#                 activity_regularizer=regularizers.L2(1e-3),
                name=f"conv2d-{i}_0"
            ))
#             if 'b' in layers_i:
#                 model.add(lktf.BatchNormalization(name=f"batch-{i}_0"))
            model.add(lktf.ReLU(name=f"relu-{i}_0"))
            conv2d_count = layers_i.count('c')
            if conv2d_count > 1:
                for c_i in range(0, conv2d_count-1):
                    model.add(lktf.Conv2D(
                        filters=conv_filters_i, kernel_size=conv_kernel_i,
                        padding='same',
        #                 kernel_regularizer=regularizers.L2(1e-3),
        #                 activity_regularizer=regularizers.L2(1e-3),
                        name=f"conv2d-{i}_{c_i+1}"
                    ))
#                     if 'b' in layers_i:
#                         model.add(lktf.BatchNormalization(name=f"batch-{i}_{c_i+1}"))
                    model.add(lktf.ReLU(name=f"relu-{i}_{c_i+1}"))
        #             model.add(self._obtain_activation(self.conv_activation, self.conv_activation_parameter))
            if 'b' in layers_i:
                model.add(lktf.BatchNormalization(name=f"batch-{i}"))
            if 'p' in layers_i:
                model.add(lktf.MaxPooling2D(pool_size=self.conv_pool_size, padding='same', name=f"max_pooling_2d-{i}"))
            if 'd' in layers_i:
                model.add(lktf.Dropout(self.conv_dropout, name=f"dropout-{i}"))

        model.add(lktf.Flatten(name='flatten'))

        for i, dense_layer_config in list(enumerate(self.dense_layer_array)):
            dense_layer_size_i, layers_i = dense_layer_config
            assert 'e' in layers_i

            if 'b' in layers_i:
                model.add(lktf.BatchNormalization(name=f"dense-batch-{i}"))

            model.add(lktf.Dense(
                dense_layer_size_i,
#                 kernel_regularizer=regularizers.L2(1e-3),
#                 activity_regularizer=regularizers.L2(1e-3),
                name=f"dense-{i}"
            ))
#             model.add(self._obtain_activation(self.dense_activation, self.dense_activation_parameter))
            model.add(lktf.ReLU(name=f"dense-relu-{i}"))

            if 'd' in layers_i:
                model.add(lktf.Dropout(self.dense_dropout, name=f"dense-dropout-{i}"))

        model.add(lktf.Dense(self.num_classes, activation='softmax', name='output'))

        model.compile(
            optimizer=self.optimizer,
            loss=self.loss,
            metrics=['accuracy'],
        )
        self.model = model

        return model

    def _obtain_activation(self, name: str, negative_slope: Union[int, NoneType] = None):
        if name == 'relu':
            return lktf.ReLU(negative_slope=0.0 if negative_slope is None else negative_slope)
        elif name == 'lrelu':
            return lktf.LeakyReLU(negative_slope=0.3 if negative_slope is None else negative_slope)

    def fit(self, features: pd.DataFrame, labels: pd.Series):
        assert (features.index == labels.index).all()
        assert self.file_path_column_name in features
        assert self.label_column_name == labels.name
        assert self.model is not None

        # ImageDataGenerator сам делает преобразование меток, если class_mode='categorical'
        # encoded_labels = pd.Series(
        #     self.one_hot_encoder.transform(labels.values.reshape(-1, 1)).toarray().tolist(),
        #     index=labels.index,
        #     name=self.label_column_name
        # )
        data_frame = pd.concat([features, labels], axis=1)
        display(data_frame.sample(10))
        display(np.unique(labels))

        image_data_generator = tkpi.ImageDataGenerator(
            rescale=1.0/255,
            validation_split=self.validation_split
        )
        train_generator = image_data_generator.flow_from_dataframe(
            dataframe=data_frame,
            x_col=self.file_path_column_name,
            y_col=self.label_column_name,
            color_mode="rgb",
            class_mode="categorical",
            target_size=(self.input_shape[0], self.input_shape[1]),
            batch_size=self.batch_size,
            seed=137,
            suffle=True,
            subset='training'
        )
        validation_generator = image_data_generator.flow_from_dataframe(
            dataframe=data_frame,
            x_col=self.file_path_column_name,
            y_col=self.label_column_name,
            color_mode="rgb",
            class_mode="categorical",
            target_size=(self.input_shape[0], self.input_shape[1]),
            batch_size=self.batch_size,
            seed=137,
            suffle=True,
            subset='validation'
        )

        result = self.model.fit(
            train_generator,
            epochs=self.epochs,
            validation_data=validation_generator,
        )
        return result

    def predict_proba_from_dataframe(self, features: pd.DataFrame):
        assert self.file_path_column_name in features
        image_data_generator = tkpi.ImageDataGenerator(rescale=1.0/255)
        test_generator = image_data_generator.flow_from_dataframe(
            dataframe=features,
            directory=None,
            x_col=self.file_path_column_name,
            y_col=None,
            batch_size=self.batch_size,
            seed=42,
            shuffle=False,
            color_mode="rgb",
            class_mode=None,
            target_size=(self.input_shape[0], self.input_shape[1]),
        )
        return self.model.predict(test_generator)
    
    def predict_proba_from_pil_image(self, image: pillow_images.Image):
        target_width = self.input_shape[1]
        target_height = self.input_shape[0]
        test_image = image.resize((target_width, target_height))
        test_image = test_image.convert('RGB')
        image_array = np.array(test_image, dtype='float64') / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        return self.model.predict(image_array)    

    def save(self, directory_path: paths.Path):
        assert directory_path is not None
        assert directory_path.is_dir()

        path_weights = directory_path / 'model.weights.h5'
        self.model.save_weights(path_weights, overwrite=True, save_format='h5')

        path_model = directory_path / 'model.tf'
        self.model.save(path_model, overwrite=True, save_format='tf')

        self_dictionary = vars(self).copy()
        self_dictionary.pop('model', None)
        self_dictionary.pop('optimizer', None)
        serialized_wrapper_json = json.dumps(self_dictionary)

        path_wrapper = directory_path / 'model.wrapper.json'
        with open(path_wrapper, 'w') as f:
            f.write(serialized_wrapper_json)

        path_model_archive = directory_path / 'model.zip'
        with zipfile.ZipFile(path_model_archive, 'w') as zip_reference:
            zip_reference.write(directory_path / 'model.tf', 'model.tf')
            zip_reference.write(directory_path / 'model.weights.h5', 'model.weights.h5')
            zip_reference.write(directory_path / 'model.wrapper.json', 'model.wrapper.json')

    @staticmethod
    def load(model_archive_path: paths.Path, extaction_directory_path: paths.Path):
        assert model_archive_path is not None
        assert model_archive_path.is_file()
        assert model_archive_path.suffix == '.zip'
        assert extaction_directory_path is not None
        assert extaction_directory_path.is_dir()

        archive_files = {
            'weights': 'model.weights.h5',
            'model': 'model.tf',
            'wrapper': 'model.wrapper.json',
        }

        path_model_archive = extaction_directory_path / 'model.zip'
        with zipfile.ZipFile(path_model_archive, 'r') as zip_reference:
            for item_name, archive_file_name in archive_files.items():
                assert archive_file_name in zip_reference.namelist()

        with zipfile.ZipFile(path_model_archive, 'r') as zip_reference:
            zip_reference.extractall(extaction_directory_path)

        model = mktf.load_model(extaction_directory_path / archive_files['model'])
        model.load_weights(extaction_directory_path / archive_files['weights'])

        with open(extaction_directory_path / archive_files['wrapper'], 'r') as f:
            wrapper_dict = json.load(f)

        wrapper = CNNCustomClassifier(**wrapper_dict)
        wrapper.model = model
        return wrapper

