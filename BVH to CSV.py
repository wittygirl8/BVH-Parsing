#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os

# Initialize variables for bone names and frame count
bone_name = []
frame_count = 0

# Check if the file name was passed as an argument
# if len(sys.argv) != 2:
#     print('Usage: python bvhparser.py path/to/filename')
#     sys.exit()

# Set the input file name (replace with sys.argv[1] for command-line argument)
filename = "C:/Users/Dell/Downloads/BVHExtract.bvh"

# Open the input file and read its contents into a list of words
with open(filename, "r") as f:
    words = f.read().split()

    # Initialize a flag to indicate whether the next word should be added to the bone name
    add_next = False

    # Iterate over the words in the file
    for word in words:
        # If the previous word was "ROOT" or "JOINT", set the flag to add the next word to the bone name
        if add_next:
            bone_name += [f"{word}{suffix}" for suffix in ("Xpos", "Ypos", "Zpos", "Yrot", "Xrot", "Zrot")]
            add_next = False
        
        # Check if the current word is "ROOT" or "JOINT"
        if word in ("ROOT", "JOINT"):
            add_next = True
        
        # Check if the current word is "Frames" and set the frame count accordingly
        if word == "Frames:":
            frame_count = int(words[words.index(word) + 1])
        
        # Check if the current word is "Time" and remove the unnecessary words from the list
        if word == "Time:":
            words = words[words.index(word) + 2:]
            break

# Initialize a list of empty lists to store the data for each bone
data = [[] for _ in range(len(bone_name))]
size = len(bone_name)

# Iterate over the remaining words and add them to the data list for the corresponding bone
for count, word in enumerate(words):
    data[count % size].append(word)

# Set the output file name based on the input file name
output_file = os.path.splitext(filename)[0] + ".csv"

# Open the output file and write the header and data for each bone
with open(output_file, "w") as f:
    # Write the header row with the frame numbers
    f.write(f"Frames,{','.join(str(i) for i in range(1, frame_count + 1))}\n")

    # Iterate over the bone names and their corresponding data lists and write them to the file
    for name, values in zip(bone_name, data):
        f.write(f"{name},{','.join(values)}\n")

