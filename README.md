![ScrapYoutuber Banner](./assets/ScrapYotuber.png)

# ScrapYoutuber

ScrapYoutuber is an efficient tool designed to assist sponsors and businesses in collecting crucial information about YouTubers. This tool automates the extraction of key data, such as primary topics, social media profiles, engagement metrics, and more, saving valuable time and effort.

## Features

- **YouTube Channel Insights**: Automatically scrape main topics covered by the YouTuber.
- **Social Media Extraction**: Gather links to other social media accounts like Instagram, Twitter, etc.
- **Engagement Metrics**: Retrieve key engagement metrics such as view counts, likes, comments, and subscriber data.
- **Multi-Agent System**: Leverages a system of intelligent agents to distribute tasks and ensure efficient web scraping and data retrieval.
- **Powered by LLMs**: Uses advanced language models to process and summarize the collected information.
- **Retrieval-Augmented Generation (RAG)**: Ensures accurate and contextually relevant data by retrieving information from multiple sources.
- **YouTube API Integration**: Seamlessly integrates with the YouTube Data API for additional metadata and statistics.

## Technologies Used

- **Multi-Agent System (LangGraph)**: Efficient parallel task execution.
- **Web Scraping (Tavely API)**: Gathers information from YouTube and social media.
- **Retrieval-Augmented Generation (RAG) (LangChain,Chroma,NVIDIA API...)**: Retrieves and summarizes relevant information.
- **YouTube API**: Accesses structured data from YouTube.

## Installation

To run ScrapYoutuber locally, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/ITSAIDI/ScrapYoutuber.git
   cd ScrapYoutuber
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys**:
   - Get your API key from [YouTube Data API](https://developers.google.com/youtube/v3/getting-started).
   - Store it in a `.env` file or directly in the configuration file.
   - You also need to add an LLM_API_Key, here I used Fireworks API but you can change that in **LLMs.py**

4. **Run the application**:

   ```bash
   python main.py
   ```

## Usage

1. Provide the YouTuber’s channel URL to the tool.
2. ScrapYoutuber will automatically collect and display information, including:
   - Main content topics
   - Links to social media accounts
   - Key engagement metrics (e.g., average views, likes, comments)
3. Summarized results will be displayed in the terminal or saved to a file.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please fork the repository and submit a pull request with your changes.

## Contact

If you have any questions or feedback, feel free to reach out via email at [noureddinesaidi111@gmail.com] or open an issue in the GitHub repository.
