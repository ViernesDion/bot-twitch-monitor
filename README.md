# 🤖 Twitch Live Monitor Bot

Um bot assíncrono desenvolvido em Python para monitorar o status de transmissões na Twitch de forma contínua, enviando notificações push em tempo real para o celular sempre que um streamer entra ao vivo ou troca de jogo.

## 🚀 Tecnologias Utilizadas
* **Python 3:** Linguagem principal do projeto.
* **asyncio:** Para rodar o loop de monitoramento de forma assíncrona, sem travar o sistema.
* **TwitchAPI:** Integração oficial e autenticação via OAuth2 com os servidores da Twitch.
* **Ntfy (ntfy.sh):** Sistema de pub/sub para envio de notificações push via requisições HTTP (`requests`).

## ⚙️ Como funciona
O bot roda em um servidor em background (daemon), consultando a Twitch a cada 60 segundos. Ele possui um sistema de "memória" em memória RAM para comparar o status atual da live com o status anterior, disparando alertas apenas quando ocorrem mudanças (Início da live, Troca de categoria/jogo ou Encerramento da live).

## 🔒 Segurança
As credenciais da API (`CLIENT_ID` e `CLIENT_SECRET`) foram isoladas utilizando variáveis de ambiente (`os.environ`), garantindo que dados sensíveis não fiquem expostos no código-fonte.
