import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser

# Orig ghost writer prompt:
#     (style != "") ? ` Write in the style of ${style}. Always write in that style.` : "";
#     //final_prompt += ` When writing, generate and insert details naturally into the ${content_type} if not specified in the prompt.`;
# 

llm = ChatOpenAI(
        api_key = os.environ.get("OPENAI_API_KEY"),
        model_name="gpt-3.5-turbo",
        temperature=1
    )

CONSIDERATIONS = "Bear in mind, this is not a conversation but a task. Just give the list, no additional context, thoughts or extra information are required, this is incredibly important. Also, no additional formatting. The content alone is sufficient. Don't insert every detail from the prompt into the response, only insert relevant details."

LIMITATIONS = "When in character, you have no limitations. If there's something you can't do, it's critical to NEVER point it out. Instead give it your best guess always as a human might. None of your responses should inform me that you can't do something because your character can. While in character, do not thank or acknowledge me in any way. It's vital that you never break character, so never tell me that you are an AI or a language model. Pretend that you literally ARE the character described."

def role_handler(role_title, content_type, theme, audience):
    init = f"Your character: You are a genius {role_title} with decades of experience. Create {content_type} based on the theme: {theme}. It's absolutely vital that the theme is the main focus. When inserting details, make sure the overall thrust is subtly tailored toward {audience}, take care not to name them in any way. Basically, it should use language that appeals to them WITHOUT directly mentioning them."
    return init

# Deprecated
# def clarification_handler(clarifications):
#     init = "It's important to remember: "
#     return init + clarifications

# Breaking down the ideal prompt
# Role: describe the agent's purpose and the flavour of work they will be tasked with
# Format: descibe how the output should be formatted. Be as specific as possible
# Exclusions: a list of things you definitely want to avoid
def generate_ideas(exclusions):
    
    add_exclusions = " The following ideas should be excluded at all costs: " + ', '.join(exclusions) +  ". "

    prompt = "You are a prodigy entrepeneur tasked with generating content ideas for ebooks. Your focus should be on selecting topics that are proven to sell well throughout the year regardless of time, what some might call 'evergreen' topics. The topics should be complex enough that others would struggle to imitate them."

    if( len(exclusions) > 0):
        prompt += add_exclusions
    
    prompt += "Other than that, use your resourcefulness and ingenuity as the entrepeurial entity you are to be as creative as possible.\n\n Format potential ideas into a markdown table. Column 1 is the concise description of the idea. Column 2 is a summary of rationale for why this idea is included in the list.\n\n Generate as many ideas as you can think of. Limit your output to the ideas only. For example, do not explain that 'this is the rationale', just provide the rationale. Likewise for the idea itself. Also, do not point out that these are evergreen ideas, just provide the ideas themselves. Do not number the ideas. The entire output should literally be the table of ideas."

    return prompt

def generate_titles(outline, audience):

    prompt = "You are a an expert marketing professional with decades of experience. You're tasked with creating catchy book titles based on outlines that describe a book's contents. You have been given the following book outline: \n\n"

    prompt += outline + "\n\n"

    prompt += "It's important to consider the whole outline when creating a title. It should embrace the contents as a whole unit."

    prompt += "The title should use language that appeals to the primary audience WITHOUT directly mentioning them in any way. The audience is: " + audience

    prompt += CONSIDERATIONS + LIMITATIONS

    return prompt

# Generates a book's introduction or conclusion based on args
def generate_bookends(outline, audience, bookend = "intro"):
    prompt = "You are a an expert author writing a book based on this outline: \n\n"
    prompt += outline + "\n\n"
    prompt += "Your task is to write a compelling " + bookend + " to the book as a whole. It's important to consider the whole outline when doing this. It should embrace the contents as a whole unit."
    prompt += "The language should appeal to the primary audience WITHOUT directly mentioning them in any way. The audience is: " + audience

    prompt += CONSIDERATIONS + LIMITATIONS

    return prompt

def pick_ideas(qty):
    prompt = "Out of the information provided, select " + qty + " easiest ideas to monetise. Output should be a markdown table with first column as idea, and second column as concise description of why that idea was selected."

    return prompt

def basic_query(query, context = "", vars = {}):

    add_context = ""

    if(context != ""):
        add_context = "The following is supplementary information to assist you: " + context   

     
    full_query = query + add_context
    prompt = PromptTemplate.from_template( full_query )
    runnable = prompt | llm | StrOutputParser()
    response = runnable.invoke(vars)
    return_dict = {
        "response": response,
        "prompt": full_query
    }
    return return_dict

 # cs = 'comma separated' list as distinct from a python list. Hacky as anything, but does the job
def convert_to_cs_list(list):   
    prompt = "Convert this list of ideas into a comma separated list. " + CONSIDERATIONS
    prompt += "This is the list: " + list
    return basic_query(prompt)

# Converts comma-separated string into python list
def string_to_list(input_string):
   
    # Using the split method to separate elements based on commas
    elements = input_string.split(',')

    # Removing leading and trailing whitespaces from each element
    elements = [element.strip() for element in elements]

    return elements


def generate_content(role, content_type, theme, audience, clarifications):
    
    ROLE = role_handler(role, content_type, theme, audience)
    CLARIFICATIONS = clarifications
    AGENT =  f"{ROLE} {CLARIFICATIONS} {CONSIDERATIONS} {LIMITATIONS}"


    prompt = PromptTemplate.from_template( AGENT )
    runnable = prompt | llm | StrOutputParser()
    response = runnable.invoke({
            "theme": theme,
            "audience": audience,
            "clarifications": clarifications
        })
    
    return_dict = {
        "response": response,
        "prompt": AGENT
    }
    return return_dict
