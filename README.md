# Twitch Live Notifier 🚀

Um bot de monitoramento leve e eficiente, desenvolvido em Python, para notificar o status de streamers da Twitch em tempo real via [Ntfy.sh](https://ntfy.sh/).

## 💡 Motivação
Desenvolvido para resolver um problema pessoal: as notificações nativas da Twitch nem sempre entregam o alerta no momento exato em que a live inicia. Além disso, este projeto serviu como estudo prático para conceitos de infraestrutura em nuvem, Git e automação.

## 🛠 Tecnologias Utilizadas
*   **Linguagem:** Python
*   **Integrações:** Twitch API, Ntfy.sh (notificações)
*   **Infraestrutura:** Render (Web Service)
*   **Monitoramento:** UptimeRobot (para evitar hibernação do plano free)
*   **Versionamento:** Git & GitHub

## ⚙️ Como funciona a Infraestrutura
O plano gratuito do Render hiberna serviços inativos. Para garantir que o bot rode 24/7, implementei um "servidor fake" interno que:
1.  Responde a requisições `GET` e `HEAD`.
2.  Mantém a porta do serviço sempre ativa para o UptimeRobot.
3.  Executa em uma `threading` separada para não bloquear a lógica principal do bot.

## 🚀 Status do Projeto
✅ Monitoramento ativo
✅ Notificações em tempo real
✅ Deploy automatizado com proteção contra hibernação

---
*Projeto desenvolvido como parte do portfólio de Ciência da Computação.*
