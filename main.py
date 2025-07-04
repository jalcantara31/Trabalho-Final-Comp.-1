#a funcao usuario recebe o nome do usuario e adiciona o nome ao arquivo usuarios.txt. Alem do nome e adicionado o numero de vitorias, que comeca em 0
def usuario():
    nome = input("Digite seu nome: ").lower()
    f = open('usuarios.txt', 'a')
    f.write(nome + ':0\n')
    print("Olá,", nome, ",bem-vindo!!")
    f.close()
    return nome


#a funcao mostrar_usuarios le o arquivo usuarios.txt e mostra o conteudo do arquivo
def mostrar_usuarios():
    try:
        f=open('usuarios.txt','r')
        conteudo_para_mostrar = ""
        for linha in f:
            conteudo_para_mostrar = conteudo_para_mostrar + linha
        f.close()
        return(f"\n{conteudo_para_mostrar}")
    except FileNotFoundError:
        return('Nao existem usuarios cadastrados')


#a funcao instrucoes mostra as regras do jogo
def instrucoes():
    print("\nInstruções do Jogo:")
    print("O peao se move apenas para frente")
    print("As torres se move em linhas retas quantas casas quiser")
    print("Os bispos se movem na diagonal quantas casas quiser")
    print("Os cavalos se movem em L")
    print("A rainha se move em linhas retas ou em diagonais quantas casas quiser")
    print("O Rei se move apenas 1 casa para qualquer direção")
    print("Quando um peão chega ao extremo do tabuleiro o jogador pode trocá-lo por qualquer outra peca, desde que nao seja por um rei")
    print('\n')

#a funcao menu exibe as opcoes que o usuario pode escolher, recebe a escolha do usuario e retorna a opcao escolhida
def menu():
    print("\nEscolha uma opcao:")
    print("1. Criar Usuario")
    print("2. Instrucoes do Jogo")
    print("3. Sair")
    print("4. Jogar")
    print("5. Mostrar usuarios e seus numeros de vitorias")
    op = input("Digite o numero da opcao: ")
    return op


#a funcao criar_tabuleiro cria o tabuleiro de xadrez padrao utilizando uma lista de listas, onde cada elemento representa uma peca ou casa vazia
def criar_tabuleiro():
    tabuleiro = [
        ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
        ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
        ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
        ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
    return tabuleiro
#a nomenclatura utilizada para cada peca foi escolhida com base na oficial do xadrez. P: Peão ; R: Torre ; N: Cavalo ; B: Bispo ; Q: Rainha ; K: Rei. b: Pretas ; w: Brancas
# wP, por exemplo, representa o peao branco

#a funcao exibir tabuleiro printa o proprio tabuleiro junto com as coordenadas das linhas e colunas
def exibir_tabuleiro(tabuleiro):
    print("\n  a  b  c  d  e  f  g  h") 
    for i in range(8):
        linha = str(8 - i) + " "
        for j in range(8):
            linha += tabuleiro[i][j] + ' '
        print(linha + str(8 - i))
    print("  a  b  c  d  e  f  g  h\n")


#a funcao coordenada recebe uma coordenada no estilo 'e2' e retorna a linha e coluna do tabuleiro. funciona como um "tradutor"
def coordenada(coord):
    colunas={'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    if len(coord) != 2 or not (coord[0] in colunas) or not (coord[1] in '12345678'):
        print("Coordenada invlida. Use o formato 'letraNumero' (ex: e2).")
        return None, None
    coluna = colunas[coord[0]] #utiliza o dicionario
    linha=8-int(coord[1]) 
    return linha,coluna


#a funcao mover peca recebe o tabuleiro -> pergunta a origem da peca e o destino da peca -> traduz as coordenadas -> 
# ->verifica se tem uma peca na coordenada -> coloca a peca que estava na posicao de origem na posicao de destino e define a posicao de origem como '  '
def mover_peca(tabuleiro):
    movimento_valido = 0 #0 -> False ; 1 -> True
    while not movimento_valido:
        origem = input("Digite a posicao da peça que deseja mover (ex: e2): ").lower()
        destino = input("Digite a posicao de destino (ex: e4): ").lower()

        linha_origem, coluna_origem = coordenada(origem)
        linha_destino, coluna_destino = coordenada(destino)

        if linha_origem is None or linha_destino is None:
            continue

        peca = tabuleiro[linha_origem][coluna_origem]

        if peca == '  ':
            print("Tente novamente")
        elif linha_origem == linha_destino and coluna_origem == coluna_destino:
            print("Tente novamente")
        else:
            resultado = verificar_movimento(tabuleiro, linha_origem, coluna_origem, linha_destino, coluna_destino)
            if resultado == False:
                print("Movimento invalido. Tente novamente")
            elif resultado == 'promocao':
                while True:
                    promocao = input("Para qual peça deseja promover o peão? (Q, R, B, N): ").upper()
                    if promocao in ['Q', 'R', 'B', 'N']:
                        tabuleiro[linha_destino][coluna_destino] = 'w' + promocao
                        tabuleiro[linha_origem][coluna_origem] = '  '
                        movimento_valido = 1
                        break
                    else:
                        print("Escolha inválida. Use Q (Rainha), R (Torre), B (Bispo), H (Cavalo).")
            else:
                tabuleiro[linha_destino][coluna_destino] = peca
                tabuleiro[linha_origem][coluna_origem] = '  '
                movimento_valido = 1

    exibir_tabuleiro(tabuleiro)


#verifica se o movimento da peca condiz com as regras do jogo
def verificar_movimento(tabuleiro, linha_origem, coluna_origem, linha_destino, coluna_destino):
    peca = tabuleiro[linha_origem][coluna_origem]
    if peca == 'bR' or peca == 'wR':
        # Verifica se a torre se move corretamente
        if linha_origem == linha_destino or coluna_origem == coluna_destino:
            return True
    elif peca == 'bB' or peca == 'wB':
        if abs(linha_origem - linha_destino) == abs(coluna_origem - coluna_destino):
            return True
    elif peca == 'bN' or peca == 'wN':
        if (abs(coluna_origem - coluna_destino == 2) and abs(linha_origem - linha_destino == 1) or (abs(coluna_origem - coluna_destino == 1) and abs(linha_origem - linha_destino == 2))):
            return True
    elif peca == 'bP':
        if (coluna_destino - coluna_origem == 0 and linha_destino - linha_origem == 1 and tabuleiro[linha_destino][coluna_destino] == '  '):
            return True
        if (coluna_destino - coluna_origem == 0 and linha_destino - linha_origem == 2 and linha_origem == 1 and tabuleiro[linha_destino][coluna_destino] == '  ' and tabuleiro[linha_destino - 1][coluna_destino] == '  '):
            return True
        if (abs(coluna_destino - coluna_origem) == 1 and linha_destino - linha_origem == 1 and tabuleiro[linha_destino][coluna_destino] != '  '):
            return True
    elif peca == 'wP':
        if (coluna_destino - coluna_origem == 0 and linha_destino - linha_origem == -1 and tabuleiro[linha_destino][coluna_destino] == '  ' and linha_destino != 0):
            return True
        if (coluna_destino - coluna_origem == 0 and linha_destino - linha_origem == -2 and linha_origem == 6 and tabuleiro[linha_destino][coluna_destino] == '  ' and tabuleiro[linha_destino + 1][coluna_destino] == '  ' and linha_destino != 0):
            return True
        if (abs(coluna_destino - coluna_origem) == 1 and linha_destino - linha_origem == -1 and tabuleiro[linha_destino][coluna_destino] != '  ' and linha_destino != 0):
            return True
        if linha_destino == 0:
            if (coluna_destino - coluna_origem == 0 and linha_destino - linha_origem == -1 and tabuleiro[linha_destino][coluna_destino] == '  ') or \
               (abs(coluna_destino - coluna_origem) == 1 and linha_destino - linha_origem == -1 and tabuleiro[linha_destino][coluna_destino] != '  '):
                return 'promocao'
        else:
            return False
        #adicionar en passant
    elif peca == 'bK' or peca == 'wK':
        if abs(linha_origem - linha_destino) <= 1 and abs(coluna_origem - coluna_destino) <= 1:
            return True
    elif peca == 'wQ' or peca == 'bQ':
        if linha_origem == linha_destino or coluna_origem == coluna_destino:
            return True
        if abs(linha_origem - linha_destino) == abs(coluna_origem - coluna_destino):
            return True
    return False
        

# A funcao fimdejogo verifica em todas as rodadas se ainda existe um rei branco ou preto no tabuleiro
def fimdejogo(tabuleiro):
    rei_branco = 0
    rei_preto = 0
    for linha in tabuleiro:
        for peca in linha:
            if peca == 'wK':
                rei_branco = 1 #True
            if peca == 'bK':
                rei_preto = 1 #True
    
    if not rei_preto: #if rei preto == 0
        print("Parabens! As peças brancas venceram!")
        return 1 #retorna True
    elif not rei_branco: #if rei branco ==0
        print("Parabens! As peças pretas venceram!")
        return 1 #retorna True
    return 0 #retorna False


#A funcao verificar vencedor verifica se existe um rei branco ou preto no tabuleiro
def verificarvencedor(tabuleiro): 
    rei_branco = 0
    rei_preto = 0
    for linha in tabuleiro:
        for peca in linha:
            if peca == 'wK':
                rei_branco = 1
            if peca == 'bK':
                rei_preto = 1
    if not rei_preto:
        return 'Brancas'
    elif not rei_branco:
        return 'Pretas'
    return None


#a funcao adicionar_vitoria recebe o nome do vencedor e adiciona para ele uma vitoria no arquivo usuarios.txt
def adicionar_vitoria(vencedor):
    linhas_do_arquivo = []
    try:
        f_leitura = open('usuarios.txt', 'r')
        for linha in f_leitura:
            linhas_do_arquivo.append(linha)
        f_leitura.close()
    except FileNotFoundError:
        print("O arquivo de usuarios nao foi encontrado. Um novo arquivo sera criado")
        linhas_do_arquivo = []
    novas_linhas_para_escrever = []
    for linha_existente in linhas_do_arquivo:
        linha_sem_quebra = linha_existente.replace('\n', '') #o replace('\n','') retira a quebra de linha no final da string para transformar em uma lista
        partes = linha_sem_quebra.split(':') #cria uma lista chamada partes onde o primeiro elemento e o nome do usuario e o segundo elemento o numero de vitorias
        
        if len(partes) == 2:
            nome_do_usuario = partes[0]
            num_vitorias = int(partes[1])
            
            if nome_do_usuario == vencedor:
                num_vitorias += 1 #adiciona uma vitoria ao usuario
            novas_linhas_para_escrever.append(nome_do_usuario + ':' + str(num_vitorias) + '\n')
        else:
            novas_linhas_para_escrever.append(linha_existente)

    f = open('usuarios.txt', 'w')
    for linha_a_escrever in novas_linhas_para_escrever:
        f.write(linha_a_escrever)
    f.close()


#a funcao verificar_usuario_existe recebe o nome do usuario e verifica se ele esta no arquivo usuarios.txt
def verificar_usuario_existe(usuario):
    try:
        f_leitura = open('usuarios.txt', 'r')
        for linha in f_leitura:
            linha_sem_quebra = linha.replace('\n', '')
            partes = linha_sem_quebra.split(':')
            if len(partes) == 2:
                nome_do_usuario = partes[0]
                if nome_do_usuario == usuario:
                    f_leitura.close()
                    return 1
        f_leitura.close()
    except FileNotFoundError:
        return 0
    return 0


import random as rdm
# a funcao jogo organiza todas as funcoes relacionadas a partida, dentre elas as de tabuleiro
def jogo():
    jogadores_validados = 0 # 0 -> false ; 1 -> true
    jogadorBrancas = "" 
    jogadorPretas = ""

    while not jogadores_validados: #enquanto nao define os jogadores
        jogador1 = input('Jogador 1: ').lower()
        if not verificar_usuario_existe(jogador1):
            print("Usuario nao cadastrado")
            return None
        
        jogador2 = input('Jogador 2: ').lower()
        if not verificar_usuario_existe(jogador2):
            print("Usuario nao encontrado")
            return None
        
        if jogador2 == jogador1:
            print("Nao e possivel jogar contra si mesmo")
        else:
            jogadores_validados = 1 
    brancas=rdm.choice([1,2])
    if brancas == 1:
        jogadorBrancas=jogador1
        jogadorPretas=jogador2
        print('Jogador 1: Brancas \nJogador 2: Pretas')
    elif brancas == 2:
        jogadorBrancas=jogador2
        jogadorPretas=jogador1
        print('Jogador 1: Pretas \nJogador 2: Brancas')
    tabuleiro = criar_tabuleiro()
    exibir_tabuleiro(tabuleiro)
    
    turno_atual = 'Brancas'

    while True:
        if turno_atual=='Brancas':
            print(f"E a vez de {jogadorBrancas}")
        elif turno_atual=='Pretas':
            print(f"E a vez de {jogadorPretas}")
        mover_peca(tabuleiro)
        
        if fimdejogo(tabuleiro): #se a funcao fimdejogo retornar 1(True)-> o jogo acabou
            cor_vencedora = verificarvencedor(tabuleiro)
            vencedor = None
            if cor_vencedora == 'Brancas':
                vencedor = jogadorBrancas
            elif cor_vencedora == 'Pretas':
                vencedor = jogadorPretas
            
            if vencedor:
                adicionar_vitoria(vencedor)
            break
        
        turno_atual = 'Pretas' if turno_atual == 'Brancas' else 'Brancas'

    return vencedor


def main(): #funcao principal
    while True:
        op = menu() # chama a funcao menu para definir a escolha do usuario
        if op == '1': # criar usuario
            nome = usuario()
            print(nome, "seu usuario foi criado com sucesso")
        elif op == '2': #instrucoes do jogo
            instrucoes()
        elif op == '3': #sair
            print("Obrigado por jogar")
            break
        elif op == '4': #jogar
            vencedor = jogo()
            if vencedor:
                print("Vitoria de", vencedor)
        elif op == '5': #mostrar usuarios cadastrados e seu numero de vitorias
            print(mostrar_usuarios())
        else:
            print("Opcao Invalida")

if __name__ == "__main__": # exigencia do enunciado do trabalho
    main()