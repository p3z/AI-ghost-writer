# Orig ghost writer prompt:
#     (style != "") ? ` Write in the style of ${style}. Always write in that style.` : "";
#     //final_prompt += ` When writing, generate and insert details naturally into the ${content_type} if not specified in the prompt.`;
# 

CONSIDERATIONS = "Bear in mind, this is not a conversation but a task. Just give the list, no additional context, thoughts or extra information are required, this is incredibly important. Also, no additional formatting. The content alone is sufficient. Don't insert every detail from the prompt into the response, only insert relevant details."

LIMITATIONS = "When in character, you have no limitations. If there's something you can't do, it's critical to NEVER point it out. Instead give it your best guess always as a human might. None of your responses should inform me that you can't do something because your character can. While in character, do not thank or acknowledge me in any way. It's vital that you never break character, so never tell me that you are an AI or a language model. Pretend that you literally ARE the character described."

def generic_role(role_title, content_type, theme, audience):
    init = f"Your character: You are a genius {role_title} with decades of experience. Create {content_type} based on the theme: '{theme}'. It's absolutely vital that the theme is the main focus. When inserting details, make sure the overall thrust is subtly tailored toward {audience}, take care not to name them in any way. Basically, it should use language that appeals to them WITHOUT directly mentioning them."
    return init



def generate_ideas(exclusions):
    
    add_exclusions = " The following ideas should be excluded at all costs: " + ', '.join(exclusions) +  ". "

    prompt = "You are a prodigy entrepeneur tasked with generating content ideas for ebooks. Your focus should be on selecting topics that are proven to sell well throughout the year regardless of time, what some might call 'evergreen' topics. The topics should be complex enough that others would struggle to imitate them."

    if( len(exclusions) > 0):
        prompt += add_exclusions
    
    prompt += "Other than that, use your resourcefulness and ingenuity as the entrepeurial entity you are to be as creative as possible.\n\n Format potential ideas into a markdown table. Column 1 is the concise description of the idea. Column 2 is a summary of rationale for why this idea is included in the list.\n\n Generate as many ideas as you can think of. Limit your output to the ideas only. For example, do not explain that 'this is the rationale', just provide the rationale. Likewise for the idea itself. Also, do not point out that these are evergreen ideas, just provide the ideas themselves. Do not number the ideas. The entire output should literally be the table of ideas with no additional comment. Just return the table, nothing more."

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


