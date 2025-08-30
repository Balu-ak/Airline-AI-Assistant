# ✈️ Airline AI Assistant

## Project Description
This project implements a simple Airline AI Assistant using OpenAI's function-calling capabilities and a Gradio web interface. The assistant can respond to user queries by intelligently deciding when to use specific tools to provide ticket prices for predefined destinations or list all available cities.

## Features
-   **Ticket Price Lookup:** Get simulated ticket prices for specific cities (currently: London, Paris, Tokyo, Berlin).
-   **Available Cities List:** Ask the assistant to list all destinations it currently supports.
-   **Interactive Chat Interface:** A user-friendly, browser-based chat interface powered by Gradio.
-   **OpenAI Function Calling:** Leverages large language models (LLMs) to understand user intent and execute Python functions (tools) to retrieve information.

## Getting Started

### Prerequisites
Before running the application, ensure you have the following installed:
-   Python 3.8+
-   An OpenAI API Key

### Setup Instructions

1.  **Clone the Repository:**
    Start by cloning this repository to your local machine:
    ```bash
    git clone https://github.com/your-username/airline-ai-assistant.git
    cd airline-ai-assistant
    ```
    (Remember to replace `your-username/airline-ai-assistant` with your actual GitHub repository path after you create it).

2.  **Create a Virtual Environment (Recommended):**
    It's good practice to use a virtual environment to manage dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    Install all required Python packages using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure OpenAI API Key:**
    Your OpenAI API Key is required to interact with the LLM. It is **highly recommended** to set this as an environment variable named `OPENAI_API_KEY`:

    **On Linux/macOS:**
    ```bash
    export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    ```

    **On Windows (Command Prompt):**
    ```bash
    set OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    ```

    **On Windows (PowerShell):**
    ```powershell
    $env:OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    ```
    Replace `"YOUR_OPENAI_API_KEY"` with your actual key. If you prefer to hardcode it (not recommended for production or sharing), you can uncomment and set the `openai.api_key` line in `app.py`.

5.  **Configure Model and System Message (Optional):**
    You can adjust the `MODEL` variable (e.g., from `"gpt-3.5-turbo"` to `"gpt-4"`) and the `system_message` in `app.py` to change the LLM's behavior or capabilities.

## Usage

Once the setup is complete, you can run the Airline AI Assistant:

```bash
python app.py
