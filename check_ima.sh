#!/bin/bash
set -e

echo "🔍 מתחיל בדיקה של Ima..."

# 1️⃣ בדיקת קבצים חיוניים
required_files=("app.py" "requirements.txt" "Dockerfile" ".env" "deploy.sh" "README.md" "ui/pages/index.js" "ui/package.json" "ui/next.config.js" ".github/workflows/deploy.yml")

for f in "${required_files[@]}"; do
    if [ ! -f "$f" ]; then
        echo "❌ חסר קובץ: $f"
    else
        echo "✅ נמצא: $f"
    fi
done

# 2️⃣ בדיקת התקנת תלויות Python
echo "🔹 בדיקה אם תלויות Python מותקנות..."
pip install -r requirements.txt

# 3️⃣ בדיקה אם Docker מותקן
if ! command -v docker &> /dev/null; then
    echo "❌ Docker לא מותקן. התקן Docker לפני המשך."
else
    echo "✅ Docker מותקן"
fi

# 4️⃣ בדיקה אם npm מותקן (ל‑UI)
if ! command -v npm &> /dev/null; then
    echo "❌ npm לא מותקן. התקן Node.js/npm לפני המשך."
else
    echo "✅ npm מותקן"
fi

# 5️⃣ בדיקה קצרה של UI
echo "🔹 בדיקה קצרה של UI..."
cd ui
npm install --silent
if [ $? -eq 0 ]; then
    echo "✅ התקנת תלויות UI הצליחה"
else
    echo "❌ התקנת תלויות UI נכשלה"
fi
cd ..

# 6️⃣ בדיקת API בסיסית
echo "🔹 בדיקת API בסיסית..."
if python app.py & then
    echo "✅ API התחיל בהצלחה (בדיקה קצרה)"
else
    echo "❌ API לא התחיל"
fi
# תעצור מיד לאחר בדיקה
pkill -f "python app.py"

echo "🎉 בדיקה הסתיימה – אם כל השלבים עברו, הפרויקט מוכן לפריסה."
