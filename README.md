# Financial Fake News Detection

A full-stack application designed to analyze financial tweets and detect potential fake news. It utilizes machine learning models to assess sentiment, compare tweet statements with recent news articles for similarity, and calculate an overall "Truth Score" based on various engagement and credibility metrics.

## Features

- **Sentiment Analysis:** Evaluates the tone of the financial tweet.
- **Keyword Extraction:** Automatically identifies core keywords to search against current events.
- **News Similarity:** Scrapes recent news articles based on keywords and checks them against the tweet's claim.
- **User Credibility & Truth Scoring:** Factors in user verification, likes, comments, and retweets to assess the likelihood of the claim being true or false.
- **Modern UI:** Built with Next.js, featuring a clean, responsive, and animated dark-mode interface.
- **FastAPI Backend:** A fast and scalable Python backend utilizing Scikit-Learn models.

## Tech Stack

- **Frontend:** Next.js, React, Tailwind CSS, TypeScript, pnpm
- **Backend:** Python, FastAPI, Uvicorn
- **Machine Learning:** Scikit-Learn, Joblib, NLTK, BeautifulSoup4

## Prerequisites

- Node.js (for the frontend)
- `pnpm` (for frontend package management)
- Python 3.13 (or compatible version)

## Getting Started

### 1. Backend Setup

1. Navigate to the project root directory.
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```
   The backend API will be available at `http://127.0.0.1:8000`.

### 2. Frontend Setup

1. Open a new terminal and navigate to the `Frontend` directory:
   ```bash
   cd Frontend
   ```
2. Install the necessary Node dependencies:
   ```bash
   pnpm install
   ```
3. Start the Next.js development server:
   ```bash
   pnpm dev
   ```
4. Open your browser and go to [http://localhost:3000](http://localhost:3000).

## How to Use

1. Go to the web application at `http://localhost:3000`.
2. Paste the text of a financial tweet.
3. Input the engagement metrics (Likes, Comments, Retweets, Account Type).
4. Select the timestamp for how far back to check the news.
5. Click **Get Result** to see the analyzed Truth Score, Sentiment, and Final Verdict.

## Project Structure

- `app/` - FastAPI backend application and routes.
- `Frontend/` - Next.js UI application.
- `Models/` - Pre-trained Scikit-Learn `.joblib` models.
- `Modules/` - Engine logic including keyword extraction, scraping, and scoring.
- `Tests/` - Python backend tests.