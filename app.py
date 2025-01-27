import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QTextEdit,
    QHBoxLayout,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QScrollArea,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import time
from huggingface_hub import HfApi, hf_hub_download

from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate


template = """
Question: {question}

Answer: Give the accurate answer. If you are unsure say you do not know.
"""
prompt = PromptTemplate.from_template(template)

class FullScreenApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("MC Studio")
        
        h_layout = QHBoxLayout()

        self.search_llm_textbox = QLineEdit()
        self.search_llm_textbox.setFixedSize(450, 45)
        self.search_llm_textbox.setPlaceholderText('Search LLM')
        
        h_layout.addWidget(self.search_llm_textbox)
        
        self.download_llm_button = QPushButton('Download LLM')
        self.download_llm_button.setFixedSize(250, 60)
        self.download_llm_button.clicked.connect(self.download_llm)
        
        h_layout.addWidget(self.download_llm_button)
        h_layout.setSpacing(10)  # Set spacing between the widgets
        
        self.results_area = QScrollArea()
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout()
        self.results_container.setLayout(self.results_layout)
        self.results_area.setWidget(self.results_container)
        self.results_area.setWidgetResizable(True)
        self.results_area.setStyleSheet("background-color: white; border: 1px solid #e2e8f0;")
        self.results_area.setFixedHeight(800)        
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(h_layout)
        main_layout.addWidget(self.results_area)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        # Show the window in full-screen mode
        self.showFullScreen()
        
    def download_llm(self):
        # Clear existing results
        for i in reversed(range(self.results_layout.count())):
            self.results_layout.itemAt(i).widget().deleteLater()
        # Get the text from the textbox
        search_query = self.search_llm_textbox.text()
        print("Looking for:",search_query)
        # Initialize Hugging Face API
        api = HfApi(endpoint="https://huggingface.co")

        # Query models based on the search term
        try:
            models = api.list_models(search=search_query, limit=5)
            print("List of models:", models)
            if models:
                print("Found models:", models)
                for model in models:
                    print("model:", model)
                    self.add_model_to_results(model_id=model.modelId)
            else:
                self.add_message_to_results("No models found for your search.")
        except Exception as e:
            self.add_message_to_results(f"An error occurred: {e}")
        
       
    def add_model_to_results(self, model_id):
        # Create a horizontal layout for the model label and download button
        model_layout = QHBoxLayout()
        print("Adding model:", model_id)
        # Create a label for the model name
        model_label = QLabel(model_id)
        model_label.setStyleSheet(
            "background-color: #f8fafc; border: 1px solid #e2e8f0; "
            "border-radius: 8px; padding: 8px; font-size: 14px; font-family: 'Arial';"
        )
        model_label.setFixedHeight(40)
        model_label.setAlignment(Qt.AlignVCenter)

        # Create a download button
        download_button = QPushButton("Download")
        download_button.setFixedHeight(40)
        download_button.setStyleSheet(
            "background-color: #3b82f6; color: white; border-radius: 4px; padding: 4px 8px;"
        )
        download_button.clicked.connect(lambda: self.download_model(model_id))

        # Add label and button to the layout
        model_layout.addWidget(model_label)
        model_layout.addWidget(download_button)
        self.results_layout.addLayout(model_layout)

    def add_message_to_results(self, message):
        # Add a simple label to the results area
        message_label = QLabel(message)
        message_label.setStyleSheet(
            "font-size: 14px; font-family: 'Arial'; color: #475569; padding: 8px;"
        )
        self.results_layout.addWidget(message_label)
        
        
    def download_model(self, model_id):
        # Simulate the download process
        time.sleep(1)  # Simulate download delay
        filename = f"{model_id}.gguf"
        with open(filename, "w") as f:
            f.write("Simulated GGUF model content")  # Simulate saving a model
        self.add_message_to_results(f"{filename} downloaded successfully.")
        self.show_chat_area()

    def show_chat_area(self):
        # Add a chat input and button after download
        self.chat_label = QLabel("Start chatting with the downloaded model:")
        self.chat_textbox = QLineEdit(self)
        self.chat_textbox.setPlaceholderText("Type your message here")
        self.chat_button = QPushButton("Send")
        self.chat_button.setFixedHeight(40)
        self.chat_button.setStyleSheet(
            "background-color: #3b82f6; color: white; border-radius: 4px; padding: 4px 8px;"
        )
        self.chat_button.clicked.connect(self.send_message_to_model)
        
        
        # Define the chat layout
        self.chat_layout = QHBoxLayout()
        self.chat_layout.addWidget(self.chat_textbox)
        self.chat_layout.addWidget(self.chat_button)

        # Add to the main layout
        self.results_layout.addWidget(self.chat_label)
        self.results_layout.addLayout(self.chat_layout)

        self.chat_response_textbox = QTextEdit(self)
        self.chat_response_textbox.setPlaceholderText("Model response")
        self.results_layout.addWidget(self.chat_response_textbox)
        
        
    def send_message_to_model(self):
        chat_message = self.chat_textbox.text()
        print("You sent...", chat_message)
        
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        llm = LlamaCpp(
            
            model_path="llama-2-7b-chat.Q2_K.gguf",
            temperature=0.8,
            max_tokens=2500,
            top_p=1,
            callback_manager=callback_manager,
            verbose=True
        )
        
        self.chat_response_textbox.setText(str(llm(chat_message)))
    
    
    def keyPressEvent(self, event):
        # Allow the user to exit full-screen mode with the 'Esc' key
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Load the stylesheet for the entire application
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())
    mainWin = FullScreenApp()
    sys.exit(app.exec_())
