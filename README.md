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

## 🧩 Architecture (OOP)

The bot was refactored following object-oriented principles, with each class having a single responsibility:

* **`Config`** — Loads and validates environment variables.
* **`Notifier`** — Sends notifications to Ntfy.sh.
* **`KeepAliveServer`** — The internal dummy HTTP server (anti-hibernation).
* **`StreamerState`** — Encapsulates the online/game state of a single channel.
* **`TwitchStreamMonitor`** — Orchestrates the monitoring loop.

## 📡 Monitoring Multiple Channels

You can now monitor several streamers at once. Set the `STREAMERS` environment variable with a comma-separated list:

```
STREAMERS=cellbit,gaules,loud_coringa
```

The legacy `STREAMER_NOME` variable is still supported for a single channel.

### Environment Variables

| Variable | Description | Default |
| --- | --- | --- |
| `TWITCH_CLIENT_ID` | Twitch application client ID | *(required)* |
| `TWITCH_CLIENT_SECRET` | Twitch application client secret | *(required)* |
| `STREAMERS` | Comma-separated list of channels to monitor | `cellbit` |
| `TOPICO_NTFY` | Ntfy.sh topic for notifications | `bot_twitch` |
| `INTERVALO_SEGUNDOS` | Polling interval in seconds | `60` |
| `PORT` | Keep-alive server port | `8080` |

## 🚀 Project Status

✅ Active monitoring ✅ Multi-channel support ✅ Real-time notifications ✅ Automated deployment with anti-hibernation protection

---
*Project developed as part of the Computer Science portfolio.*
