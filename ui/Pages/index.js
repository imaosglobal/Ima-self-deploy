import { useState, useEffect } from "react";
import axios from "axios";

export default function Home() {
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");
  const [userId] = useState("user1");
  const [preferences, setPreferences] = useState({gender: "female", occupation: "engineer"});

  useEffect(() => {
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
