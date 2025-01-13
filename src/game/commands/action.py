from abc import ABC, abstractmethod

class ActionCommand(ABC):
    @abstractmethod
    def execute():
        pass

# ActionCommand placePiece(piece, position)
# ActionCommand removePieceFromShowcase()
# ActionCommand startNewRound()