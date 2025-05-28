### SET-UP ###
Have OLLAMA hosted locally - preferably on 11434, as OllamaChatCompletionClient uses it as standard. IF NO OLLAMA --> https://ollama.com/

Have a LLM running on your local OLLAMA, run commands --> ollama serve --> ollama run mistral

IF you are not running Mistral then refer to coin.py & coin_30_days.py --> LINE 10 & change "mistral" to desired LLM.

Select .venv as python interpreter. (CTRL + SHIFT + P) --> Python: Select Interpreter 

in terminal, make sure you're in the right environment "c:/somewhere/in/your/folders/MiniProjectAIAgent" then do:

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

Run these commands in your terminal.

python coin.py       OR        python coin_30_days.py

wait for console to answer... 

use one of examples below.


### EXAMPLES ###
bitcoin
ethereum
solana
cardano
avalanche-2
chainlink
polkadot
dogecoin
litecoin
arbitrum



### OLD FAILED PROJECT ###

Same steps for Setup as above. Type python failed.py to run.

wait for console to answer...

Type something like "Give me a summary of the news in Ukraine for the last 7 days"

### INPUT/OUPUT ####

For examples of input & desired output, see the InputOutputExamples.txt file in the root folder.
