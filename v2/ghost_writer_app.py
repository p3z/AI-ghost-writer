
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from agents import generate_content, generate_ideas, basic_query, pick_ideas, generate_titles, convert_to_cs_list, generate_bookends, string_to_list
open_ai_key = os.environ.get("OPENAI_API_KEY") # this variable name is intentional, dont change it

# when encountering python interpreter conflicts, ensure the package is being installed in the dir of the correct interpreter with this: python3 -m pip install MODULE_NAME, and then run the files with this: python3 -m COMMAND_TO_RUN

######################################

FILE_DIVIDER = "\n\n==============\n\n"

st.set_page_config(page_title="Ghost writer v2", page_icon=":robot:")
st.header("Ghost writer v2")
st.markdown("---")

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




def handle_radio_change(selected_option):
    if selected_option == "ideas":
        ideas_ui()
    elif selected_option == "narrow down ideas":
        narrow_idea_scope_ui()
    elif selected_option == "topics":
        topic_ui()
    elif selected_option == "book outline":
        book_outline_ui()
    elif selected_option == "book title":
        book_title_ui()
    elif selected_option == "bookend":
        bookend_ui()
    elif selected_option == "outlines":
        show_outlines()
    elif selected_option == "content":
        show_content()


    elif selected_option == "test":
        test()


# parse through the book outline and build chapter outlines
def parse_outline():
    outline = read_from_file("book_outline.txt")
    outline_list = convert_to_cs_list(outline) # because converting directly to python list is a pain
    parsed_list = outline_list['response']
    chapter_list = string_to_list(parsed_list)

    test_audience = "gen z authors"
    clarifications = " Choose 5 key points for each chapter MAXIMUM, focus on the most important points. Here's an example of the structure: "
    clarifications += "\n1. Understanding the Essence of World-Building: Creating a Solid Foundation\n2. Imagining New Realms: Sparking Creativity and Igniting the Imagination\n3. Setting the Stage: Establishing a Vivid and Engaging Setting\n4. Developing a Unique and Consistent Magic System: Tapping into the Extraordinary\n5. Creating Culture and Society: Shaping Believable Communities within Your World\n\n"

    chapter_counter = 1
    for chapter_title in chapter_list:              
        generate_chapter_outline(outline, chapter_title, test_audience, clarifications, chapter_counter)
        chapter_counter += 1

def generate_chapter_outline(book_outline, chapter_title, audience, clarifications, chapter_counter):
    content_type = "a list of topics to cover in this chapter. NEVER output the chapter title or any other information, notes or suggestions. Literally just print the list with no context."
    content_type += " The chapter's title is " + chapter_title
    full_clarifications = "This is the entire book outline: \n\n" + book_outline + "\n\n Make sure NOT to duplicate content from this outline. Other than that, the outline is to be ignored! REMEMBER, the final list should ONLY contain topics for THIS chapter, this is VITAL! \n\n" + clarifications


    response = generate_content("author", content_type, chapter_title, audience, full_clarifications) 
    st.subheader(chapter_title)
    st.write(response['response'])
    st.write("===========================")

    file_name = "chapter_ " + str(chapter_counter) + '_outline.txt'
    # theres a bug in here somewhere, the first chapter always saves multiple times... (or was i just failing to delete the file each time... cos it appends to it doesnt it)
    save_to_file("output/ghost_writer/" + file_name, response['response'])
    save_to_file("output/ghost_writer/" + file_name, "\n\n================================\n\nPrompt:\n\n")
    save_to_file("output/ghost_writer/" + file_name, response['prompt'])


def test():
    parse_outline()
    




def ideas_ui():
    submit = st.button("Generate ideas")
    if submit:
        topic_exclusions = ["self help", "medicine and physical health", "business", "personal growth", "productivity"]
        idea_prompt = generate_ideas(topic_exclusions)

        context = read_from_file("brainstorm_ideas.txt")
        full_context = "Ideas that we've already covered. It's vital that we dont repeat ideas, each should be completely unique and separate from the others: \n\n" + context

        


        response = basic_query(idea_prompt, full_context)
        st.subheader("Full prompt:")
        st.write(response['prompt'])

        st.subheader("Answer:")
        st.write(response['response'])
        

        
        save_to_file("brainstorm_ideas.txt", response['response'], FILE_DIVIDER)

def narrow_idea_scope_ui():
    ideas = "Possible ideas: " + read_from_file("brainstorm_ideas.txt")
    narrowed_ideas_prompt = pick_ideas("3")

    submit = st.button("Pick ideas")
    if submit:

        response = basic_query(narrowed_ideas_prompt, ideas)

        st.subheader("Answer:")
        st.write(response['response'])

        st.subheader("Full prompt:")
        st.write(response['prompt'])

        

    




def topic_ui():
    st.markdown("#### Generate content ideas")
    selected_theme = st.text_input("Select a theme: ", key="theme")
    selected_audience = st.text_input("Describe your audience: ", key="audience")
    selected_clarifications = st.text_input("Additional thoughts: ", key="clarifications")
    submit = st.button('Generate')

    if submit:
        content_type = "a list of content ideas"
        response = generate_content("marketing manager", content_type, selected_theme, selected_audience, selected_clarifications)        
        st.subheader("Answer:")
        st.write(response['response'])

        # Write mode: 'w', Append or create: a+
        with open('brainstorm_topics.txt', 'a+') as file:
            file.write(response['response'])

def book_outline_ui():
    st.markdown("#### Generate book outline")
    selected_theme = st.text_input("Select a theme: ", key="theme")
    selected_audience = st.text_input("Describe your audience: ", key="audience")
    submit = st.button('Generate')

    if submit:
        content_type = "a book outline that lists chapter titles for a rounded out book. Don't include the word 'chapter'."
        response = generate_content("author", content_type, selected_theme, selected_audience)        
        st.subheader("Answer:")
        st.write(response['response'])

        # Write mode: 'w', Append or create: a+
        with open('book_outline.txt', 'a+') as file:
            file.write(response['response'])

def book_title_ui():
    st.markdown("#### Generate book title")
    outline = read_from_file("book_outline.txt")
    selected_audience = st.text_input("Describe your audience: ", key="audience")

    prompt = generate_titles(outline, selected_audience)

    submit = st.button('Generate potential book titles')

    if submit:
        response = response = basic_query(prompt)    
        st.subheader("Potential titles:")
        st.write(response['response'])

        # Write mode: 'w', Append or create: a+
        # with open('book_outline.txt', 'a+') as file:
        #     file.write(response)


def bookend_ui():
    st.markdown("#### Generate bookend (intro or conclusion)")
    outline = read_from_file("book_outline.txt")
    bookend_type = st.radio("Bookend type", ["introduction", "conclusion"])
    selected_audience = st.text_input("Describe your audience: ", key="audience")

    prompt = generate_bookends(outline, selected_audience, bookend_type)

    submit = st.button('Generate bookend')

    if submit:
        response = response = basic_query(prompt)    
        st.subheader("Introduction:")
        st.write(response['response'])

        # Write mode: 'w', Append or create: a+
        # with open('book_outline.txt', 'a+') as file:
        #     file.write(response)
    

def show_outlines():
    st.markdown("#### Generate outlines")
    st.write("Function for displaying outlines")

def show_content():
    st.markdown("#### Generate content")
    st.write("Function for displaying content")

# Create a radio button
selected_option = st.radio("What do you need?", ["ideas", "narrow down ideas", "topics", "book outline", "book title", "bookend", "outlines", "content", "test"])

# Run different functions based on the selected option
handle_radio_change(selected_option)
