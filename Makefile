.PHONY: install run test coverage lint lint-fix clean docker help

# Variables
PYTHON := python
VENV := venv
PORT := 8000

help: ## Afficher l'aide
	@echo "Commandes disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Installer les dépendances
	@echo "Installation des dépendances..."
	pip install -r requirements.txt

run: ## Lancer l'API
	@echo "Démarrage de l'API sur http://localhost:$(PORT)"
	uvicorn app.main:app --reload --port $(PORT)

dev: run ## Alias pour run

test: ## Lancer les tests avec coverage
	@echo "Exécution des tests..."
	pytest

coverage: ## Générer un rapport de coverage détaillé
	@echo "Génération du rapport de coverage..."
	pytest --cov=app --cov-report=html --cov-report=term-missing
	@echo "Rapport HTML généré dans htmlcov/index.html"

lint: ## Vérifier le code avec Ruff
	@echo "Vérification du code avec Ruff..."
	ruff check .

lint-fix: ## Corriger automatiquement les erreurs de linting
	@echo "Correction automatique avec Ruff..."
	ruff check --fix .

format: ## Formater le code
	@echo "Formatage du code avec Ruff..."
	ruff format .

clean: ## Nettoyer les fichiers générés
	@echo "Nettoyage..."
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

docker: ## Construire l'image Docker
	@echo "Construction de l'image Docker..."
	docker build -t ticket-api .

docker-run: docker ## Construire et lancer le conteneur Docker
	@echo "Lancement du conteneur Docker..."
	docker run -p $(PORT):8000 ticket-api

docker-compose-up: ## Lancer avec Docker Compose
	docker-compose up --build

docker-compose-down: ## Arrêter Docker Compose
	docker-compose down

venv: ## Créer un environnement virtuel
	$(PYTHON) -m venv $(VENV)
	@echo "Environnement virtuel créé. Activez-le avec 'source $(VENV)/bin/activate'"

all: install lint test ## Installer, linter et tester
