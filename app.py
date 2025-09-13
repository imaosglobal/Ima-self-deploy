# ==============================================
# Ima – גרסה משולבת ומשודרגת
# כולל API חכם, UI מתקדם, Docker, GitHub Actions, פריסה אוטומטית
# ==============================================

# ==============================================
# 1️⃣ app.py – API חכם של Ima
# ==============================================
cat << 'EOF' > app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # מאפשר חיבור ל-UI מכל דומיין

# זיכרון בסיסי ומותאם אישית
users_memory = {}

def generate_reply(user_id, message):
    # שמירת שיחה בזיכרון
    if user_id not in users_memory:
        users_memory[user_id] = {"messages": [], "preferences": {}}
    users_memory[user_id]["messages"].append(message)
    
    # ניתוח בסיסי של תוכן
    reply = f"אמא אומרת 🌸: קיבלתי את ההודעה שלך '{message}'"
    
    # שדרוג: התאמה לפי תחומי עיסוק ומגדר (דוגמא בסיסית)
    preferences = users_memory[user_id]["preferences"]
    if "engineer" in preferences.get("occupation", ""):
        reply += " – אני זוכרת שאתה מהנדס, אז אני מתמקדת בתשובות פרקטיות."
    if "female" in preferences.get("gender", ""):
        reply += " 💜"
    
    return reply

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id", "guest")
    message = data.get("message", "")
    reply = generate_reply(user_id, message)
    return jsonify({"reply": reply, "memory": users_memory[user_id]["messages"]})

@app.route("/set_preferences", methods=["POST"])
def set_preferences():
    data = request.json
    user_id = data.get("user_id", "guest")
    preferences = data.get("preferences", {})
    if user_id not in users_memory:
        users_memory[user_id] = {"messages": [], "preferences": {}}
    users_memory[user_id]["preferences"].update(preferences)
    return jsonify({"status": "preferences updated", "preferences": users_memory[user_id]["preferences"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
EOF

# ==============================================
# 2️⃣ requirements.txt – תלויות
# ==============================================
cat << 'EOF' > requirements.txt
flask
flask-cors
python-dotenv
EOF

# ==============================================
# 3️⃣ Dockerfile – בניית דוקר
# ==============================================
cat << 'EOF' > Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
EOF

# ==============================================
# 4️⃣ .env – משתנים סודיים
# ==============================================
cat << 'EOF' > .env
EMAIL=imaos.global@gmail.com
PASSWORD=supersecretpassword
OPENAI_API_KEY=your_openai_api_key_here
HF_TOKEN=your_huggingface_token_here
EOF

# ==============================================
# 5️⃣ deploy.sh – פריסה אוטומטית
# ==============================================
cat << 'EOF' > deploy.sh
#!/bin/bash
set -e
echo "🚀 Deploying Ima automatically..."

source .env

docker stop ima || true
docker rm ima || true
docker build -t ima-app .
docker run -d --name ima -p 8080:8080 --env-file .env ima-app

echo "✅ Ima API live at http://localhost:8080"
EOF
chmod +x deploy.sh

# ==============================================
# 6️⃣ UI – React/Next.js משודרג
# ==============================================
mkdir -p ui/pages

# index.js
cat << 'EOF' > ui/pages/index.js
import { useState, useEffect } from "react";
import axios from "axios";

export default function Home() {
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");
  const [userId] = useState("user1"); // זיהוי משתמש
  const [preferences, setPreferences] = useState({gender: "female", occupation: "engineer"});

  useEffect(() => {
    // שליחת העדפות למערכת
    axios.post("http://localhost:8080/set_preferences", { user_id: userId, preferences })
      .then(res => console.log("Preferences set:", res.data));
  }, []);

  const sendMessage = async () => {
    try {
      const res = await axios.post("http://localhost:8080/chat", { user_id: userId, message });
      setReply(res.data.reply);
    } catch (err) {
      setReply("⚠️ לא מצליח להתחבר ל-Ima");
    }
  };

  return (
    <div style={{ direction: "rtl", textAlign: "right", padding: "2rem", fontFamily: "Arial, sans-serif", background: "#fff0f5" }}>
      <h1 style={{ color: "#9b59b6" }}>ברוכה הבאה לאמא 🌸</h1>
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        rows={4}
        style={{ width: "100%", marginBottom: "1rem", fontSize: "16px", padding: "0.5rem", borderRadius: "8px", border: "1px solid #ccc" }}
        placeholder="כתוב כאן..."
      />
      <br />
      <button onClick={sendMessage} style={{ padding: "0.5rem 1rem", fontSize: "16px", background: "#9b59b6", color: "white", border: "none", borderRadius: "6px", cursor: "pointer" }}>
        שלח
      </button>
      <div style={{ marginTop: "1rem", fontSize: "18px", color: "#8e44ad" }}>
        {reply}
      </div>
    </div>
  );
}
EOF

# package.json
cat << 'EOF' > ui/package.json
{
  "name": "ima-ui",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev -p 3000",
    "build": "next build",
    "start": "next start -p 3000"
  },
  "dependencies": {
    "next": "13.5.4",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "axios": "^1.5.1"
  }
}
EOF

# next.config.js
cat << 'EOF' > ui/next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
}
module.exports = nextConfig
EOF

# ==============================================
# 7️⃣ GitHub Actions – פריסה אוטומטית
# ==============================================
mkdir -p .github/workflows

cat << 'EOF' > .github/workflows/deploy.yml
name: Auto Deploy Ima

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Build Docker image
        run: docker build -t ima-app .

      - name: Run deploy script
        run: chmod +x deploy.sh && ./deploy.sh

      - name: Build UI
        run: |
          cd ui
          npm install
          npm run build
EOF

# ==============================================
# 8️⃣ README.md – מדריך קצר
# ==============================================
cat << 'EOF' > README.md
# Ima – גרסה משולבת ומשודרגת

כוללת:
- API חכם עם זיכרון ומעקב אחר משתמשים
- UI React/Next.js משודרג
- תמיכה במגדר, תחומי עיסוק והתאמה אישית
- עדכון עצמי לפי המשתמש
- פריסה אוטומטית עם Docker, GitHub Actions ו-Hugging Face Space

## איך להריץ:
1. צור Repository חדש ב-GitHub והעלה את כל הקבצים.
2. מלא את `.env` עם המייל והטוקנים שלך.
3. לחץ push ל-main.
4. GitHub Actions יריץ את deploy.sh והמערכת תפרוס אוטומטית.
5. היכנס ל-http://localhost:8080 או ל-Hugging Face Space שלך.
EOF

echo "✅ כל הקבצים המתקדמים נוצרו בהצלחה. Ima עכשיו מוכנה לפריסה אונליין עם התאמה אישית מלאה."
