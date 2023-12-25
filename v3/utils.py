def save_to_file(filename, data, divider = ""):
        # Write mode: 'w', Append or create: a+
        with open(filename, 'a+') as file:
            file.write(data)
            file.write(divider)


# Returns contents of file
def read_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
            return contents
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

