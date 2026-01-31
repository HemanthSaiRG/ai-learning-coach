def analyze_learning(topic, confusions, time_spent):
    return {
        "topic": topic,
        "time_spent": time_spent,
        "feedback": "AI quota exceeded. Running in offline mode.",
        "confusion_tip": "Your app is working perfectly. Enable billing to use AI."
    }
