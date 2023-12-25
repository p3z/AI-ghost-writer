const express = require('express');
const app = express();
require('dotenv').config();
const bodyParser = require('body-parser');
app.use(bodyParser.json());

//app.use('/styles', express.static(__dirname + '/public'));
const { init_DAN } = require('./prompts/general');


const { Configuration, OpenAIApi } = require("openai");
const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
});

const is_dev = process.env.NODE_ENV ?? false;
// todo: use this to indicate in the view's title if is live or prod at a glance


// Ensure users cant repurpose form
const acceptable_params = [
  'title', 'chapter', 'prologue', 'epilogue', 'blurb', 'tagline', 'topics', 'review',
]


const openai = new OpenAIApi(configuration);

app.get('/', (req, res) => {
  //res.send("Ghost writer prototype root")
  res.sendFile(__dirname + '/index.html');
});

app.get('/test', (req, res) => {
  res.send("Simple test route")
});


// Returns a duplicate object of the original object (any 'removals' that matched keys of that original object will have been removed)
function remove_keys_from_obj(orig_obj, removals = []){

     let new_obj = {};
     
     Object.keys(orig_obj).forEach((key, i) => {
       let orig_val = Object.values(orig_obj)[i];
   
       if( !removals.includes(key) ){
        new_obj[key] = orig_val;
       }    
       
     });
     

     return new_obj;

}



function handle_prompt(prompt_obj){
  
    let {
      qty, content_type, sentiment, style, topics, audience
    } = prompt_obj;
    

    let final_prompt = init_DAN();
    final_prompt += `Generate ${qty}  ${content_type}${(qty > 1) ? "s" : ""} on the topic of "${topics}".`;
    final_prompt += (style != "") ? ` Write in the style of ${style}. Always write in that style.` : "";
    final_prompt += (sentiment != "") ? ` Make sure that the tone of voice is ${sentiment}.` : "";
    //final_prompt += ` When writing, generate and insert details naturally into the ${content_type} if not specified in the prompt.`;
    //final_prompt += ` Do not insert every detail from the prompt into the response, only insert relevant details.`;
    // final_prompt += ` When inserting details, use your own words but make sure the overall thrust is subtly tailored toward ${audience} without naming them.`;
    
    
    return final_prompt;
    


  
    // let default_prompt = `Using the information expressed in the following json object, generate ${qty} creative ${content_type}${(is_plural) ? "s" : ""} for a book. ${(qty > 1) ? "They should all be completely different. " : ""}Return the data as an html ordered list:\n`;
    

}


app.post('/writer', async (req, res) => {
  
  let response_obj = {};
  let user_data_obj = req.body;

  if(!acceptable_params.includes(user_data_obj.content_type)){   
    res.send({ error: "Not acceptable input" });  // Prevent arbitrary inputs
  }

  

  // Add user settings to response object for troubleshooting
  response_obj.qty = user_data_obj.qty;
  response_obj.content_type = user_data_obj.content_type;

  let prompt_obj = remove_keys_from_obj(user_data_obj); // Reduce data object down to what will be used to construct the body content
  
  let prompt_body = handle_prompt(prompt_obj);
  
  
  // Now submit the request to openAI
  let args = {
      model: "text-davinci-003",  
      //prompt: JSON.stringify({test: "Say hello"}), // This is just a test line in case something goes wrong with the line below
      prompt: JSON.stringify(prompt_body),
      temperature: 1,
      max_tokens: 2086,
      top_p: 1,
      frequency_penalty: 0,
      presence_penalty: 0,
  };
  

  try {
    let response = await openai.createCompletion(args);   
     // Now parse the returned payload
    response_obj.answer = response.data.choices[0].text;
    response_obj.json_request = prompt_obj;
    response_obj.prompt_body = prompt_body; 
  }
  catch(err) {
    console.log("Error with API");
    response_obj.error = err
  }
  
   res.send( response_obj );
  
});

app.get('*', (req, res) => {
  //res.status(404).send('404 Not Found');
  res.send("Not a valid GhostWriter route")
});


// Listen for requests
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});