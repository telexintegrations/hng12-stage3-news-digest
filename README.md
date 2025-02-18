# hng12-stage3-news-digest: FastAPI News Digest Service

This project is a FastAPI-based web service that fetches the latest news articles from various categories, generates a summarized news digest using an AI summarizer, and sends the digest to a specified endpoint. The service utilizes background tasks to perform these operations asynchronously, ensuring non-blocking API responses.

## Features

- **Fetch Latest News**: Retrieves news articles from multiple categories using the NewsAPI.
- **AI Summarization**: Summarizes the fetched news articles into a concise digest.
- **Background Processing**: Executes news fetching and digest generation in the background to avoid blocking API routes.
- **Telex Integration**: Sends the generated news digest to the Telex platform.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Ayobamidele/hng12-stage3-news-digest.git
   cd hng12-stage3-news-digest
   ```

2. **Install Dependencies**:

   It's recommended to use a virtual environment. You can install dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:

   Create a `.env` file in the project root directory and add the following configurations:

   ```env
   NEWS_API_KEY=your_newsapi_key
   NEWS_COUNTRY=us by defalut but use any countries ISO 3166-1 alpha-2 code of your choice
   TELEX_API_URL=https://ping.telex.im/v1/webhooks/
   SUMMARIZER_API_KEY=Gemini_ai_api_key
   ```

   Replace `your_newsapi_key` and `Gemini_ai_api_key` with your actual API keys.

## Usage

1. **Start the FastAPI Server**:

   ```bash
   uvicorn main:app --reload
   ```

   The server will start at `http://127.0.0.1:8000`.

2. **Trigger News Digest Generation**:

   To initiate the news digest generation process, send a GET request to the `/api/v1/news-digest/tick` endpoint:

   ```bash
      curl -X 'GET' 'http://localhost:8000/api/v1/news_digest/tick' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"settings": [{"label": "categories", "default": ["business", "tech", "sports"]}]}'
   ```

   This will start the background task to fetch, summarize, and send the news digest.

## API Endpoints

### **GET** `/api/v1/news-digest`

This endpoint is used to initiate the background process of fetching, summarizing, and sending the news digest. The process runs in the background and is triggered by the request.

#### **Arguments (Request Body)**

The request requires a JSON payload containing the settings to generate the news digest. The key setting expected is `categories`.

##### Example Request Body

```json
{
  "settings": [
    {
      "label": "categories",
      "default": ["business", "tech", "sports"]
    }
  ]
}
```

### **GET**`/api/v1/current_news?category=str`: Retrive news on a particoer category default is technology. Categories avilable are "business", "technology", "sports", "health" and "entertainment"

## Configuration

- **NewsAPI**: Sign up at [NewsAPI](https://newsapi.org/) to obtain your API key.
- **Telex**: Ensure you have the correct API URL and necessary credentials to send messages to Telex.
- **AI Summarizer**: Obtain a Gemini API key for the AI summarization service.
