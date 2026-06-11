# Twitch Live Notifier 🚀

A lightweight and efficient monitoring bot developed in Python to notify the status of Twitch streamers in real-time via Ntfy.sh.

## 💡 Motivation

Developed to solve a personal problem: native Twitch notifications do not always deliver the alert at the exact moment the stream starts. Additionally, this project served as a practical study for cloud infrastructure concepts, Git, and automation.

## 🛠️ Technologies Used

* **Language:** Python
* **Integrations:** Twitch API, Ntfy.sh (notifications)
* **Infrastructure:** Render (Web Service)
* **Monitoring:** UptimeRobot (to prevent free tier hibernation)
* **Version Control:** Git & GitHub

## ⚙️ How the Infrastructure Works

Render's free plan hibernates inactive services. To ensure the bot runs 24/7, I implemented an internal "dummy server" that:

1. Responds to `GET` and `HEAD` requests.
2. Keeps the service port continually active for UptimeRobot.
3. Runs on a separate `threading` to avoid blocking the bot's main logic.

## 🚀 Project Status

✅ Active monitoring ✅ Real-time notifications ✅ Automated deployment with anti-hibernation protection

---
*Project developed as part of the Computer Science portfolio.*
