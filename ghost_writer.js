const express = require('express');
const app = express();
require('dotenv').config();
const bodyParser = require('body-parser');
app.use(bodyParser.json());

//app.use('/styles', express.static(__dirname + '/public'));


const { Configuration, OpenAIApi } = require("openai");
const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
});

const openai = new OpenAIApi(configuration);

app.get('/', (req, res) => {
  //res.send("Ghost writer prototype root")
  res.sendFile(__dirname + '/index.html');
});

app.get('/test', (req, res) => {
  res.send("Simple test route")
});


app.post('/writer', async (req, res) => {
  
  let response_obj = {};
  let user_data = req.body;

  
  // Current potential params: sentiment, length, genre, summary

  //TODO: ADD A WAY TO ENSURE THAT IF THERE IS MISSING INPUT THEN FORM WILL STILL WORK

  let acceptable_params = [
    'title', 'page', 'prologue', 'epilogue', 'blurb', 'tagline', 'summary', 'review',
  ]

  if(!acceptable_params.includes(user_data.content_type) ||user_data.content_type == ""){   
    res.send({ error: "Not acceptable input" });  // Prevent arbitrary inputs
  }

  let handle_plural_types = (user_data.qty == 1) ? user_data.content_type : user_data.content_type + "s"; // Dont worry about spelling errors, gpt is pretty much smart enough to know what you meant  

  response_obj.qty = user_data.qty;
  response_obj.content_type = user_data.content_type;
  response_obj.sentiment = user_data.sentiment;
  response_obj.length = user_data.length;
  response_obj.genre = user_data.genre;
  response_obj.summary = user_data.summary;

  let prompt_body = `Using the information expressed in the following json object, generate ${user_data.qty} creative ${handle_plural_types} for a book. They should all be completely different. Return the data as an html ordered list:\n`;
  
  // Reduce the user_data object down to the data that will be used to construct the body content
  const excludedKeys = ['qty', 'content_type'];
  
  let new_req_obj = {};
  
  Object.keys(user_data).forEach((key, i) => {
    let orig_val = Object.values(user_data)[i];

    if( !excludedKeys.includes(key)){
      new_req_obj[key] = orig_val;
    }    
    
  });

  prompt_body += JSON.stringify(new_req_obj);
  
  
    
  let args = {
      model: "text-davinci-003",  
      //prompt: "Say hello", // This is just a test line in case something goes wrong with the line below
      prompt: prompt_body,
      temperature: 1,
      max_tokens: 2086,
      top_p: 1,
      frequency_penalty: 0,
      presence_penalty: 0,
  };

  
  const response = await openai.createCompletion(args);
  const answer = response.data.choices[0].text;

  // Now parse the returned payload



  response_obj.answer = answer;

  res.send( response_obj );
  
});

app.get('*', (req, res) => {
  //res.status(404).send('404 Not Found');
  res.send("Ghost writer prototype (Catch all)")
});


// Listen for requests
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});