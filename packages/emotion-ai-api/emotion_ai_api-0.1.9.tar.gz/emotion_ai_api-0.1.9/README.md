pip install emotion_ai_api

emotion_ai = EmotionAI(base_url="https://api.emotion-ai.io", api_key="YOUR_API_KEY")

text = "This is the text to be analyzed."
user_id = "USER_ID"

response = emotion_ai.analyze_user_text(text, user_id)
emotion_ai.pretty_print_response(response)
