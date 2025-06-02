from RecipesDB import RecipesDB

if __name__ == "__main__":
    db = RecipesDB()

    # test after adding recipes in db_filters_test.py
    db.update_tag(4, "#śniadanie")
    db.update_ingredient(6, "Majonez", "łyżki")

    what_to_update={'info': True, 'tags': True, 'ingredients': False}
    recipe_details={'title': 'Onigiri', 
        'description': 'Opis przygotowania...', 
        'ingredients': [
            {'amount': 150, 'name': 'Ryż', 'unit': 'g'},
            {'amount': 100, 'name': 'Tuńczyk', 'unit': 'g'},
            {'amount': 3, 'name': 'Majonez', 'unit': 'łyżka'}
            ],
        'tags': ['#śniadanie', '#szybkie']}

    db.update_recipe(what_to_update, 3, recipe_details)

    db.print_all()

    db.close_db()