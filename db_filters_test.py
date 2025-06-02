from RecipesDB import RecipesDB

if __name__ == "__main__":
    db = RecipesDB()

    print(db.is_ready())

    recipe_dict_1 = {'title': 'Krem dyniowy', 
                'description': 'Opis przygotowania...', 
                'ingredients': [
                    {'amount': 1, 'name': 'Dynia', 'unit': 'szt.'},
                        {'amount': 1000, 'name': 'Woda', 'unit': 'litr'}
                ],
                'tags': ['#zupa', '#szybkie']}
    
    recipe_dict_2 = {'title': 'Pomidorowa', 
                'description': 'Opis przygotowania...', 
                'ingredients': [
                    {'amount': 200, 'name': 'Koncentrat pomidorowy', 'unit': 'g'},
                        {'amount': 1000, 'name': 'Woda', 'unit': 'litr'}
                ],
                'tags': ['#zupa', '#domowy']}
    
    recipe_dict_3 = {'title': 'Onigiri', 
                'description': 'Opis przygotowania...', 
                'ingredients': [
                    {'amount': 150, 'name': 'Ryż', 'unit': 'g'},
                        {'amount': 100, 'name': 'Tuńczyk', 'unit': 'g'},
                        {'amount': 3, 'name': 'Majonez', 'unit': 'łyżka'}
                ],
                'tags': ['#sniadanie']}
    
    db.add_recipe(recipe_dict_1)
    db.add_recipe(recipe_dict_2)
    db.add_recipe(recipe_dict_3)

    db.print_all()

    print("Filters test 1")
    print(db.get_simple_recipes(filters={
        'tags': [],
        'ingredients': []
    }))
    print("Filters test 2")
    print(db.get_simple_recipes(filters={
        'tags': ['#zupa'],
        'ingredients': []
    }))
    print("Filters test 3")
    print(db.get_simple_recipes(filters={
        'tags': ['#zupa', '#domowy'],
        'ingredients': []
    }))
    print("Filters test 4")
    print(db.get_simple_recipes(filters={
        'tags': ['#zupa', '#domowy'],
        'ingredients': ['Dynia', 'Woda']
    }))
    print("Filters test 5")
    print(db.get_simple_recipes(filters={
        'tags': ['#zupa', '#domowy'],
        'ingredients': ['Koncentrat pomidorowy']
    }))

    db.close_db()