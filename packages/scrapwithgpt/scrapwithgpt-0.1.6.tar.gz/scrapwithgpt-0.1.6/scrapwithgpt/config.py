# PIP Package to get specific information from a website using ChatGPT

# First version: 9th of May 2024 by Henry Obegi - Github hanbdle: henryobj
# Updated by XXXXX on XXXXXX
# Contributors: XXXXXXX 

import os

# ***** KEYS 
OAI_KEY = os.getenv("OAI_API_KEY")


# ****** TEXT
OPEN_AI_ISSUE = r"%$144$%" # Arbitrary choice. Just an unlikely string to be output by the LLM. 
ERROR_MESSAGE = "An error occurred and was logged"
WARNING_UNKNOWN = "\033[31mUNKNOWN\033[0m"

# ****** For Web
HTTP_URL_PATTERN = r'^http[s]?://.+'   # Regex pattern to match a URL
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
}

# ****** Models used for Open AI + Window size
MODEL_CHAT = r"gpt-3.5-turbo-0125"
MODEL_CHAT_STABLE = r"gpt-3.5-turbo"
MODEL_GPT4_TURBO = (
    r"gpt-4-1106-preview"  # Max 128,000 token context window total with 4,096 output
)
MODEL_GPT4_STABLE = r"gpt-4"  # 8K context window and 4,096 output

MODEL_EMB_LARGE = r"text-embedding-3-large"
MODEL_EMB_SMALL = r"text-embedding-3-small"

MAX_TOKEN_OUTPUT_DEFAULT = 300
MAX_TOKEN_GPT4_RESULT = 500
MAX_TOKEN_OUTPUT_DEFAULT_HUGE = 3000
MAX_TOKEN_OUTPUT_FILTER = 10000

MAX_TOKEN_WINDOW_GPT4_TURBO = 128000
MAX_TOKEN_WINDOW_GPT35_TURBO = 16385
MAX_TOKEN_WINDOW_GPT4 = 8192
MAX_TOKEN_OUTPUT_GPT3 = 4096


# ***** Default Prompts and output - can be transformed into objects / pull from a json file in the future.
DEFAULT_FILTERING_CRITERIA = """
### Criteria ###
The VC fund / investor should:
a. Primarily invest in companies at early stages (pre-revenue or early revenues).
b. Invest in startups with a valuation of approximately $3M to $15M. Check that the fund does NOT typically invest small amounts for disproportionately large equity. For example investing $100K against 10% of equity.
c. The VC fund / investor should have experience with SaaS, Edtech or AI.
d. Not finance companies that are direct competitors in the space of 'training with simulation of interaction with fake clients'.
e. Have made at least 5 investments.
f. The fund is located in the US or the GCC (Gulf Cooperation Council) countries.
### end of the Criteria ###
"""

JSON_OUTPUT_VC = """{
  "Name of the fund": "string",
  "Country": "string",
  "Number of investments": "integer",
  "Size of the fund": "string",
  "Ticket size": "string",
  "One relevant investment to us and why": "string",
  "Who to contact": {
    "Name": "string",
    "Position": "string",
    "Email": "string",
    "Linkedin page": "string"
  },
  "Good reasons to contact them": "string",
  "Useful Infos": "string"
}"""

JSON_EXAMPLE_VC = """{
  "Name of the fund": "Innovate Ventures",
  "Country": "USA",
  "Number of investments": "12",
  "Size of the fund": "$50M",
  "Ticket size": "$100K to $250K with follow up",
  "One relevant investment to us and why": "EduTech Innovators - Innovate Ventures invested $200K in 2019. EduTech is relevant because your company does X and EduTech does Y which has synergy with your company on A/B/C.",
  "Who to contact": {
    "Name": "Jane Doe",
    "Position": "Investment Director",
    "Email": "jdoe@innovatevc.com",
    "Linkedin page": "https://www.linkedin.com/in/janedoe"
  },
  "Good reasons to contact them": "Innovate Ventures has a strong focus on Edtech, which aligns with our product. They also have a track record of supporting early-stage startups and can provide valuable mentorship and networks in the US market.",
  "Useful Infos": "The fund recently increased its investment cap for Edtech startups and is actively seeking new innovative projects to finance. It mentioned that X and Y. It is noteworthy that Z."
}"""

