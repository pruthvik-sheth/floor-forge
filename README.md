# Floor Forge AI

![Floor Forge Logo](https://img.shields.io/badge/Floor-Forge-blue)

Floor Forge is an AI-powered floor plan generation tool that allows users to create architectural floor plans from text descriptions. Using state-of-the-art Stable Diffusion technology, Floor Forge transforms your ideas into visual floor plans in seconds.

## 📋 Table of Contents

- [Demo](#-demo)
- [Features](#-features)
- [Architecture](#-architecture)
- [Technologies](#-technologies)
- [Installation](#-installation)
- [Usage](#-usage)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

## 🎬 Demo

[![Floor Forge Demo](https://img.shields.io/badge/YouTube-Demo-red)](https://youtube.com/your-demo-link)

Check out our [YouTube demo](https://youtu.be/Qy2p5deY8kc) to see Floor Forge in action!

## ✨ Features

- **Text-to-Floor-Plan Generation**: Convert text descriptions into detailed floor plans
- **Customizable Parameters**: Adjust inference steps, guidance scale, and random seed
- **Real-time Preview**: See your floor plan as it's being generated
- **History Management**: Save and revisit previously generated floor plans
- **Responsive Design**: Works on desktop and mobile devices

## 🏗️ Architecture

Floor Forge follows a client-server architecture:

### Frontend (React)

- Single-page application built with React and Vite
- Responsive UI with modern design principles
- State management using React hooks

### Backend (Python/Flask)

- RESTful API built with Flask
- Stable Diffusion model for floor plan generation
- File storage for generated images and metadata

## 🔧 Technologies

### Frontend

- React
- React Router
- Tailwind CSS
- Vite

### Backend

- Python
- Flask
- PyTorch
- Diffusers (Hugging Face)
- Stable Diffusion

## 📥 Installation

### Prerequisites

- Node.js (v14+)
- Python (v3.8+)
- CUDA-compatible GPU (recommended for faster generation)

### Backend Setup

1. Clone the repository

   ```bash
   git clone https://github.com/yourusername/floor-forge.git
   cd floor-forge
   ```

2. Set up Python environment

   ```bash
   cd floor-forge-backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the backend server
   ```bash
   python run.py
   ```
   The server will start at http://localhost:5000

### Frontend Setup

1. Install dependencies

   ```bash
   cd floor-forge-frontend
   npm install
   ```

2. Start the development server
   ```bash
   npm run dev
   ```
   The frontend will be available at http://localhost:3000

## 🚀 Usage

1. Open your browser and navigate to http://localhost:3000
2. Enter a description of your desired floor plan in the text area
3. Optionally adjust the generation parameters
4. Click "Generate Floor Plan" and wait for the result
5. Save or download your generated floor plan

### Example Prompts

- "A modern one-bedroom apartment with an open kitchen and living room"
- "A spacious three-bedroom house with two bathrooms and a large backyard"
- "A studio apartment with a kitchen island and built-in storage"
- "A two-story family home with four bedrooms and a home office"

## 📚 Documentation

- [Project Report](https://docs.google.com/document/d/1aHJL8Iud8FiWZr9D3W1cL8oal7qwU1uqFO65g7y925s/edit?usp=sharing)
- [Presentation Slides](https://docs.google.com/presentation/d/1AQgPd731rvh8xMPizHvbTUh82BYsb3mH6AHezWmgtnc/edit?usp=sharing)
