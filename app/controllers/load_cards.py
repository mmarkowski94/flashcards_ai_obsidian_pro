from app.db.db import DBTiny
from app.models.flashcard_models import FlashCard
from app.settings.settings import dirname_app


def load_cards() -> list[FlashCard]:
	with DBTiny(dirname_app / '.store', 'flashcards') as db:
		cards = db.read_all()

	return [FlashCard(**card) for card in cards]