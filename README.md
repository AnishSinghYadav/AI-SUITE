# AI Suite - Multi-Feature Application

A Streamlit-based web application combining AI-powered literary creation and face swapping capabilities.

![AI Suite Demo]
<img width="1710" alt="Screenshot 2025-04-06 at 2 34 13 AM" src="https://github.com/user-attachments/assets/830f1123-825f-46fc-a1a8-edc29fba7b15" />
<img width="1710" alt="Screenshot 2025-04-06 at 2 37 13 AM" src="https://github.com/user-attachments/assets/2300a53e-2568-4a47-892f-5b935dbdf67c" />
<img width="1710" alt="Screenshot 2025-04-06 at 2 37 35 AM" src="https://github.com/user-attachments/assets/3f661f13-86bb-42cc-9431-7f79ec458dfd" />
<img width="1710" alt="Screenshot 2025-04-06 at 2 39 08 AM" src="https://github.com/user-attachments/assets/4d2fc6f4-1a7c-4a2d-8e38-7e0a03ac3514" />
<img width="1710" alt="Screenshot 2025-04-06 at 4 01 56 AM" src="https://github.com/user-attachments/assets/f6edd8cb-f578-4510-9f65-2da5c5d487db" />

## Features

### 📚 Literary Creator
- **Poem Generation**: Create poems in 3 styles (Rhyming, Free Verse, Haiku) with length control
- **Story Generation**: Generate multi-chapter stories with dialogues and descriptions
- **Parent Controls**: 
  - Set approved topics
  - Track usage attempts (10/session)
  - AI-powered topic validation
- **Text-to-Speech**: Convert generated content to audio
- **Content Editing**: Modify generated text before export

### 🖼️ Face Swapper
- Real-time face swapping between images
- Automatic face detection
- Side-by-side comparisons
- Supports JPG/PNG formats

## Prerequisites

- Python 3.8+
- OpenAI API key
- [inswapper_128.onnx](https://github.com/deepinsight/insightface/releases) model file

## Installation

1. Clone repository:
```bash
git clone https://github.com/yourusername/ai-suite.git
cd ai-suite
