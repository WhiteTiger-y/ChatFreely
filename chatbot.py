import streamlit as st
from g4f.client import Client

# App title and configuration
st.set_page_config(page_title="🤖💬 ChatGpt-4 Chatbot", page_icon="🤖")

# Initialize the GPT-4 client
client = Client()

# Sidebar for model selection and chat clearing
with st.sidebar:
    st.title('🤖💬 GPT4Free LLMs Chatbots')
    st.markdown('This is a chatbot using various models.')
    model = st.selectbox(
        "Choose a model",
        [
            "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo","gpt-4o", "Meta-Llama-3-8b-instruct", 
            "Meta-Llama-3-70b-instruct", "CodeLlama-34b-Instruct-hf", "CodeLlama-70b-Instruct-hf", 
            "Mixtral-8x7B-Instruct-v0.1", "Mistral-7B-Instruct-v0.1", "Mistral-7B-Instruct-v0.2", 
            "zephyr-orpo-141b-A35b-v0.1", "dolphin-2.6-mixtral-8x7b", "gemini", "gemini-pro", 
            "claude-v2", "claude-3-opus", "claude-3-sonnet", "lzlv_70b_fp16_hf", "airoboros-70b", 
            "openchat_3.5", "pi"
        ]
    )
    if st.button("Clear Chat"):
        st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Function for generating LLM response with streaming
def generate_response_stream(prompt_input):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for message in st.session_state.messages:
        messages.append({"role": message["role"], "content": message["content"]})

    messages.append({"role": "user", "content": prompt_input})

    # Get the response from the model
    chat_completion = client.chat.completions.create(model=model, messages=messages, stream=True)

    # Stream the response
    response = ""
    for completion in chat_completion:
        delta = completion.choices[0].delta.content or ""
        response += delta
        yield delta

# Store LLM generated responses
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        with st.spinner("Thinking..."):
            for delta in generate_response_stream(prompt):
                full_response += delta
                response_container.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
