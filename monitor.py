import os
import asyncio
import requests
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first

CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.environ.get('TWITCH_CLIENT_SECRET')
STREAMER_NOME = os.environ.get('STREAMER_NOME', 'cellbit')
TOPICO_NTFY = os.environ.get('TOPICO_NTFY', 'bot_twitch')

def enviar_notificacao(mensagem):
		url = f"https://ntfy.sh/{TOPICO_NTFY}"
		requests.post(url,
			data=mensagem.encode('utf-8'),
			headers={
				"title": f"Monitor: {STREAMER_NOME}",
				"Tags": "video_game,bell"
			}
		)

async def monitorar_streamer():
		twitch = await Twitch(CLIENT_ID, CLIENT_SECRET)
		print(f"bot iniciado!!! Monitorando o canal: {STREAMER_NOME}...")

		user = await first(twitch.get_users(logins=[STREAMER_NOME]))
		if not user:
			print("Erro: Streamer não encontrado.")
			await twitch.close()
			return

		estado_anterior_online = False
		jogo_anterior = None

		try:
			while True:
				stream = await first(twitch.get_streams(user_id=user.id))

				if stream:
					jogo_atual = stream.game_name
					if not estado_anterior_online:
						msg = f"{STREAMER_NOME} está ONLINE!!\n Jogando: {jogo_atual}"
						print(msg)
						enviar_notificacao(msg)
						estado_anterior_online = True
						jogo_anterior = jogo_atual

					elif jogo_atual != jogo_anterior:
		     				msg = f"{STREAMER_NOME} trocou de jogo!!.\n Novo jogo: {jogo_atual}"
		     				print(msg)
		     				enviar_notificacao(msg)
		     				jogo_anterior = jogo_atual
				else:
					if estado_anterior_online:
			   			msg = f"{STREAMER_NOME} encerrou a live."
			   			print(msg)
			   			enviar_notificacao(msg)
			   			estado_anterior_online = False
			  	 		jogo_anterior = None

				await asyncio.sleep(60)

		except KeyboardInterrupt:
				print("\n Monitoramento encerrado pelo usuário")
		finally:
				await twitch.close()
if __name__ == '__main__':
				asyncio.run(monitorar_streamer())
