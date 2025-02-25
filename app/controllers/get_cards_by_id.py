from app.db.db import DBTiny
from app.models.flashcard_models import FlashCard
from app.settings.settings import dirname_app


def get_cards_by_id(indexes: list[int]) -> list[FlashCard]:
	with DBTiny(dirname_app / '.store', 'flashcards') as db:
		cards = db.get(indexes)

	return [FlashCard(**card) for card in cards]
