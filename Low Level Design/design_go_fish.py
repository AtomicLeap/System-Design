# Design Go Fish

"""
Implement a simplified, fully deterministic version of the Go Fish card game,
simulating a multiplayer card game where players aim to collect sets of four
cards of the same rank (books) to win. Watch a video demonstration of the game.

Determinism (no randomness):
-> The deck is created in a fixed order with no shuffling.
    - SUITS order: ['hearts', 'diamonds', 'clubs', 'spades']
    - RANKS order: ['A', '2', ..., '10', 'J', 'Q', 'K']
    - The deck therefore starts as: A of hearts, 2 of hearts, ..., K of hearts, 
        A of diamonds, ..., K of spades.
->  Dealing and drawing always take from the top of the deck (front of the list).
->  On each turn, the current player always targets the next player in seatig order
     (index + 1 modulo number of players).
->  The rank requested is always the first (lowest) rank in the current player's hand
     when the ranks are sorted by the RANKS order above.

Gameplay:
->  Game(player_names: list<string>) -> void
    - 2 - 6 players are required. Throws if outside range.
    - Each player receives an initial hand:
        - 7 cards if there are 2 - 3 players
        - 5 cards if there are 4 - 6 players

->  `play_turn()` (internal to the game loop)
    - Let `current` to be player whose turn it is, `opponent` to be next player
        (deterministically chosen).
    - Let `rank` be the first rank in `sorted(current.hand ranks)`.
    - If `opponent` has any cards of `rank`, all such cards are transferred to 
        `current`, books are checked, and `current` takes another turn 
        (does not advance to the next player).
    - Otherwise, `current` draws the top card from the deck (if any), adds it, 
        checks books, and:
      - If the drawn card’s rank equals the requested rank, `current` keeps the turn.
      - Else, advance to the next player.
    - A "book" is completed when a player collects all 4 cards of a rank; those 4 cards 
        are removed from the hand and the player’s book count increments by 1.

->  `is_over() -> boolean`
    - The game ends when the deck is empty AND all players have no cards left in hand.

- `get_winner() -> Player`
    - Returns the player with the most books (ties are resolved by standard max behavior 
    i.e., the first with the maximum).

- `start() -> string`
    - Runs turns until `is_over()` is true, then returns the winner's name (also prints it).
"""

# Solution

from collections import deque, defaultdict

class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank # 'Ace', '2' - '10', 'Jack', 'King', 'Queen'
        self.suit = suit # 'hearts', 'diamonds', 'clubs', 'spades'
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    RANKS = ['Ace'] + [str(i) for i in range(2, 11)] + ['Jack', 'King', 'Queen'] # 13 ranks
    SUITS = ['hearts', 'diamonds', 'clubs', 'spades'] # 4 suits

    def __init__(self):
        ## Assume Deterministic shuffling not random shuffling  --> # 52 cards
        self.cards = deque([Card(rank, suit) for suit in self.SUITS for rank in self.RANKS])

    def deal(self, num_of_cards: int) -> list[Card]:
        if num_of_cards > len(self.cards):
            raise ValueError("Not enough cards in deck")
        hand, self.card = self.cards[:num_of_cards], self.cards[num_of_cards:]
        return hand

    def draw(self) -> Card:
        if not self.cards:
            raise ValueError('Deck is empty')
        return self.cards.popleft()

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand = deque() # deque[Card]
        self.books = 0 # Number of books completed

    def add_cards(self, cards: list[Card]):
        self.hand.extend(cards)
        self._check_for_books()

    def remove_cards(self, rank: str) -> list[Card]:
        match_cards = list(filter(lambda card: card.rank == rank, self.hand))
        self.hand = deque(filter(lambda card: card.rank != rank, self.hand))
        return match_cards

    def has_rank(self, rank: str) -> bool:
        return any(card.rank == rank for card in self.hand)

    def get_ranks_in_hand(self) -> set[str]:
        return { card.rank for card in self.hand }

    def _check_for_books(self):
        rank_count = defaultdict(int)
        for card in self.hand:
            rank_count[card.rank] += 1
        for rank, count in rank_count.items():
            if count == 4:
                self.hand = deque([card for card in self.hand if card.rank != rank])
                self.books += 1

class Game:
    def __init__(self, player_names: list[str]):
        if not 2 <= len(player_names) <= 6:
            raise ValueError('2 - 6 players required')
        self.deck = Deck()
        self.players = [Player(name) for name in player_names]
        self.current_player_idx = 0
        self._deal_initial_hands()

    def _deal_initial_hands(self):
        cards_per_player = 7 if len(self.players) <= 3 else 5
        for player in self.players:
            player.add_cards(self.deck.deal(cards_per_player))

    def play_turn(self):
        current_player = self.players[self.current_player_idx]
        opponent_idx = (self.current_player_idx + 1) % len(self.players)
        opponent_player = self.players[opponent_idx]

        ranks = sorted(current_player.get_ranks_in_hand())
        if not ranks:
            self.current_player_idx = \
                (self.current_player_idx + 1) % len(self.players)
            return
        
        rank = ranks[0]

        if opponent_player.has_rank(rank):
            cards = opponent_player.remove_cards(rank)
            current_player.add_cards(cards)
            return
        else:
            try:
                drawn = self.deck.draw()
                current_player.add_cards([drawn])
                if drawn.rank == rank:
                    return
            except ValueError:
                pass

        self.current_player_idx = \
                (self.current_player_idx + 1) % len(self.players)

    def is_over(self) -> bool:
        return not self.deck.cards and \
            all(len(player.get_ranks_in_hand()) == 0 for player in self.players)
    
    def get_winner(self) -> Player:
        return max(self.players, key=lambda player: player.books)
    
    def start(self):
        while not self.is_over():
            self.play_turn()
        
        winner = self.get_winner()
        return winner.name

# Game is instantiated as follows:
# game = Game(['Player_name 1', 'Player_name 2', 'Player_name 3'])
# game.start()

