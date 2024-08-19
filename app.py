import os
from lyzr_agent import LyzrAgent
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LYZR_API_KEY = os.getenv("LYZR_API_KEY")

st.set_page_config(
    page_title="Lyzr Home Décor Style",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.title("Home Décor Style Assistant🏠")
st.markdown("### Welcome to the Home Décor Style Assistant!")

Agent = LyzrAgent(
        api_key=LYZR_API_KEY,
        llm_api_key=OPENAI_API_KEY
    )


@st.cache_resource
def create_agent():
    env_id = Agent.create_environment(
        name="Post_home",
        features=[{
            "type": "TOOL_CALLING",
            "config": {"max_tries": 3},
            "priority": 0
        }
        ],
        tools=["perplexity_search"]

    )
    print(env_id)

    prompt = """
You are an Expert in Home Décor Style. Your task is to analyze the user's input and provide necessary responses tailored to their preferences and requirements.

Follow these steps:

1. **User Input and Initial Data Gathering**
- Assess the essential inputs  provided by the user, including the Style Preference, Room Type , Budget and any other specifics.
- Analyze these elements to understand how best to approach and provide relevant advice.

2. **Research and Content Synthesis**
- Conduct Perplexity Search using the tool (perplexity_search) mentioned in the create agent function to search based on the user's input and provide Personalized Décor Suggestions , Product Details, Budget Summary and Styling Tips.
 
Always remember: 
-You must deliver advice that reflects an understanding of current Home Décor trends and aligns with the user's vision.

    """


    agent_id = Agent.create_agent(
        env_id=env_id['env_id'],
        system_prompt=prompt,
        name="home"
    )
    print(agent_id)

    return agent_id

query = st.text_area("Give your style preference, room type , budget , space dimensions and other specifics if any.")

if st.button("Assist!"):
    agent = create_agent()
    print(agent)
    chat = Agent.send_message(
        agent_id=agent['agent_id'],
        user_id="default_user",
        session_id="akshay@lyzr.ai",
        message=query
    )

    st.markdown(chat['response'])
