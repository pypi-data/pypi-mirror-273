from webflask import functions

# Display available files
functions.display_files()

# Ask the user to select a file
file_index = int(input("Enter the number of the file you want to copy: "))

# Copy the selected file to the current directory
functions.copy_file(file_index)
