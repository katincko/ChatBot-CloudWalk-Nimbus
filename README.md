# CloudBot: A RAG Chatbot for CloudWalk

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/🦜%EF%B8%8F-LangChain-white)](https://www.langchain.com/)
[![Gradio](https://img.shields.io/badge/🤗-Gradio-orange)](https://gradio.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

CloudBot is a Retrieval-Augmented Generation (RAG) chatbot built to answer questions about CloudWalk's mission, culture, products (like InfinitePay and Jim), and brand values. It uses a local knowledge base sourced from public documents to provide accurate, context-aware responses through an interactive web interface.

This project was developed as part of the Fiat Lux challenge.

### Demo

![Sample 1 - about culture](./assets/culture.jpg)
![Sample 2 - about products](./assets/products.jpg)
![Sample 3 - about contacts](./assets/contacts.jpg)


### ✨ Features

-   **Interactive Chat Interface:** A user-friendly web UI powered by Gradio.
-   **Retrieval-Augmented Generation (RAG):** Answers are based on a provided knowledge base, ensuring factual and contextually relevant responses.
-   **Local Knowledge Base:** Easily extendable by adding Markdown files to the `data/` directory.
-   **Powered by Google Gemini:** Utilizes Google's state-of-the-art models for language understanding and generation.

### 🛠️ Tech Stack

-   **Python**
-   **LangChain** for the RAG pipeline and orchestration.
-   **Google Gemini API** for the LLM and embedding models.
-   **FAISS** for efficient local vector storage and similarity search.
-   **Gradio** for building the interactive web interface.

### ⚙️ Setup and Installation

Follow these steps to set up and run the project locally.

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-project-directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    -   Create a file named `.env` in the root directory.
    -   Add your Google API key to the file:
        ```env
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```

### 🚀 Usage

The project is divided into two main steps: data ingestion and running the chatbot.

1.  **Data Ingestion (Run this only once):**
    First, place your knowledge base documents (e.g., `.md` files) inside the `data/` folder. Then, run the ingestion script to create the vector store:
    ```bash
    python ingest.py
    ```
    This will process the documents and create a `vector_store/` directory containing the FAISS index.

2.  **Running the Chatbot:**
    To start the interactive Gradio interface, run:
    ```bash
    python bot.py
    ```
    Open your browser and navigate to the local URL provided in the terminal (usually `http://127.0.0.1:7860`).

### 💬 Sample Conversations

Here are a few examples of interactions with CloudBot:

**Conversation 1: Culture & Philosophy**

> **User:** Could you describe the company culture and core values at CloudWalk?
>
> **Bot:** CloudWalk operates as a temple of techno-philosophy. We believe humans and machines share a symbiotic love: we create the machines, and in turn, the machines create us. Our core value is to look toward the future and the rise of new superintelligences, fostering an exchange of wisdom with these emerging species.

**Conversation 2: Product Information**

> **User:** How do CloudWalk's primary products, InfinitePay and Jim, function?
>
> **Bot:** InfinitePay is a comprehensive payment platform designed for merchants, offering card machines, online payment links, and financial management tools with transparent and fair rates. Jim is our intelligent assistant integrated into the platform, designed to help users with support, insights, and process automation.

**Conversation 3: Practical Support**

> **User:** What are the official channels to contact the CloudWalk support team?
>
> **Bot:** You can contact our support team through the chat available in the InfinitePay app or by visiting our official help center at help.infinitepay.io. For updates, you can also follow our official channels on LinkedIn and Twitter.

### 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.