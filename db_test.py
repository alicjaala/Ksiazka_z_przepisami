from RecipesDB import RecipesDB

if __name__ == "__main__":
    db = RecipesDB()

    db.test_structure()

    print(db.is_ready())

    db.print_all()

    # test after adding recipes in db_filters_test.py
    print("Trying to delete:")
    print("Ryż -", db.delete_ingredient(4))
    print("#domowy -", db.delete_tag(3))
    print("Krem dyniowy -", db.delete_recipe(1))

    db.print_all()

    print("Trying to delete:")
    print("Dynia -", db.delete_ingredient(1))

    db.print_all()

    print(db.get_list_of_ingredients())
    print(db.get_list_of_tags())
    print(db.get_recipe_details(3))

    db.close_db()
