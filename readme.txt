### Development history

| version | approach |
| --- | --- | 
| 1 | Integrating API calls to Open AI's LLM models directly via ajax. Express app with custom html structure. | 
| 2 | Using langchain's more refined interface with a view to chaining LLM calls. StreamLit app for faster iteration. |
| 3 | Using AutoGen, replicate v2, refine by interpolating additional agents for editor, copychecking, etc roles.  |




### Components
- idea generator
- outline generator

### Breaking down the ideal prompt
# Role: describe the agent's purpose and the flavour of work they will be tasked with
# Clarify: describe the specific task that they should be undertaking, be sure to iron out ambiguity
# Format: descibe how the output should be formatted. Be as specific as possible
# Exclusions: a list of things you definitely want to avoid