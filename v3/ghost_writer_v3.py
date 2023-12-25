from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from v2_fns import generic_role, generate_ideas, pick_ideas, generate_titles, generate_bookends, string_to_list
from utils import save_to_file, read_from_file

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})
user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})

################################################################################

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


################################################################################
role_title="author"
theme = ""
content_type = ""
audience = ""

ghost_writer_prompt = generic_role(role_title, content_type, theme, audience)
user_proxy.initiate_chat(assistant, message=ghost_writer_prompt)
