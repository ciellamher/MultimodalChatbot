# Multimodal Dictionary Chatbot

## Overview
This project is a multimodal chatbot that functions as a dictionary for both words and images. It allows users to look up word definitions or upload images to get a description and classification.

## Features
- **Word Dictionary:** Returns definitions, parts of speech, examples, and synonyms using NLTK WordNet.
- **Image Analysis:** Classifies images and provides descriptions using a pre-trained ResNet50 model (torchvision).
- **Interfaces:** Supports both a Command Line Interface (CLI) and a Web UI (Streamlit).
- **Safety:** Includes a basic safety filter to refuse explicit or unsafe content.

## Installation
1. Ensure Python 3.10+ is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt# MultimodalChatbot
