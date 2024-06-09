import socket
import os

def clear_screen():
    """Função para limpar a tela."""
    # Verifica o sistema operacional e usa o comando apropriado para limpar a tela
    if os.name == 'nt':  # Para Windows
        os.system('cls')
    else:               # Para Unix/Linux/MacOS
        os.system('clear')

def main():
    host = '127.0.0.1'  # Host onde o servidor está rodando
    port = 5000         # Porta em que o servidor está escutando

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Conectado ao servidor Jokenpô")

    try:
        # Recebe a solicitação do servidor para inserir o ID
        server_message = client_socket.recv(1024).decode('utf-8')
        print(server_message)

        # Solicita o ID do jogador
        player_id = input("Seu ID: ").strip()
        client_socket.send(player_id.encode('utf-8'))

        while True:

            clear_screen()

            # Solicita a escolha do jogador
            print("Escolha uma opção:")
            print("0 - Pedra")
            print("1 - Papel")
            print("2 - Tesoura")
            player_choice = input("Sua escolha: ").strip()

            # Verifica se o usuário deseja sair
            if player_choice.lower() in ['exit', 'quit', 'sair']:
                print("Saindo do jogo...")
                break

            try:
                player_choice_int = int(player_choice)
                if player_choice_int not in [0, 1, 2]:
                    raise ValueError()
            except ValueError:
                print("Entrada inválida. Por favor, escolha 0, 1 ou 2.")
                os.system('pause')
                continue

            # Envia a escolha do jogador para o servidor
            client_socket.send(player_choice.encode('utf-8'))

            # Recebe a resposta do servidor
            response = client_socket.recv(1024).decode('utf-8')
            print(response)
            
            os.system('pause')

    finally:
        # Fecha a conexão do cliente
        client_socket.close()

if __name__ == "__main__":
    main()
