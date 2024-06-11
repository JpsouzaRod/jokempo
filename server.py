import socket
import threading
import random

# Dicionário para armazenar o placar de cada jogador por ID
player_scores = {}

# Lock para garantir a segurança ao acessar o dicionário de placar
score_lock = threading.Lock()

def jokenpo_result(player_choice, machine_choice, client_wins, client_losses):
    """Função para determinar o resultado do jogo Jokenpô."""
    # Condições de vitória
    if (player_choice == 0 and machine_choice == 2) or \
       (player_choice == 1 and machine_choice == 0) or \
       (player_choice == 2 and machine_choice == 1):
        result = "Você venceu!"
        client_wins += 1
    elif player_choice == machine_choice:
        result = "Empate!"
    else:
        result = "Você perdeu!"
        client_losses += 1
    
    return result, client_wins, client_losses

def handle_client(client_socket):
    """Função que lida com a conexão do cliente."""
    # Solicita o ID do jogador
    client_socket.send("Por favor, insira seu ID: ".encode('utf-8'))
    player_id = client_socket.recv(1024).decode('utf-8').strip()
    
    with score_lock:
        if player_id not in player_scores:
            player_scores[player_id] = (0, 0)  # Inicializa placar (vitórias, derrotas)
        client_wins, client_losses = player_scores[player_id]

    try:
        while True:
            # Recebe a escolha do jogador
            request = client_socket.recv(1024).decode('utf-8').strip()
            if not request:
                break
            
            player_choice = int(request)
            
            # Gera a escolha da máquina
            machine_choice = random.randint(0, 2)
            choices = ["Pedra", "Papel", "Tesoura"]
            
            # Determina o resultado do jogo
            result, client_wins, client_losses = jokenpo_result(player_choice, machine_choice, client_wins, client_losses)
            response = f"Você escolheu {choices[player_choice]}, Máquina escolheu {choices[machine_choice]}.\n{result}\n"
            
            response += f"Seu placar: {client_wins} Vitórias, {client_losses} Derrotas\n"

            with score_lock:
                player_scores[player_id] = (client_wins, client_losses)

            # Envia a resposta de volta para o cliente
            client_socket.send(response.encode('utf-8'))
    finally:
        # Fecha a conexão do cliente
        client_socket.close()

def start_server(host, port):
    """Função para iniciar o servidor socket."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Servidor escutando em {host}:{port}")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Conexão aceita de {addr}")
        # Cria uma nova thread para lidar com a conexão do cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    HOST, PORT = 'localhost', 5000  # Define o host e a porta do servidor
    start_server(HOST, PORT)
