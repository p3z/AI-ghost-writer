const express = require('express');
const app = express();
require('dotenv').config();
const bodyParser = require('body-parser');
app.use(bodyParser.json());

const { Configuration, OpenAIApi } = require("openai");
const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
});

const openai = new OpenAIApi(configuration);

app.get('/', (req, res) => {
  //res.send("Ghost writer prototype root")
  res.sendFile(__dirname + '/index.html');
});


app.post('/book/:qty/:content_type', async (req, res) => {

  console.log("Post route visited")

  let { qty = 1, content_type = "" } = req.params;
  let user_args = JSON.stringify(req.query); 
  // Current potential params: sentiment, length, genre, summary

  let acceptable_params = [
    'title', 'page', 'prologue', 'epilogue', 'blurb', 'tagline', 'summary', 'review',
  ]

  if(!acceptable_params.includes(content_type) || content_type == ""){   
    res.send({ error: "Not acceptable input" });  // Prevent arbitrary inputs
  }

  let handle_plural_types = (qty == 1) ? content_type : content_type + "s"; // Dont worry about spelling errors, gpt is pretty much smart enough to know what you meant

  let prompt_body = `Using the information expressed in the following json object, generate ${qty} creative ${handle_plural_types} for a book. They should all be completely different\n ${user_args}`;

  // console.log("Generated prompt body")
  // console.log(prompt_body)
  
    
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

  console.log("All available options:")
 // console.log(response.data.choices)

  res.send({ answer });
});

app.get('*', (req, res) => {
  //res.status(404).send('404 Not Found');
  res.send("Ghost writer prototype")
});


// Listen for requests
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});