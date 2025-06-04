import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from RecipesDB import RecipesDB
from RecipeFileHandler import RecipeFileHandler
from Recipe import Recipe


class RecipeManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("książka")
        self.db = RecipesDB()
        self.recipe_ids = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.recipe_list = QListWidget()
        self.recipe_list.itemClicked.connect(self.display_recipe)
        layout.addWidget(QLabel("przepisy (z bazy):"))
        layout.addWidget(self.recipe_list)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("dodaj ręcznie")
        self.btn_import = QPushButton("import z pliku")
        self.btn_export = QPushButton("eksport listy")
        self.btn_save = QPushButton("zapisz przepis")
        self.btn_delete = QPushButton("usuń przepis")

        self.btn_add.clicked.connect(self.add_recipe)
        self.btn_import.clicked.connect(self.import_recipe)
        self.btn_export.clicked.connect(self.export_shopping_list)
        self.btn_save.clicked.connect(self.save_recipe_to_file)
        self.btn_delete.clicked.connect(self.delete_recipe)

        for btn in [self.btn_add, self.btn_import, self.btn_save, self.btn_export, self.btn_delete]:
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)

        self.recipe_view = QTextEdit()
        self.recipe_view.setReadOnly(True)
        layout.addWidget(QLabel("info o przepisie:"))
        layout.addWidget(self.recipe_view)

        self.setLayout(layout)
        self.load_recipes()

    def load_recipes(self):
        self.recipe_list.clear()
        self.recipe_ids.clear()
        recipes = self.db.get_simple_recipes(filters={'tags': [], 'ingredients': []})
        for recipe in recipes:
            self.recipe_ids.append(recipe["id"])
            self.recipe_list.addItem(recipe["name"])

    def display_recipe(self, item):
        index = self.recipe_list.row(item)
        recipe_id = self.recipe_ids[index]
        recipe = self.db.get_recipe_details(recipe_id)

        details = f"tytuł: {recipe['title']}\n"
        details += "składniki:\n"
        for i in recipe['ingredients']:
            details += f"{i['name']} - {i['amount']} {i['unit']}\n"
        details += "opis:\n" + recipe['description'] + "\n"
        if recipe['tags']:
            details += "tagi: " + ", ".join(recipe['tags'])
        self.recipe_view.setPlainText(details)

    def add_recipe(self):
        title, ok = QInputDialog.getText(self, "nowy przepis", "tytuł:")
        if not (ok and title):
            return

        all_ingredients = self.db.get_list_of_ingredients()
        ingredient_names = [i['name'] for i in all_ingredients]

        ingredients = []
        while True:
            item, ok = QInputDialog.getItem(self, "składnik", "Wybierz składnik:", ingredient_names, editable=False)
            if not ok or not item:
                break

            amount, ok = QInputDialog.getDouble(self, "ilość", f"Ile potrzebujesz składnika '{item}'?", 1.0, 0.0)
            if not ok:
                continue

            unit, ok = QInputDialog.getText(self, "jednostka", f"Podaj jednostkę dla '{item}':")
            if not (ok and unit):
                continue

            ingredients.append({'name': item, 'amount': amount, 'unit': unit})

            more, ok = QInputDialog.getItem(self, "dodaj więcej?", "Dodać kolejny składnik?", ["Tak", "Nie"], editable=False)
            if not ok or more == "Nie":
                break

        if not ingredients:
            QMessageBox.warning(self, "Brak składników", "Przepis nie został dodany — brak składników.")
            return

        desc, _ = QInputDialog.getMultiLineText(self, "opis", "Podaj opis przygotowania:")
        tags_text, _ = QInputDialog.getText(self, "tagi", "Podaj tagi (oddzielone spacją):")
        tags = tags_text.strip().split() if tags_text else []

        recipe_dict = {
            'title': title,
            'description': desc,
            'ingredients': ingredients,
            'tags': tags
        }

        self.db.add_recipe(recipe_dict)
        QMessageBox.information(self, "Sukces", "Przepis dodany do bazy danych.")
        self.load_recipes()

    def import_recipe(self):
        path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik z przepisem", filter="*.txt")
        if not path:
            return
        try:
            recipe = RecipeFileHandler.load_from_file(path)
            recipe_dict = {
                "title": recipe.title,
                "description": recipe.description,
                "tags": recipe.tags,
                "ingredients": recipe.ingredients
            }
            self.db.add_recipe(recipe_dict)
            QMessageBox.information(self, "Dodano", "Przepis zaimportowany do bazy.")
            self.load_recipes()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", str(e))

    def save_recipe_to_file(self):
        current_item = self.recipe_list.currentItem()
        if not current_item:
            return
        index = self.recipe_list.row(current_item)
        recipe_id = self.recipe_ids[index]
        recipe_data = self.db.get_recipe_details(recipe_id)

        recipe_obj = Recipe(
            title=recipe_data["title"],
            description=recipe_data["description"],
            tags=recipe_data["tags"],
            ingredients=recipe_data["ingredients"]
        )

        path, _ = QFileDialog.getSaveFileName(self, "Zapisz przepis", filter="*.txt")
        if not path:
            return
        RecipeFileHandler.save_to_file(recipe_obj, path)
        QMessageBox.information(self, "Zapisano", "Przepis zapisany do pliku.")

    def export_shopping_list(self):
        current_item = self.recipe_list.currentItem()
        if not current_item:
            return
        index = self.recipe_list.row(current_item)
        recipe_id = self.recipe_ids[index]
        recipe = self.db.get_recipe_details(recipe_id)

        path, _ = QFileDialog.getSaveFileName(self, "Zapisz listę zakupów", filter="*.txt")
        if not path:
            return

        with open(path, "w", encoding="utf-8") as f:
            f.write(f"Lista zakupów do przepisu: {recipe['title']}\n")
            for ing in recipe["ingredients"]:
                f.write(f"- {ing['amount']} {ing['unit']} {ing['name']}\n")

        QMessageBox.information(self, "Zapisano", "Lista zakupów została zapisana.")

    def delete_recipe(self):
        current_item = self.recipe_list.currentItem()
        if not current_item:
            return
        index = self.recipe_list.row(current_item)
        recipe_id = self.recipe_ids[index]

        confirm = QMessageBox.question(self, "Usuń przepis",
                                       "Czy na pewno chcesz usunąć ten przepis?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.db.delete_recipe(recipe_id)
            QMessageBox.information(self, "Usunięto", "Przepis został usunięty.")
            self.load_recipes()

    def closeEvent(self, event):
        self.db.close_db()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RecipeManager()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
