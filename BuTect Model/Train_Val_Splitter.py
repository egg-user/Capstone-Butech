import os
import random
import shutil
from shutil import copyfile

#Ganti jadi path sendiri
#WARNING: JANGAN KE FOLDER YG UDH ADA ISINYA, NANTI DIGANTI SEMUA
root_dir = 'D:/Documents/Capstone/FruitDataset'
if os.path.exists(root_dir):
  shutil.rmtree(root_dir)

#10 Kategori
def create_train_val_dirs(root_path):
  subdirs = ['training', 'validation']
  categories = ['Apple_Bad', 'Apple_Good', 'Banana_Bad', 'Banana_Good', 'Guava_Bad', 'Guava_Good', 'Lime_Bad', 'Lime_Good',
                'Orange_Bad', 'Orange_Good']
  for subdir in subdirs:
      for category in categories:
          new_path = os.path.join(root_path, subdir, category)
          os.makedirs(new_path, exist_ok=True)
  pass

try:
    create_train_val_dirs(root_path=root_dir)
except FileExistsError:
    print("You should not be seeing this since the upper directory is removed beforehand")

for rootdir, dirs, files in os.walk(root_dir):
  for subdir in dirs:
      print(os.path.join(rootdir, subdir))
def split_data(SOURCE_DIR, TRAINING_DIR, VALIDATION_DIR, SPLIT_SIZE):
   files = os.listdir(SOURCE_DIR)
   files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
   for file in files:
       if os.path.getsize(os.path.join(SOURCE_DIR, file)) == 0:
           print(f"{file} is zero length, so ignoring.")
           files.remove(file)
       split_size = int(len(files) * SPLIT_SIZE)
       train_files = files[:split_size]
       val_files = files[split_size:]
   for file in train_files:
       shutil.copy(os.path.join(SOURCE_DIR, file), TRAINING_DIR)
   for file in val_files:
       shutil.copy(os.path.join(SOURCE_DIR, file), VALIDATION_DIR)
   pass

#Ganti jadi path sendiri
Apple_Bad_Source_Dir = 'D:/Documents/Capstone/ImageDataset(Ori)/Bad Quality_Fruits/Apple_Bad/'
Banana_Bad_Source_Dir = 'D:/Documents/Capstone/ImageDataset(Ori)/Bad Quality_Fruits/Banana_Bad/'
Guava_Bad_Source_Dir = 'D:/Documents/Capstone/ImageDataset(Ori)/Bad Quality_Fruits/Guava_Bad/'
Lime_Bad_Source_Dir = 'D:/Documents/Capstone/ImageDataset(Ori)/Bad Quality_Fruits/Lime_Bad/'
Orange_Bad_Source_Dir = 'D:/Documents/Capstone/ImageDataset(Ori)/Bad Quality_Fruits/Orange_Bad/'
Apple_Good_Source_Dir = 'D:/Documents/Capstone/ImageDataset(Ori)/Good Quality_Fruits/Apple_Good/'
Banana_Good_Source_Dir = 'D:/Documents/Capstone/ImageDataset(Ori)/Good Quality_Fruits/Banana_Good/'
Guava_Good_Source_Dir = 'D:/Documents/Capstone/ImageDataset(Ori)/Good Quality_Fruits/Guava_Good/'
Lime_Good_Source_Dir = 'D:/Documents/Capstone/ImageDataset(Ori)/Good Quality_Fruits/Lime_Good/'
Orange_Good_Source_Dir = 'D:/Documents/Capstone/ImageDataset(Ori)/Good Quality_Fruits/Orange_Good/'

Training_Dir = 'D:/Documents/Capstone/FruitDataset/training/'
Validation_Dir = 'D:/Documents/Capstone/FruitDataset/validation/'

Training_Apple_Bad_Dir = os.path.join(Training_Dir, 'Apple_Bad/')
Training_Banana_Bad_Dir = os.path.join(Training_Dir, 'Banana_Bad/')
Training_Guava_Bad_Dir = os.path.join(Training_Dir, 'Guava_Bad/')
Training_Lime_Bad_Dir = os.path.join(Training_Dir, 'Lime_Bad/')
Training_Orange_Bad_Dir = os.path.join(Training_Dir, 'Orange_Bad/')
Training_Apple_Good_Dir = os.path.join(Training_Dir, 'Apple_Good/')
Training_Banana_Good_Dir = os.path.join(Training_Dir, 'Banana_Good/')
Training_Guava_Good_Dir = os.path.join(Training_Dir, 'Guava_Good/')
Training_Lime_Good_Dir = os.path.join(Training_Dir, 'Lime_Good/')
Training_Orange_Good_Dir = os.path.join(Training_Dir, 'Orange_Good/')
Validation_Apple_Bad_Dir = os.path.join(Validation_Dir, 'Apple_Bad/')
Validation_Banana_Bad_Dir = os.path.join(Validation_Dir, 'Banana_Bad/')
Validation_Guava_Bad_Dir = os.path.join(Validation_Dir, 'Guava_Bad/')
Validation_Lime_Bad_Dir = os.path.join(Validation_Dir, 'Lime_Bad/')
Validation_Orange_Bad_Dir = os.path.join(Validation_Dir, 'Orange_Bad/')
Validation_Apple_Good_Dir = os.path.join(Validation_Dir, 'Apple_Good/')
Validation_Banana_Good_Dir = os.path.join(Validation_Dir, 'Banana_Good/')
Validation_Guava_Good_Dir = os.path.join(Validation_Dir, 'Guava_Good/')
Validation_Lime_Good_Dir = os.path.join(Validation_Dir, 'Lime_Good/')
Validation_Orange_Good_Dir = os.path.join(Validation_Dir, 'Orange_Good/')

split_size = .8

split_data(Apple_Bad_Source_Dir, Training_Apple_Bad_Dir, Validation_Apple_Bad_Dir, split_size)
split_data(Banana_Bad_Source_Dir, Training_Banana_Bad_Dir, Validation_Banana_Bad_Dir, split_size)
split_data(Guava_Bad_Source_Dir, Training_Guava_Bad_Dir, Validation_Guava_Bad_Dir, split_size)
split_data(Lime_Bad_Source_Dir, Training_Lime_Bad_Dir, Validation_Lime_Bad_Dir, split_size)
split_data(Orange_Bad_Source_Dir, Training_Orange_Bad_Dir, Validation_Orange_Bad_Dir, split_size)
split_data(Apple_Good_Source_Dir, Training_Apple_Good_Dir, Validation_Apple_Good_Dir, split_size)
split_data(Banana_Good_Source_Dir, Training_Banana_Good_Dir, Validation_Banana_Good_Dir, split_size)
split_data(Guava_Good_Source_Dir, Training_Guava_Good_Dir, Validation_Guava_Good_Dir, split_size)
split_data(Lime_Good_Source_Dir, Training_Lime_Good_Dir, Validation_Lime_Good_Dir, split_size)
split_data(Orange_Good_Source_Dir, Training_Orange_Good_Dir, Validation_Orange_Good_Dir, split_size)

#List berapa gambar di tiap folder
print(f"{len(os.listdir(Training_Apple_Bad_Dir))}")
print(f"{len(os.listdir(Training_Banana_Bad_Dir))}")
print(f"{len(os.listdir(Training_Guava_Bad_Dir))}")
print(f"{len(os.listdir(Training_Lime_Bad_Dir))}")
print(f"{len(os.listdir(Training_Orange_Bad_Dir))}")
print(f"{len(os.listdir(Training_Apple_Good_Dir))}")
print(f"{len(os.listdir(Training_Banana_Good_Dir))}")
print(f"{len(os.listdir(Training_Guava_Good_Dir))}")
print(f"{len(os.listdir(Training_Lime_Good_Dir))}")
print(f"{len(os.listdir(Training_Orange_Good_Dir))}")

print(f"{len(os.listdir(Validation_Apple_Bad_Dir))}")
print(f"{len(os.listdir(Validation_Banana_Bad_Dir))}")
print(f"{len(os.listdir(Validation_Guava_Bad_Dir))}")
print(f"{len(os.listdir(Validation_Lime_Bad_Dir))}")
print(f"{len(os.listdir(Validation_Orange_Bad_Dir))}")
print(f"{len(os.listdir(Validation_Apple_Good_Dir))}")
print(f"{len(os.listdir(Validation_Banana_Good_Dir))}")
print(f"{len(os.listdir(Validation_Guava_Good_Dir))}")
print(f"{len(os.listdir(Validation_Lime_Good_Dir))}")
print(f"{len(os.listdir(Validation_Orange_Good_Dir))}")