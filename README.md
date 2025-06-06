# AI-Powered Trivia Game

An interactive, web-based trivia game built with Python, HTML, Quart, and OpenAI API. Users can choose trivia categories and difficulty levels, answer multiple-choice questions, and receive instant feedback with GPT-powered answer explanations.

---

## Features

- Question bank from [Open Trivia DB API](https://opentdb.com/api_config.php)
- Selction menu offers dropdown category selection menu and question difficulty choice (easy, medium, or hard)
- AI explanations implemented using an OpenAI API Key (incorporperated through a dotenv file for security)
- "New Question" and "Choose New Category" buttons for fast replay
- Clean, minimalist HTML UI.

---

## Screenshots

### Category & Difficulty Selection  
![Category Selection](Assets/menu.png)

### Correct Answer Example  
![Correct Answer](Assets/right2.png)

### Incorrect Answer Example  
![Wrong Answer](Assets/wrong.png)

> More screenshots located in the `/Assets/` folder

---

## Running the App

To run your own version of the trivia game with OpenAI explanations, follow these steps:

---

### 1. Get an OpenAI API Key

1. Sign up at [https://platform.openai.com/signup](https://platform.openai.com/signup)  
2. Visit your [API keys dashboard](https://platform.openai.com/account/api-keys)  
3. Click **"Create new secret key"** and copy it somewhere safe

> Treat this key like a password — do **not** share or upload it.

---

### 2. Set up your `.env` file

In the root folder of your project, create a file named `.env` and paste in:

```env
OPENAI_API_KEY=your-api-key-here
```

---

### 3. Download the Project Files

Make sure your folder includes the following:

your-folder/
  - chat.py
  - .env
  - templates/
    - index.html

---

### 4. Run the App Locally
Finally, run the chat.py file. This should provide you a link in the terminal to a local deployment of the app that can be opened on an internet browser.

--- 
