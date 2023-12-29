import os
from datetime import datetime
current_datetime = datetime.now()
date_time_string = current_datetime.strftime("%Y-%m-%d-%H_%M_%S")

from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager, config_list_from_json
from utils import save_to_file, read_from_file, string_to_list

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
llm_config={"config_list": config_list}

output_divider = "===================================="
output_folder = "ghost_writer_output"

# Create the folder if it doesn't exist
if not os.path.exists( output_folder ):
    os.makedirs( output_folder ) 

class Topic_focus_compiler:
    def __init__(self, audience, voice, purpose, exceptions):
        self.audience = audience
        self.voice = voice
        self.purpose = purpose
        self.exceptions = exceptions

    def brainstorm_ideas(self):
        return f"You are a master consultant whose focus is content creation. Your job is to generate a list of as many ideas as possible for {self.purpose} that will appeal to {self.audience}. \n\n The ideas should all be on distinctly different topics, however they can be on any topic besides those listed here: {self.exceptions}. \n\n The focus of the idea can be any aspect of the topic itself, or even of a related topic. For example, if a topic is food, here are some possible ideas:\n - the history of a particular dish\n- cultural differences in cuisine\n- etiquette of dining\n\n You are not limited to these examples, they are just for illustration. Basically, use your imagination and experience as the master consultant you are.\n\n The ideas should be formatted as a list. Besides the list of ideas, no other other output should be returned (no explanations, no context, no suggestions, nothing).\n\n To reiterate the output should look like this example: ['idea', 'idea', 'idea'] with no additional information."
    
    def topic_finaliser(self, idea_list, qty = 3):
        return f"Out of the list of topics provided, select {qty} of the easiest ideas to monetise. Output should be a markdown table with first column as the idea, and second column as concise description of why that idea was selected. This is the list of topics: {idea_list}"

    def focus_generator(self, selected_topic):
        return f"Given the topic: '{selected_topic}' , what niche topic could this book focus on? \n\n Your response should just be the niche with no further explanation or context."
    

# Initialise settings
target_audience = "gen x authors"
spoken_voice = "angry"
content_purpose = "a new book"
exceptions = "[self help, medicine and physical health, business, personal growth, productivity]"
chosen_topic = "Exploring the world of virtual reality gaming"

# Initialise the class
compiler_instance = Topic_focus_compiler(target_audience, spoken_voice, content_purpose, exceptions)

# Prepare the prompts


# focus_prompt = compiler_instance.focus_generator(selected_topic=chosen_topic)

# init autogen agents
# user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})
user_proxy = UserProxyAgent(
   name="user_proxy",
   code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
   human_input_mode="TERMINATE"
)

idea_consultant = AssistantAgent(
    name="idea_consultant",
    system_message=compiler_instance.brainstorm_ideas(),
    llm_config=llm_config
)

# idea_list = read_from_file(output_folder + '/ideas.txt')
# select_ideas_prompt = compiler_instance.topic_finaliser(idea_list=idea_list) # defaults to top 3 ideas

idea_selector = AssistantAgent(
    name="idea_selector",
    system_message="Picking the top 3 ideas.",
    llm_config=llm_config
)


# Sent to autogen
groupchat = GroupChat(agents=[user_proxy, idea_consultant, idea_selector], messages=[], max_round=12)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
user_proxy.initiate_chat(manager, message="Generate some ideas.")



# user_proxy.initiate_chat(assistant, message=idea_prompt)
# agent_response = user_proxy.last_message(assistant)["content"]
# #idea_file_name = output_folder + '/ideas_' + date_time_string + ".txt"
# idea_file_name = output_folder + '/ideas.txt'
# save_to_file(idea_file_name, agent_response)