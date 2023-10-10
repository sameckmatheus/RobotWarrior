# A classe Part representa uma parte de um robô, como a cabeça, o braço ou a arma.
class Part:
    # O método _init_ é o construtor da classe, que recebe os atributos da parte como parâmetros.
    def _init_(self, name: str, attack_level=0, defense_level=0, energy_consumption=0):
        # Os atributos são definidos como variáveis de instância usando o prefixo self.
        self.name = name # O nome da parte
        self.attack_level = attack_level # O nível de ataque da parte
        self.defense_level = defense_level # O nível de defesa da parte
        self.energy_consumption = energy_consumption # O consumo de energia da parte

    # O método get_status_dict retorna um dicionário com as informações da parte, como o nome, o status, o ataque, a defesa e o consumo de energia.
    def get_status_dict(self):
        # O nome da parte é formatado para ser usado como uma chave no dicionário, substituindo os espaços por underscores e deixando tudo em minúsculo.
        formatted_name = self.name.replace(" ", "_").lower()
        return {
            "{}_name".format(formatted_name): self.name.upper(), # O nome da parte em maiúsculo
            "{}_status".format(formatted_name): self.is_available(), # O status da parte, que é True se a defesa for menor ou igual a zero, ou False caso contrário
            "{}_attack".format(formatted_name): self.attack_level, # O nível de ataque da parte
            "{}_defense".format(formatted_name): self.defense_level, # O nível de defesa da parte
            "{}_energy_consump".format(formatted_name): self.energy_consumption, # O consumo de energia da parte
        }

    # O método reduce_defense reduz o nível de defesa da parte pelo nível de ataque dado como parâmetro, mas não deixa que fique negativo.
    def reduce_defense(self, attack_level):
        self.defense_level = max(0, self.defense_level - attack_level)

    # O método is_available retorna True se a defesa da parte for menor ou igual a zero, ou False caso contrário. Isso indica se a parte está disponível para ser usada ou não.
    def is_available(self):
        return self.defense_level <= 0


# A classe Robot representa um robô, que tem um nome, um código de cor, uma energia e uma lista de partes.
class Robot:
    # O método _init_ é o construtor da classe, que recebe o nome e o código de cor do robô como parâmetros.
    def _init_(self, name, color_code):
        self.name = name # O nome do robô
        self.color_code = color_code # O código de cor do robô
        self.energy = 100 # A energia inicial do robô
        self.parts = [ # A lista de partes do robô, que são objetos da classe Part
            Part("Head", attack_level=5, defense_level=10, energy_consumption=5), # A cabeça do robô
            Part("Weapon", attack_level=15, defense_level=0, energy_consumption=10), # A arma do robô
            Part("Left Arm", attack_level=3, defense_level=20, energy_consumption=10), # O braço esquerdo do robô
            Part("Right Arm", attack_level=6, defense_level=20, energy_consumption=10), # O braço direito do robô
            Part("Left Leg", attack_level=4, defense_level=20, energy_consumption=15), # A perna esquerda do robô
            Part("Right Leg", attack_level=8, defense_level=20, energy_consumption=15), # A perna direita do robô
        ]

    # O método get_part_status retorna um dicionário com as informações de todas as partes do robô, usando o método get_status_dict de cada parte.
    def get_part_status(self):
        part_status = {} # Um dicionário vazio para armazenar as informações das partes
        for part in self.parts: # Para cada parte na lista de partes do robô
            status_dict = part.get_status_dict() # Obter o dicionário com as informações da parte
            part_status.update(status_dict) # Atualizar o dicionário geral com as informações da parte
        return part_status # Retornar o dicionário geral

    # O método print_status imprime o status do robô, usando o código de cor, o nome, a energia e as informações das partes.
    def print_status(self):
        print(self.color_code) # Imprimir o código de cor do robô
        str_robot = robot_art.format(**self.get_part_status()) # Formatar a string robot_art com as informações das partes do robô
        self.greet() # Chamar o método greet para cumprimentar o usuário
        self.print_energy() # Chamar o método print_energy para imprimir a energia do robô
        print(str_robot) # Imprimir a string formatada com a arte do robô
        print(colors["white"]) # Imprimir a cor branca para voltar ao padrão

    # O método greet imprime uma saudação com o nome do robô
    def greet(self):
        print("Hello, my name is", self.name)

    # O método print_energy imprime a energia do robô em porcentagem
    def print_energy(self):
        print("We have", self.energy, " percent energy left")

    # O método is_there_available_part retorna True se há alguma parte do robô que está disponível para ser usada, ou False caso contrário. Ele usa o método is_available de cada parte para verificar isso.
    def is_there_available_part(self):
        for part in self.parts: # Para cada parte na lista de partes do robô
            if part.is_available(): # Se a parte está disponível
                return True # Retornar True
        return False # Se nenhuma parte está disponível, retornar False

    # O método is_on retorna True se a energia do robô é maior que zero, ou False caso contrário. Isso indica se o robô está ligado ou não.
    def is_on(self):
        return self.energy > 0

    # O método attack ataca um robô inimigo usando uma parte específica e mirando em outra parte do inimigo. Ele usa o método reduce_defense da parte atacada e reduz a energia do robô atacante pelo consumo de energia da parte usada.
    def attack(self, enemy_robot, part_to_use, part_to_attack):
        enemy_robot.parts[part_to_attack].reduce_defense(self.parts[part_to_use].attack_level) # Reduzir a defesa da parte atacada pelo nível de ataque da parte usada
        self.energy -= self.parts[part_to_use].energy_consumption # Reduzir a energia do robô atacante pelo consumo de energia da parte usada


# A função build_robot cria um novo robô, pedindo ao usuário o nome e a cor do robô. Ela usa a classe Robot para criar o objeto e o método print_status para imprimir o status do robô. Ela retorna o objeto criado.
def build_robot():
    robot_name = input("Robot name: ") # Pedir ao usuário o nome do robô
    color_code = choose_color() # Chamar a função choose_color para escolher uma cor para o robô
    robot = Robot(robot_name, color_code) # Criar um objeto da classe Robot com o nome e a cor escolhidos
    robot.print_status() # Imprimir o status do robô usando o método print_status
    return robot # Retornar o objeto criado


# A função choose_color pede ao usuário que escolha uma cor para o robô entre as cores disponíveis no dicionário colors. Ela verifica se a cor escolhida é válida e retorna o código de cor correspondente.
def choose_color():
    available_colors = colors # Atribuir o dicionário colors à variável available_colors
    print("Available colors:") # Imprimir as cores disponíveis
    for key, value in available_colors.items(): # Para cada chave e valor no dicionário available_colors
        print(value, key) # Imprimir o valor (código de cor) e a chave (nome da cor)
    print(colors["white"]) # Imprimir a cor branca para voltar ao padrão
    while True: # Entrar em um loop infinito
        chosen_color = input("Choose a color: ").lower() # Pedir ao usuário que escolha uma cor e converter para minúsculo
        if chosen_color in available_colors: # Se a cor escolhida está no dicionário available_colors
            return available_colors[chosen_color] # Retornar o valor (código de cor) correspondente à chave (nome da cor)
        else: # Se a cor escolhida não está no dicionário available_colors
            print("Invalid color choice. Please choose a valid color.") 


# A função play é a função principal do programa, que controla o fluxo do jogo.
def play():
    playing = True # Uma variável booleana que indica se o jogo está em andamento ou não
    print("Welcome to the game!") # Imprimir uma mensagem de boas-vindas
    print("Datas for player 1:") # Imprimir uma mensagem para o jogador 1
    robot_one = build_robot() # Chamar a função build_robot para criar o robô do jogador 1
    print("Datas for player 2:") # Imprimir uma mensagem para o jogador 2
    robot_two = build_robot() # Chamar a função build_robot para criar o robô do jogador 2

    current_robot = robot_one # Uma variável que armazena o robô que está atacando no momento
    enemy_robot = robot_two # Uma variável que armazena o robô que está sendo atacado no momento
    round_count = 0 # Uma variável que conta o número de rodadas do jogo

    while playing: # Enquanto o jogo estiver em andamento
        if round_count % 2 == 0: # Se o número de rodadas é par
            current_robot = robot_one # O robô do jogador 1 é o atacante
            enemy_robot = robot_two # O robô do jogador 2 é o alvo
        else: # Se o número de rodadas é ímpar
            current_robot = robot_two # O robô do jogador 2 é o atacante
            enemy_robot = robot_one # O robô do jogador 1 é o alvo

        current_robot.print_status() # Imprimir o status do robô atacante usando o método print_status

        try: # Tentar executar o bloco de código a seguir
            part_to_use = int(input("What part should I use to attack? Choose a number part: ")) # Pedir ao usuário que escolha uma parte para usar no ataque e converter para um número inteiro
            part_to_attack = int(input("Which part of the enemy should we attack? Choose an enemy number part to " 
                                       "attack: ")) # Pedir ao usuário que escolha uma parte do inimigo para atacar e converter para um número inteiro
        except ValueError: # Se ocorrer um erro de valor, ou seja, se o usuário não digitar um número válido
            print("Invalid input. Please enter a number.") # Imprimir uma mensagem de erro
            continue # Continuar para a próxima iteração do loop, sem executar o resto do código

        if 0 <= part_to_use <= 5 and 0 <= part_to_attack <= 5: # Se os números escolhidos estão entre 0 e 5, ou seja, se são partes válidas
            current_robot.attack(enemy_robot, part_to_use - 1, part_to_attack - 1) # Chamar o método attack do robô atacante, passando o robô alvo e as partes escolhidas como parâmetros. Note que subtraímos 1 dos números porque as listas começam em zero.
            round_count += 1 # Incrementar o contador de rodadas em 1

            if not enemy_robot.is_on() or not enemy_robot.is_there_available_part(): # Se o robô alvo não está ligado ou não tem nenhuma parte disponível, ou seja, se ele foi derrotado
                playing = False # Mudar a variável playing para False, encerrando o loop
                print() # Imprimir uma linha em branco
                print(f"Congratulations, {current_robot.name.upper()} wins!!!") # Imprimir uma mensagem de parabéns para o robô vencedor
        else: # Se os números escolhidos não estão entre 0 e 5, ou seja, se são partes inválidas
            print("Invalid part number. Please choose a number between 0 and 5.") # Imprimir uma mensagem de erro


# Robot art and colors 
# Essa parte do código define uma string com a arte do robô e um dicionário com as cores disponíveis para os robôs. Esses valores são usados nas funções e métodos anteriores para imprimir os robôs na tela.
robot_art = r""" 
    0: {head_name}
      Is available: {head_status}
      Attack: {head_attack}
      Defense: {head_defense}
      Energy consumption: {head_energy_consump}
              ^
              |                  |1: {weapon_name}
              |                  |Is available: {weapon_status}
     ____     |    ____          |Attack: {weapon_attack}
    |oooo|  ____  |oooo| ------> |Defense: {weapon_defense}
    |oooo| '    ' |oooo|         |Energy consumption: {weapon_energy_consump}
    |oooo|/\_||_/\|oooo|
    `----' / __ \  `----'           |2: {left_arm_name}
   '/  |#|/\/__\/\|#|  \'           |Is available: {left_arm_status}
   /  \|#|| |/\| ||#|/  \           |Attack: {left_arm_attack}
  / \_/|_|| |/\| ||_|\_/ \          |Defense: {left_arm_defense}
 |_\/    O\=----=/O    \/_|         |Energy consumption: {left_arm_energy_consump}
 <_>      |=\__/=|      <_> ------> |
 <_>      |------|      <_>         |3: {right_arm_name}
 | |   ___|======|___   | |         |Is available: {right_arm_status}
// \\ / |O|======|O| \  //\\        |Attack: {right_arm_attack}
|  |  | |O+------+O| |  |  |        |Defense: {right_arm_defense}
|\/|  \_+/        \+_/  |\/|        |Energy consumption: {right_arm_energy_consump}
\__/  _|||        |||_  \__/
      | ||        || |          |4: {left_leg_name}
     [==|]        [|==]         |Is available: {left_leg_status}
     [===]        [===]         |Attack: {left_leg_attack}
      >_<          >_<          |Defense: {left_leg_defense}
     || ||        || ||         |Energy consumption: {left_leg_energy_consump}
     || ||        || || ------> |
     || ||        || ||         |5: {right_leg_name}
   __|\_/|__    __|\_/|__       |Is available: {right_leg_status}
  /___n_n___\  /___n_n___\      |Attack: {right_leg_attack}
                                |Defense: {right_leg_defense}
                                |Energy consumption: {right_leg_energy_consump}
""" 

colors = {
    "black": '\x1b[90m', # Um código de cor para o preto
    "blue": '\x1b[94m', # Um código de cor para o azul
    "cyan": '\x1b[96m', # Um código de cor para o ciano
    "green": '\x1b[92m', # Um código de cor para o verde
    "magenta": '\x1b[95m', # Um código de cor para o magenta
    "red": '\x1b[91m', # Um código de cor para o vermelho
    "white": '\x1b[97m', # Um código de cor para o branco
    "yellow": '\x1b[93m', # Um código de cor para o amarelo
}

if __name__ == "__main__": # Se o nome do módulo é igual a "main_", ou seja, se o programa está sendo executado diretamente e não importado por outro módulo
    play() # Chamar a função play para iniciar o jogo