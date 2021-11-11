from random import sample

# PROBLEMAS:
# - TODA PARTIDA A MANILHA É A MESMA
# - O CÓDIGO QUEBRA ANTES DA PARTIDA TERMINAR (PRÓXIMO AO SCORE 6)

# A SER ADICIONADO:
# - Loop de 3 rodadas - OK
# - Marcador de pontos de rodada - OK
# - Loop de 12 partidas - OK
# - Marcador de pontos de partida - OK
# - Opção de pedir truco -> Opção de aceitar, fugir, ou pedir 6, 9 ou 12
# - Mão de 11

cartas_valor = ('4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3')
cartas_naipe = ('O', 'E', 'C', 'P')

# RODADAS (<= 3) <- PARTIDAS (12) <- JOGO (1)


class Game:
    def __init__(self, n_players):
        self.n_players = n_players
        self.use_card = self.seleciona_cartas()
        self.manilhas = self.manilha()

    def baralho(self):
        """Retorna todas as cartas usadas no truco"""
        cheap = []
        for naipe in cartas_naipe:
            for value in cartas_valor:
                cards_naipe_values = {naipe: value}
                cheap.append(cards_naipe_values)
        return cheap  # Lista de dicionários

    def seleciona_cartas(self):
        """Cartas a serem usadas nas rodadas"""
        cheap_cards = self.baralho()
        if self.n_players == 2:
            total_cards = sample(cheap_cards, 7)
        return total_cards  # Lista de dicinários

    def mao(self):
        """Retorna um mão de cartas para cada jogador"""
        hand = self.use_card
        players = {}
        if self.n_players == 2:
            players = {
                'player1': hand[:3],
                'player2': hand[3:6]
            }
        return players  # Dicionário

    def vira(self):
        """Define a carta tombada (a de cima do monte depois da distribuição das cartas, segundo a regra)"""
        card = self.use_card
        if self.n_players == 2:
            tombo_card = card[6]
        return tombo_card  # Dicionário

    def manilha(self):
        """Identifica as quatro maiores cartas do jogo"""
        tombo_card = self.vira()
        cheap_cards = self.baralho()

        for k in tombo_card.keys():
            tombo_value = tombo_card[k]

        manilha_cards = []
        # Procura e armazena as manilhas dentro de uma lista
        if tombo_value == '2' or tombo_value == '3':
            manilha_value = '4'
            for card in cheap_cards:
                for chave in card.keys():
                    if card[chave] == manilha_value:
                        manilha_cards.append(card)
        else:
            for value in cartas_valor:
                if value == tombo_value:
                    index = cartas_valor.index(value)
                    manilha_value = cartas_valor[index + 1]
            for card in cheap_cards:
                for chave in card.keys():
                    if card[chave] == manilha_value:
                        manilha_cards.append(card)

        return manilha_cards  # Lista de dicionários

    def partidas(self):

        player1_score = 0
        player2_score = 0

        for n in range(12):
            ganhador = self.rodadas()

            if ganhador == 'player1':
                player1_score += 1
                print(f'PLAYER1 SCORE: {player1_score}')
                if player1_score == 12:
                    print('\033[1;35mO PLAYER1 GANHOU O JOGO!!!\033[m')
            else:
                player2_score += 1
                print(f'PLAYER2 SCORE: {player2_score}')
                if player2_score == 12:
                    print('\033[1;33mO PLAYER2 GANHOU O JOGO!!!\033[m')

    def rodadas(self):
        hands = self.mao()

        player2_hand = hands['player2']
        player1_hand = hands['player1']

        ganhador = 'player1'
        rodadas_player1 = 0
        rodadas_player2 = 0

        for n in range(3):
            if 'player1' == ganhador:
                player1_choice = self.playerN_turn('player1', player1_hand)
                player2_choice = self.playerN_turn('player2', player2_hand)
            else:
                player2_choice = self.playerN_turn('player2', player2_hand)
                player1_choice = self.playerN_turn('player1', player1_hand)

            ganhador = self.ganhador_da_rodada(player1_choice, player2_choice)
            print(f'O {ganhador} ganhou a rodada.\n')

            # Verifica quem ganhou a partida
            if ganhador == 'player1':
                rodadas_player1 += 1
                if rodadas_player1 == 2:
                    print(f'\033[1;35mO PLAYER1 GANHOU A PARTIDA\033[m\n')
                    self.use_card = self.seleciona_cartas()
                    return 'player1'
            else:
                rodadas_player2 += 1
                if rodadas_player2 == 2:
                    print('\033[1;33mO PLAYER2 GANHOU A PARTIDA\033[m\n')
                    self.use_card = self.seleciona_cartas()
                    return 'player2'

    def ganhador_da_rodada(self, card1, card2):
        """Define o vencedor da rodada"""
        manilha_cards = self.manilhas
        # Chave e valor da carta 1
        for chave1 in card1.keys():
            index_card1_value = cartas_valor.index(card1[chave1])
            index_card1_naipe = cartas_naipe.index(chave1)

        # Chave e valor da carta 2
        for chave2 in card2.keys():
            index_card2_value = cartas_valor.index(card2[chave2])
            index_card2_naipe = cartas_naipe.index(chave2)

        if card1 in manilha_cards or card2 in manilha_cards:
            if card1 in manilha_cards and card2 in manilha_cards:
                if index_card1_naipe > index_card2_naipe:
                    msg = 'player1'
                else:
                    msg = 'player2'
            elif card1 in manilha_cards:
                msg = 'player1'
            else:
                msg = 'player2'
        else:
            if index_card1_value > index_card2_value:
                msg = 'player1'
            elif index_card1_value < index_card2_value:
                msg = 'player2'
            else:
                if index_card1_naipe > index_card2_naipe:
                    msg = 'player1'
                else:
                    msg = 'player2'
        return msg

    def playerN_turn(self, playerN, playerN_hand):
        cor = '\033[35m' if playerN == 'player1' else '\033[33m'
        print(f'{cor}Cartas do {playerN}: {playerN_hand}')
        choice_card = int(input('Escolha sua carta (com base na posição): '))
        playerN_choice = playerN_hand[choice_card]  # Remove carta escolhida
        playerN_hand.remove(playerN_hand[choice_card])
        print(f'{playerN_choice}\033[m\n')
        return playerN_choice


# Principal
n = int(input('\n\033[1;33mQual a quantidade de jogadores?\033[m '))
game = Game(n)
print(f'\n\033[1;32mTombo: {game.vira()}\033[m')
print(f'\033[1;34mManilhas: {game.manilha()}\033[m\n')
game.partidas()
