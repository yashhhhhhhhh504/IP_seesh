import pickle

# Load the .pkl file
with open('file_list.pkl', 'rb') as f:
    file_list = pickle.load(f)

# Print the contents
print("Contents of the .pkl file:")
for file in file_list:
    print(file)
