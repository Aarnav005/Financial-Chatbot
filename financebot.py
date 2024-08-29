import streamlit as st
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
import yfinance as yf
import pandas as pd
from StockPredictor import predict, stock_graph
from TTS_STT import text_to_speech, recognize_speech


load_dotenv()

def generate_ai_response(prompt, client):
    csv_data= st.session_state.get('csv_data', pd.DataFrame())
    text_data= st.session_state.get('text_data', "No text data available")
    system_message = f"""You are a personal finance AI assistant. You will only respond to queries related to personal finance.
    Also answer questions based on the following data:

    Text data:
    {text_data}

    CSV data:
    {csv_data.to_string() if not csv_data.empty else "No CSV data available"}
    When answering questions, always refer to and use the information from the Text data and CSV data provided above if it's relevant to the query.
    Answer questions related to the uploaded files or personal finance only."""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]

    response = ""
    for message in client.chat_completion(
        messages=messages,
        max_tokens=120,
        stream=True
    ):
        response += message.choices[0].delta.content or ""

    return response

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

            
def main():
    st.title('AI Assistant')

    
    with st.sidebar:
        st.title('AI Assistant Settings')
        hf_api_token = os.getenv("Hugging_Face_Api")
        st.button('Clear Chat History', on_click=clear_chat_history)
        st.title("Drag and Drop Files")
        csv_uploaded_files = st.file_uploader("Drag and drop CSV files here", type=["csv"])
        if csv_uploaded_files is not None:
            st.session_state.csv_data = pd.read_csv(csv_uploaded_files)
            st.success("CSV data uploaded and ready to use!")

        text_uploaded_files = st.file_uploader("Drag and drop text files here", type=["txt"])
        if text_uploaded_files is not None:
            text_data = text_uploaded_files.getvalue().decode("utf-8")
            st.session_state.text_data = text_data
            st.success("Text data uploaded and ready to use!")

        st.title("Stock Price Predictor")
        tick=st.chat_input("Enter Ticker Symbol")
        if tick:
            st.write("Tomorrow's Predicted Stock price is ",predict(tick))
        else:
            st.write("Enter Valid ticker symbol")

    
    client = InferenceClient(
        token=hf_api_token  
    )

    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    
    user_input = st.chat_input("Type your message here:")
    response = ""

    if user_input:
        start_date = "2011-01-01"
        end_date = "2024-01-01"
        if "stock price of" in user_input.lower():
            ticker = user_input.lower().split("stock price of")[-1].strip()
            tables=yf.download(ticker,start=start_date,end=end_date)
            try:
                stock_info = yf.Ticker(ticker).info
                current_price = stock_info.get('currentPrice')
                response = f"\nThe current price of {ticker} is: {current_price}"
            except Exception as e:
                response = f"\nError fetching stock data: {e}"
            with st.sidebar:
                st.title("Graph of Stock price")
                stock_graph(tables)
                
        elif "stock price table of" in user_input.lower():
            ticker = user_input.lower().split("stock price table of")[-1].strip()
            tables=yf.download(ticker,start=start_date,end=end_date)
            response=st.dataframe(tables)
            with st.sidebar:
                st.title("Graph of Stock price")
                stock_graph(tables)
                


        else:
            response = generate_ai_response(user_input, client)

        
        if response:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
    
    if st.button("Read", key=f"tts_{message}"):
        audio_file = text_to_speech(message["content"])
        if audio_file:
            st.audio(audio_file)

    if st.button("Speak"):
        speech = recognize_speech()
        if speech:
            user_input=speech
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        response = generate_ai_response(user_input, client)

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

        

            
if __name__ == "__main__":
    main()
