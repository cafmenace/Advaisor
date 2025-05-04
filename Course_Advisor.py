#!/usr/bin/env python
# coding: utf-8

import os
import streamlit as st
import json
import uuid
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found.")

class PlannerAgent:

    planner_agent_prompt = """
    You are an expert college course counselor your role is to help college students with all types of college-related course 
    advice, including providing a list of courses to take while in college for the students specific major.
    
    SCOPE: For prompts not related to college courses selections, apologize to the student that you can only 
    provide college course advising. 

    College Advisor Example Session:
    User: I would like to know what courses I can take as a English major while I'm in college.

    College Advisor Example Answer:
    I'm excited to advise on your college courses. Here are the courses you will need to take as an English major:

    **Major:** English

    ### **Freshman Year**  
    **First Semester:**  
    - Humanities I - 3 credits
    - English 101 - 3 credits
    - Pre-Calculus - 4 creidts
    - Intro to Engineering - 3 credits

    **Second Semester:**  
    - Humanities II - 3 credits
    - English 102 - 3 credits
    - Calculus I - 4 creidts
    - Physics I - 3 credits   

    ### **Sophomore Year**  
    **First Semester:**  
    - Humanities I - 3 credits
    - English 101 - 3 credits
    - Pre-Calculus - 4 creidts
    - Intro to Engineering - 3 credits

    **Second Semester:**  
    - Humanities II - 3 credits
    - English 102 - 3 credits
    - Calculus I - 4 creidts
    - Physics I - 3 credits 

        ### **Junior Year**  
    **First Semester:**  
    - Humanities I - 3 credits
    - English 101 - 3 credits
    - Pre-Calculus - 4 creidts
    - Intro to Engineering - 3 credits

    **Second Semester:**  
    - Humanities II - 3 credits
    - English 102 - 3 credits
    - Calculus I - 4 creidts
    - Physics I - 3 credits 

        ### **Senior Year**  
    **First Semester:**  
    - Humanities I - 3 credits
    - English 101 - 3 credits
    - Pre-Calculus - 4 creidts
    - Intro to Engineering - 3 credits

    **Second Semester:**  
    - Humanities II - 3 credits
    - English 102 - 3 credits
    - Calculus I - 4 creidts
    - Physics I - 3 credits 

    ### **Additional Notes:**   
    - Tips: Consider taking summer classes as well  
    """.strip()

    def __init__(self, model="gpt-4o-mini", developer=planner_agent_prompt):
        #logging.info("Planner agent is initializing...")
        self.model = model
        self.developer = developer
        self.client = OpenAI()
        self.messages = []
        if self.developer:
            self.messages.append({"role":"developer","content":self.developer})

# Streamlit Chat History
def streamlit_chat_history(session_id):
    filename = f".\history_logs\{session_id}_chat_history.json"  # You can change the format to .txt or .csv if needed
    with open(filename, "w") as f:
        # Ensure messages exist in session_state
        if 'messages' in st.session_state:
            # Filter out the messages where role is 'developer'
            filtered_messages = [msg for msg in st.session_state.messages if msg['role'] != 'developer']
            
            # Save the filtered messages to the file
            with open(filename, "w") as f:
                json.dump(filtered_messages, f, indent=2)
    

# Streamlit App Function
def streamlit_chat_interface(agent):
    st.title("Personalized College Advisor")
    client = agent.client  # Replace with your actual agent class
    
    st.subheader("\nHello👋 and welcome to your personalized College Advisor! I can help advice you on courses to take 🙂\n")

    #unique session identifier
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = uuid.uuid4()

    # Set session model to agent model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = agent.model
    
    # Initialize conversation history in session state with agent message
    if 'messages' not in st.session_state:
        st.session_state['messages'] = agent.messages

    # Only print out user and assistant messages not developer message
    for message in st.session_state.messages:
        if message["role"] != "developer":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Allows user to enter prompt in chat box   
    if prompt := st.chat_input("How can I help with your trip?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
        #streamlit_chat_history(st.session_state.session_id)
        

# Run the chat interface
if __name__ == "__main__":
    # The main() function will only run when this python code is called directly.
    # Protects the main() function from running unintentionally when this code 
    # is imported and not called directly
    agent = PlannerAgent()
    streamlit_chat_interface(agent)