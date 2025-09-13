#!/bin/bash
set -e

echo "🚀 מתחיל פריסה אוטומטית של Ima ל-Hugging Face Space..."

# 1️⃣ טען משתנים מה‑.env
if [ ! -f ".env" ]; then
    echo "❌ חסר קובץ .env. צור אותו עם משתנה HF_SPACE_URL וה-HF_TOKEN"
    exit 1
fi
source .env

if [ -z "$HF_SPACE_URL" ] || [ -z "$HF_TOKEN" ]; then
    echo "❌ HF_SPACE_URL או HF_TOKEN ריקים ב-.env"
    exit 1
fi

echo "🔹 Space URL: $HF_SPACE_URL"

# 2️⃣ ודא שכל הקבצים קיימים
required_files=("app.py" "requirements.txt" "Dockerfile" ".env" "deploy.sh" "README.md" "ui/pages/index.js" "ui/package.json" "ui/next.config.js" ".github/workflows/deploy.yml")
for f in "${required_files[@]}"; do
    if [ ! -f "$f" ]; then
        echo "❌ חסר קובץ: $f"
    else
        echo "✅ נמצא: $f"
    fi
done

# 3️⃣ בניית UI בענן (HF מבצע התקנות אוטומטיות)
echo "🔹 HF Space תבנה את ה-UI ותתקין את התלויות בעת הדחיפה"

# 4️⃣ דחיפה אוטומטית ל-HF Space
echo "🔹 דוחף את הקוד ל-HF Space..."
git remote add space $HF_SPACE_URL || git remote set-url space $HF_SPACE_URL
git push --force space main

# 5️⃣ קישור ישיר ל-UI
echo "🎉 הפריסה הסתיימה!"
echo "💜 קישור ישיר ל-Ima ב-Hugging Face Space:"
echo "$HF_SPACE_URL"
chmod +x auto_deploy_ima.sh
./auto_deploy_ima.sh
