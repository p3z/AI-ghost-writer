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
        print(f"The file '{file_path}' does not exist. Returning <empty string>")
        return ''
    except Exception as e:
        print(f"An error occurred: {e}. Returning <empty string>")
        return ''

# Converts comma-separated string into python list
def string_to_list(input_string):
   
    # Using the split method to separate elements based on commas
    elements = input_string.split(',')

    # Removing leading and trailing whitespaces from each element
    elements = [element.strip() for element in elements]

    return elements

# parse through the book outline and build chapter outlines
# def parse_outline():
#     outline = read_from_file("book_outline.txt")
#     outline_list = convert_to_cs_list(outline) # because converting directly to python list is a pain
#     parsed_list = outline_list['response']
#     chapter_list = string_to_list(parsed_list)

#     test_audience = "gen z authors"
#     clarifications = " Choose 5 key points for each chapter MAXIMUM, focus on the most important points. Here's an example of the structure: "
#     clarifications += "\n1. Understanding the Essence of World-Building: Creating a Solid Foundation\n2. Imagining New Realms: Sparking Creativity and Igniting the Imagination\n3. Setting the Stage: Establishing a Vivid and Engaging Setting\n4. Developing a Unique and Consistent Magic System: Tapping into the Extraordinary\n5. Creating Culture and Society: Shaping Believable Communities within Your World\n\n"

#     chapter_counter = 1
#     for chapter_title in chapter_list:              
#         generate_chapter_outline(outline, chapter_title, test_audience, clarifications, chapter_counter)
#         chapter_counter += 1

# def generate_chapter_outline(book_outline, chapter_title, audience, clarifications, chapter_counter):
#     content_type = "a list of topics to cover in this chapter. NEVER output the chapter title or any other information, notes or suggestions. Literally just print the list with no context."
#     content_type += " The chapter's title is " + chapter_title
#     full_clarifications = "This is the entire book outline: \n\n" + book_outline + "\n\n Make sure NOT to duplicate content from this outline. Other than that, the outline is to be ignored! REMEMBER, the final list should ONLY contain topics for THIS chapter, this is VITAL! \n\n" + clarifications


#     response = generate_content("author", content_type, chapter_title, audience, full_clarifications) 
#     st.subheader(chapter_title)
#     st.write(response['response'])
#     st.write("===========================")

#     file_name = "chapter_ " + str(chapter_counter) + '_outline.txt'
#     # theres a bug in here somewhere, the first chapter always saves multiple times... (or was i just failing to delete the file each time... cos it appends to it doesnt it)
#     save_to_file("output/ghost_writer/" + file_name, response['response'])
#     save_to_file("output/ghost_writer/" + file_name, "\n\n================================\n\nPrompt:\n\n")
#     save_to_file("output/ghost_writer/" + file_name, response['prompt'])