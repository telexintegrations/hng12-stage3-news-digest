# hng12-stage3-news-digest: FastAPI News Digest Service

This project is a FastAPI-based web service that fetches the latest news articles from various categories, generates a summarized news digest using an AI summarizer, and sends the digest to a specified endpoint. The service utilizes background tasks to perform these operations asynchronously, ensuring non-blocking API responses.

## Features

- **Fetch Latest News**: Retrieves news articles from multiple categories using the NewsAPI.
- **AI Summarization**: Summarizes the fetched news articles into a concise digest.
- **Background Processing**: Executes news fetching and digest generation in the background to avoid blocking API routes.
- **Telex Integration**: Sends the generated news digest to the Telex platform.
- **Integration Endpoint**: Provides an `/api/v1/integration.json` endpoint for Telex integration.

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
   NEWS_COUNTRY=us by default but use any country's ISO 3166-1 alpha-2 code of your choice
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

   To initiate the news digest generation process, send a POST request to the `/api/v1/news-digest/tick` endpoint:

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

### **GET** `/api/v1/current_news?category=<category>`

This endpoint retrieves the latest news articles from a specified category. If no category is provided, it defaults to `business`.

#### **Available Categories:**

- `business`
- `technology`
- `sports`
- `health`
- `entertainment`

#### **Example Response:**

```json
{
  "status_code": 200,
  "success": true,
  "message": "Articles fetched successfully",
  "data": [
    {
      "source": {"id": "bbc-news", "name": "BBC News"},
      "author": "John Doe",
      "title": "Breaking News Title",
      "description": "Short description of the news article...",
      "url": "https://news.example.com/article",
      "urlToImage": "https://news.example.com/image.jpg",
      "publishedAt": "2025-02-22T12:00:00Z",
      "content": "Full news article content..."
    }
  ]
}
```

### **GET** `/api/v1/integration.json`

This endpoint provides integration details for Telex, including available settings and execution parameters.

#### **Example Response:**

```json
{
  "data": {
    "date": {
      "created_at": "2025-02-18",
      "updated_at": "2025-02-22"
    },
    "descriptions": {
      "app_name": "News Digest",
      "app_description": "An automated news digest service that fetches and summarizes news articles from multiple sources, then sends the digest to Telex.",
      "app_logo": "https://ucarecdn.com/ca598933-5ebc-49c8-a338-d7fef3bed1df/news_digest.jpg",
      "app_url": "http://127.0.0.1:8000",
      "background_color": "#fff"
    },
    "is_active": true,
    "integration_type": "interval",
    "key_features": [
      "Fetches news from multiple categories",
      "Uses AI summarization for digest generation",
      "Sends digest to Telex channels"
    ],
    "integration_category": "Communication & Collaboration",
    "author": "Ayobamidele Ewetuga",
    "website": "http://127.0.0.1:8000",
    "settings": [
      {
        "label": "categories",
        "type": "multi-select",
        "description": "Select categories to filter trending news",
        "options": ["business", "technology", "sports", "health", "entertainment"],
        "default": ["technology", "business"]
      },
      {
        "label": "interval",
        "type": "text",
        "required": true,
        "default": "* */6 * * *"
      }
    ],
    "target_url": "",
    "tick_url": "http://127.0.0.1:8000/api/v1/news_digest/tick"
  }
}
```

### **POST** `/api/v1/news_digest/tick`

This endpoint is triggered by Telex at a specified cron interval to generate the news digest.

#### **Example Request Body:**

```json
{
  "settings": [
    {
      "label": "categories",
      "default": ["business", "technology"]
    }
  ]
}
```

#### **Example Response:**

```json
{
  "status_code": 200,
  "success": true,
  "message": "News digest generation initiated."
}
```

## Configuration

- **NewsAPI**: Sign up at [NewsAPI](https://newsapi.org/) to obtain your API key.
- **Telex**: Ensure you have the correct API URL and necessary credentials to send messages to Telex.
- **AI Summarizer**: Obtain a Gemini API key for the AI summarization service.
