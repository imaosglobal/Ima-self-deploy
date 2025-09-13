#!/bin/bash
set -e

echo "🚀 מתחיל פריסה מלאה של Ima ל-Hugging Face Space..."

# 1️⃣ בדיקה שכל הקבצים קיימים
required_files=("app.py" "requirements.txt" "Dockerfile" ".env" "deploy.sh" "README.md" "ui/pages/index.js" "ui/package.json" "ui/next.config.js" ".github/workflows/deploy.yml")
for f in "${required_files[@]}"; do
    if [ ! -f "$f" ]; then
        echo "❌ חסר קובץ: $f"
    else
        echo "✅ נמצא: $f"
    fi
done

# 2️⃣ בדיקת תלויות Python
echo "🔹 התקנת תלויות Python..."
pip install -r requirements.txt

# 3️⃣ בדיקת npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm לא מותקן. התקן Node.js/npm לפני המשך."
    exit 1
else
    echo "✅ npm מותקן"
fi

# 4️⃣ בניית UI קצרה
echo "🔹 בניית UI..."
cd ui
npm install --silent
npm run build
cd ..

# 5️⃣ הפעלת deploy.sh
echo "🔹 הרצת deploy.sh ל-Docker..."
chmod +x deploy.sh
./deploy.sh

# 6️⃣ דחיפה ל-HF Space
HF_REMOTE="https://huggingface.co/spaces/imaosglobal/ima-space"
echo "🔹 דחיפה ל-Hugging Face Space: $HF_REMOTE"
git remote add space $HF_REMOTE || echo "Remote כבר קיים"
git push --force space main

echo "🎉 הפריסה הסתיימה!"
echo "💜 קישור ישיר ל-Space שלך: $HF_REMOTE"
echo "בדוק את ה-UI וה-API: https://huggingface.co/spaces/imaosglobal/ima-space"
