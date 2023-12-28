# BLACKJACK CARD GAME VS COMPUTER

from random import shuffle


class Card:
    suits = ["Spades", "Clubs", "Diamonds", "Hearts"]

    values = [
        "Ace",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "Jack",
        "Queen",
        "King",
    ]

    def __init__(self, v, s):
        self.value = v
        self.suit = s

    def __repr__(self):
        return f"{self.values[self.value]} of {self.suits[self.suit]}"

    # return the numerical value of a card for scoring purposes
    def get_value(self, tally):
        if self.value > 9:
            return 10
        if self.value == 0:
            return 11 if tally + 11 <= 21 else 1
        return int(self.values[self.value])


class Deck:
    def __init__(self):
        self.cards = []
        for i in range(4):
            for j in range(13):
                self.cards.append(Card(j, i))
        shuffle(self.cards)

    # pop a card from the top of the deck and return it
    def rm_card(self):
        if len(self.cards) == 0:
            return
        return self.cards.pop()


class Player:
    def __init__(self):
        self.hand = []
        self.tally = 0
        self.wins = 0
        self.busts = 0


class Game:
    def __init__(self):
        self.player = Player()
        self.deck = Deck()
        self.ai_wins = 0
        self.ai_busts = 0

    def play_game(self):
        print(
            "\nWelcome to Blackjack.\nTry to get as close to 21 as possible without going over.\n"
        )

        cards_remaining = len(self.deck.cards)

        # keep playing until less than 5 cards
        while cards_remaining > 4:
            self.play_a_round()
            cards_remaining = len(self.deck.cards)
            print("\n")
            input("Press enter to continue.\n")

        # split remaining cards between player and computer
        if cards_remaining and cards_remaining % 2 == 0:
            for i in range(int(cards_remaining / 2)):
                self.player.hand[i] = self.deck.cards[i]
                if self.update_tally() == True:
                    self.check_win()
            self.complete_round()

        self.print_score()

        # determine and print winner
        if self.player.wins > self.ai_wins:
            print(f"\nYou win!")
        elif self.player.wins < self.ai_wins:
            print("\nComputer wins!")
        else:
            if self.player.busts < self.ai_busts:
                print(f"\nYou win!")
            elif self.player.busts > self.ai_busts:
                print("\nComputer wins!")
            else:
                print("\nIt's a tie!")

        print("\nThanks for playing.")

    def play_a_round(self):
        # reset player's hand and tally at start of each round
        self.player.hand = []
        self.player.tally = 0

        print("Dealing cards... ")
        for i in range(2):
            self.draw_card()
        self.sort_hand()

        # tally player's card values and check if they won or busted
        for card in self.player.hand:
            if self.update_tally(card) == True:
                self.check_win()
                return

        print(f"Your current tally is {self.player.tally}\n")

        # repeatedly ask player to hit or sit, either until no cards remain, or they choose to sit
        while len(self.deck.cards) > 0:
            print("Type h to hit, or press enter to sit.")
            ans = input("What would you like to do? ")
            print("\n")
            if ans == "h":
                print("Dealt... ")
                hit = self.draw_card()

                # only re-sort hand if an Ace was drawn
                if hit.value == "Ace":
                    self.sort_hand()

                # update player tally and check for win or bust
                if self.update_tally(hit) == True:
                    self.check_win()
                    return

                print(f"Your current tally is {self.player.tally}")
            else:
                break

        # once out of cards or player sits, complete the round
        self.complete_round()

    # take a card from the deck and add it to the player's hand
    def draw_card(self):
        new_card = self.deck.rm_card()
        print(new_card)
        self.player.hand.append(new_card)
        return new_card

    # sort the cards in the player's hand, ensuring Aces are counted last
    def sort_hand(self):
        for card in self.player.hand:
            if card.value == "Ace":
                index = self.player.hand.index(card)
                last = len(self.player.hand) - 1
                if not index == last:
                    tmp = self.player.hand[last]
                    self.player.hand[last] = self.player.hand[index]
                    self.player.hand[index] = tmp

    # update the player's tally, returning True if reached 21 or higher, meaning round is over
    def update_tally(self, card):
        self.player.tally += card.get_value(self.player.tally)
        if self.player.tally >= 21:
            return True
        return False

    # determine if player wins or busts and update scores
    def check_win(self):
        if self.player.tally == 21:
            print("21! You win!\n")
            self.player.wins += 1
            self.print_score()
        else:
            print(f"Bust! You got {self.player.tally}!\n")
            self.player.busts += 1
            self.ai_wins += 1
            self.print_score()

    # the player chose to sit - deal cards to the computer and check who won this round
    def complete_round(self):
        print("Tallying scores... ")

        ai_tally = 0
        ai_cards = 0

        if len(self.deck.cards) < 3:
            # deal remaining cards to computer
            for i in range(len(self.deck.cards) - 1):
                ai_tally += self.deck.cards.pop().get_value(ai_tally)
                ai_cards += 1
        else:
            # AI will always hit if tally < 16
            while ai_tally < 16:
                ai_tally += self.deck.cards.pop().get_value(ai_tally)
                ai_cards += 1

        print(f"AI got {ai_tally} in {ai_cards} cards.")
        if (ai_tally) > 21:
            print("Computer busts! Player wins!")
            self.ai_busts += 1
            self.player.wins += 1
            self.print_score()
            return

        print(f"Player got {self.player.tally} in {len(self.player.hand)} cards.\n")

        # determine winner by who's closer to 21
        ai_score = 21 - ai_tally
        player_score = 21 - self.player.tally
        if player_score < ai_score:
            print("Player wins off tally!\n")
            self.player.wins += 1
        elif ai_score < player_score:
            print("Computer wins off tally!\n")
            self.ai_wins += 1
        else:
            # if tally is tied, go by card count
            if len(self.player.hand) < 3:
                print("It's a tie!")
            else:
                print("Computer wins off card count!\n")
                self.ai_wins += 1

        self.print_score()

    # print the player's and the computers score to the screen, as well as how many cards remain
    def print_score(self):
        print("Player: ")
        print(f"{self.player.wins} wins, {self.player.busts} busts!\n")
        print("Computer: ")
        print(f"{self.ai_wins} wins, {self.ai_busts} busts!\n")
        print(f"Cards remaining: {len(self.deck.cards)}")


game = Game()
game.play_game()
