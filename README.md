# Financial Chatbot

This project is a financial chatbot built with Streamlit, leveraging various machine learning models, APIs, and other tools to provide users with financial insights and predictions. The chatbot utilizes Mistral AI for natural language processing and generating context-aware responses.

## Features

- *Chat-based Interface*: Users can interact with the chatbot through a simple chat interface.
- *Stock Price Prediction*: Predict future stock prices based on historical data using linear regression.
- *Text-to-Speech*: Convert chatbot responses to speech using the Google Text-to-Speech (gTTS) API.
- *Speech Recognition*: Allow users to input queries through speech, using the SpeechRecognition library.
- *Dynamic Data Handling*:
  - *CSV Drag and Drop*: Upload CSV files, and the chatbot will use the data to answer related questions.
  - *Text File Drag and Drop*: Upload text files, and the chatbot will incorporate the content into its responses.
- *File-based Question Answering*: The chatbot can answer questions based on the uploaded CSV and text files, enhancing its ability to provide context-aware responses.

## Project Files

- *finbot.py*: The main script that runs the Streamlit app, handles user interactions, processes data, and generates responses.
- *StockPredictor.py*: Adds the feature of stock price prediction and helps us in displaying graphs.
- *TTS_STT*: Helps in converting text to speech and speech to text.
- *.gitignore*: Ensures that sensitive files like environment variables, temporary files, and other non-essential files are not tracked by Git.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Aarnav005/Financial-Chatbot.git
   cd Financial-Chatbot
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a .env file in the root directory.
   - Add your Hugging Face API token to this file:
     
     Hugging_Face_Api=your_api_key
     

4. Run the Streamlit app:
   ```bash
   streamlit run finbot.py
   ```

## Usage

- *Upload Data*: Drag and drop CSV or text files to provide the chatbot with additional data.
- *Chat Interface*: Type or speak your queries. The chatbot will respond based on available data and context.
- *Stock Predictions*: Enter a stock ticker symbol to get a prediction for the next day's closing price.
