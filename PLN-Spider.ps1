# Get the current username
$current_username = $env:USERNAME

# Create a file path using the current username
$file_path = "C:\Users\$current_username\Documents\PLN-Spider"

# Use the file_path as needed
cd $file_path
py main.py