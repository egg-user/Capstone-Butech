import urllib.request
import tensorflow as tf
from keras_preprocessing.image import ImageDataGenerator
from keras import Model
from keras.optimizers import RMSprop
#from keras.constraints import unit_norm
from keras import layers
from keras.applications.mobilenet_v2 import MobileNetV2

physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

pre_trained_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)

last_layer =  pre_trained_model.get_layer('out_relu')

#Ganti jadi path sendiri
Training_Dir = 'D:/Documents/Capstone/FruitDataset/training/'
Validation_Dir = 'D:/Documents/Capstone/FruitDataset/validation/'

def train_val_generators(Training_Dir, Validation_Dir):
    train_datagen = ImageDataGenerator(rescale=1. / 255,
                                       rotation_range=40,
                                       width_shift_range=0.2,
                                       height_shift_range=0.2,
                                       shear_range=0.2,
                                       zoom_range=0.2,
                                       horizontal_flip=True,
                                       fill_mode='nearest')

    train_generator = train_datagen.flow_from_directory(directory=Training_Dir,
                                                        batch_size=20,
                                                        class_mode='categorical',
                                                        target_size=(224, 224))

    validation_datagen = ImageDataGenerator(rescale=1. / 255)

    validation_generator = validation_datagen.flow_from_directory(directory=Validation_Dir,
                                                                  batch_size=20,
                                                                  class_mode='categorical',
                                                                  target_size=(224, 224))
    return train_generator, validation_generator

train_generator, validation_generator = train_val_generators(Training_Dir, Validation_Dir)

x = layers.Flatten()(last_layer.output)
#x = layers.Dense(10, 
#                 activation='relu',
#                 kernel_regularizer='l2',
#                 kernel_initializer='random_normal',
#                # kernel_constraint=unit_norm(),
#                 bias_initializer='zeros')(x)
x = layers.Dropout(0.5)(x)
x = layers.Dense(10, activation='softmax')(x)

model = Model(inputs=pre_trained_model.input, outputs=x)

model.compile(
    optimizer=RMSprop(learning_rate=4.999999873689376e-05),
    loss=tf.keras.losses.CategoricalCrossentropy(),
    metrics=['accuracy'])

#class myCallback(tf.keras.callbacks.Callback):
#  def on_epoch_end(self, epoch, logs={}):
#    if(logs.get('val_accuracy')>0.9):
#      print("\nReached 90% validation accuracy so cancelling training!")
#      self.model.stop_training = True
#
#callbacks = myCallback()

callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
lr_reduction = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', patience=5, verbose=1, factor=0.5,
                                                        min_lr=0.00001)

history = model.fit(
    train_generator,
    epochs=10,
    verbose=1,
    validation_data=validation_generator,
    callbacks=[callback, lr_reduction])

#Export the model
BuTect_Saved_Model = 'butect_saved_model'
tf.saved_model.save(model, BuTect_Saved_Model)
loaded = tf.saved_model.load(BuTect_Saved_Model)

print(list(loaded.signatures.keys()))
infer = loaded.signatures["serving_default"]
print(infer.structured_input_signature)
print(infer.structured_outputs)

#Convert to TFLite
converter = tf.lite.TFLiteConverter.from_saved_model(BuTect_Saved_Model)
converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_SIZE]
tflite_model = converter.convert()

tflite_model_file = 'converted_model.tflite'

with open(tflite_model_file, "wb") as f:
    f.write(tflite_model)
