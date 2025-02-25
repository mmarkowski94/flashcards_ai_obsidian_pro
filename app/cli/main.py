import re
import time
from typing import Iterator

import typer
from rich import print
from rich.console import Console
from rich.table import Table
from typer import Typer

from app.controllers.create_cards import create_cards
from app.controllers.get_cards_by_id import get_cards_by_id
from app.controllers.load_cards import load_cards
from app.controllers.save_cards import save_cards
from app.controllers.save_deck import save_deck

# from app.models.flashcard_models import FlashCard

app: Typer = Typer(add_completion=False)
console: Console = Console()


@app.callback(invoke_without_command=True)
def menu() -> None:
	print("Choose option:")
	print("1. Create cards from Vault")
	print("2. Get cards from DB")
	print("3. Create Deck")

	choice = typer.prompt("Provide option number", type=int)

	if choice == 1:
		cards = create_cards_cli()
		option = typer.confirm("Save to db?")
		if option:
			save_cards_cli(cards)
		menu()
	elif choice == 2:
		get_cards_cli()
	elif choice == 3:
		create_deck_cli()
	else:
		print("Thank you for using Flashcards AI")


def save_cards_cli(cards: list) -> None:
	save_cards(cards)


def flat_if(cards: list) -> Iterator:
	for card in cards:
		if not isinstance(card, dict):
			yield from flat_if(card)
		else:
			yield card


@app.command(name="create-cards")
def create_cards_cli() -> list:
	total = 100
	with typer.progressbar(range(total), label="Generating...") as progress:
		for _ in progress:
			time.sleep(0.01)

	cards = create_cards()
	table = Table("Question", "Level", title="Flashcards AI")

	with typer.progressbar(range(100), label="Transforming...") as progress:
		for _ in progress:
			time.sleep(0.01)

	for card in cards:
		table.add_row(card.front_site, card.difficulty_level.value)

	console.print(table)
	return cards


@app.command(name="get-cards")
def get_cards_cli() -> None:
	cards = load_cards()
	table = Table("Index", "Question", "Level", title="Flashcards AI")

	for card in cards:
		table.add_row(str(card.id), card.front_site, card.difficulty_level)

	console.print(table)


@app.command(name="create-deck")
def create_deck_cli() -> None:
	get_cards_cli()

	name = typer.prompt("Enter deck name: ")
	indexes = typer.prompt("Provide indexes for deck, coma separated.", type=str)
	indexes_digits = list({int(digit) for digit in re.findall(r"\d+", indexes)})

	cards = get_cards_by_id(indexes_digits)

	save_deck({
		"name": name,
		"cards_idx": [card.id for card in cards],
	})
