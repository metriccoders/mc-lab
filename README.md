# MC Lab

MC Lab is a powerful and user-friendly software designed to run large language models (LLMs) locally. It provides seamless integration with Hugging Face, allowing users to download and manage models effortlessly. Additionally, it supports manual input of `.gguf` files for full flexibility. With MC Lab, you can also access an automatically configured FastAPI server to chat with your locally hosted models.

---

## Key Features

- **Download Models from Hugging Face**: Search and download models directly from the Hugging Face repository.
- **Manual Model Input**: Specify custom `.gguf` files for running LLMs.
- **Integrated FastAPI Server**:
  - Automatically starts a FastAPI server upon launching the app.
  - Access the chat endpoint at: `http://127.0.0.1:8000/chat`
- **Interactive Chat Interface**: Chat directly with the downloaded models via the app or API.
- **Full-Screen, Modern GUI**: Designed with PyQt5 for a sleek and intuitive user experience.

---

## Installation

Follow these steps to get started with MC Lab:

### Prerequisites

- **Python 3.8+**
- Install the required Python libraries:
  ```bash
  pip install -r requirements.txt
  ```
  
  Required libraries include:
  - `PyQt5`
  - `huggingface_hub`
  - `fastapi`
  - `uvicorn`
  - `langchain-core`
  - `langchain-community`

### Download MC Lab

1. Clone the repository:
   ```bash
   git clone https://github.com/metriccoders/mc-lab.git
   cd mc-lab
   ```

2. Run the application:
   ```bash
   python app.py
   ```

---

## Usage

### Starting the Application

Run `app.py` to launch the GUI application. The application starts in full-screen mode and includes the following features:

1. **Search and Download Models**:
   - Use the search bar to find models on Hugging Face.
   - Download the selected model by clicking the "Download LLM" button.
2. **Manual Model Loading**:
   - Specify the path to a `.gguf` file manually.
3. **Chat with Models**:
   - Use the chat interface in the GUI to interact with your models.

### FastAPI Server

- The FastAPI server runs automatically when the application starts.
- **Chat Endpoint**: `http://127.0.0.1:8000/chat`
  - Send a POST request to this endpoint with the following format:
    ```json
    {
      "message": "Your message here"
    }
    ```
  - The server will respond with the model's output.

---

## Example API Usage

You can interact with the FastAPI server using any HTTP client, such as `curl` or `Postman`.

**Example using `curl`**:

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
-H "Content-Type: application/json" \
-d '{"message": "Hello, LLM!"}'
```

**Response**:
```json
{
  "response": "Hello! How can I assist you today?"
}
```

---

## Screenshots

Coming soon!

---

## Contributing

We welcome contributions to MC Lab! Feel free to submit issues or pull requests to improve the application.

---

## License

MC Lab is released under the [MIT License](LICENSE).

---

## Contact

For any questions or feedback, please reach out to us at [suhas@metriccoders.com](mailto:suhas@metriccoders.com).

---

Enjoy exploring the power of LLMs with MC Lab!

