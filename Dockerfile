# ১. পাইথন এনভায়রনমেন্ট সেটআপ
FROM python:3.9

# ২. সার্ভারের ভেতরে একটি ফোল্ডার তৈরি
WORKDIR /code

# ৩. আপনার সব ফাইল সার্ভারে কপি করা
COPY . .

# ৪. প্রয়োজনীয় লাইব্রেরি ইন্সটল করা
RUN pip install --no-cache-dir -r requirements.txt

# ৫. পোর্টের এক্সেস দেওয়া (Hugging Face-এর জন্য ৭৮৬০ জরুরি)
EXPOSE 7860

# ৬. বট রান করার মেইন কমান্ড
CMD ["python", "main.py"]
