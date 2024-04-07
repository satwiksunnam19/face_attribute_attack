import os
import shutil

# Path to the main folder
main_folder1 = './output1'
main_folder2 = './output2'

# List all folders in the main folders
folders1 = [f for f in os.listdir(main_folder1) if os.path.isdir(os.path.join(main_folder1, f))]
folders2 = [f for f in os.listdir(main_folder2) if os.path.isdir(os.path.join(main_folder2, f))]

# Split the list into two halves
half_len_1 = len(folders1)
folder1_train = folders1[:half_len_1]
folder1_test = folders1[half_len_1:]

half_len_2=len(folders2)
folder2_train = folders2[:half_len_2]
folder2_test = folders2[half_len_2:]

# Define the target directories
target_dir1_train = './data/train/real'
target_dir1_test = './data/test/real'

target_dir2_train = './data/train/fake'
target_dir2_test = './data/test/fake'

# Create new folders
os.makedirs(target_dir1_train, exist_ok=True)
os.makedirs(target_dir1_test, exist_ok=True)
os.makedirs(target_dir2_train, exist_ok=True)
os.makedirs(target_dir2_test, exist_ok=True)

# Copy contents of folders to new folders
for folder in folder1_train:
    source = os.path.join(main_folder1, folder)
    destination = os.path.join(target_dir1_train, folder)
    shutil.copytree(source, destination)

for folder in folder1_test:
    source = os.path.join(main_folder1, folder)
    destination = os.path.join(target_dir1_test, folder)
    shutil.copytree(source, destination)

for folder in folder2_train:
    source = os.path.join(main_folder2, folder)
    destination = os.path.join(target_dir2_train, folder)
    shutil.copytree(source, destination)

for folder in folder2_test:
    source = os.path.join(main_folder2, folder)
    destination = os.path.join(target_dir2_test, folder)
    shutil.copytree(source, destination)

print("Folders copied successfully.")
