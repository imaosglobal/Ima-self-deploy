#!/bin/bash
set -e

echo "🚀 בדיקת מצב Ima ב-Hugging Face Space..."

# 1️⃣ טען משתנים מה‑.env
if [ ! -f ".env" ]; then
    echo "❌ חסר קובץ .env עם HF_SPACE_URL ו-HF_TOKEN"
    exit 1
fi
source .env

if [ -z "$HF_SPACE_URL" ] || [ -z "$HF_TOKEN" ]; then
    echo "❌ HF_SPACE_URL או HF_TOKEN ריקים"
    exit 1
fi

echo "🔹 Space URL: $HF_SPACE_URL"

# 2️⃣ בדיקת Build אחרון מה-Logs של HF
echo "🔹 בדיקת Logs אחרונים ב-HF Space..."
curl -s -H "Authorization: Bearer $HF_TOKEN" "$HF_SPACE_URL/logs" | tail -n 20

# 3️⃣ בדיקה אם ה-UI פעיל (אם sleeping, יתחיל להתעורר)
echo "🔹 מנסה לגשת ל-UI..."
status_code=$(curl -o /dev/null -s -w "%{http_code}\n" "$HF_SPACE_URL")
if [ "$status_code" -eq 200 ]; then
    echo "✅ ה-UI פעיל"
else
    echo "⚠️ ה-UI עדיין sleeping או בעיה. קוד HTTP: $status_code"
fi

# 4️⃣ בדיקה פשוטה ל-API (שולח הודעה לדמו Ima)
echo "🔹 בודק תגובה מ-Ima..."
response=$(curl -s -X POST "$HF_SPACE_URL/run/predict" \
    -H "Authorization: Bearer $HF_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"data":["בדיקת מצב"]}')

if [[ "$response" == *"בדיקת מצב"* ]] || [[ "$response" == *"error"* ]]; then
    echo "✅ קבלת תשובה מה-API"
else
    echo "❌ אין תגובה מה-API או בעיה בתקשורת"
fi

echo "🎉 בדיקה הסתיימה!"
