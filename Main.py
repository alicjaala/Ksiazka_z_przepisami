from Recipe import *
from RecipeFileHandler import *
from ShoppingListGenerator import *
import pprint

if __name__ == '__main__':

    try:
        recipe = RecipeFileHandler.load_from_file('przepis.txt')
        print(recipe)
        RecipeFileHandler.save_to_file(recipe, 'eksport.txt')
    except RecipeParseError as e:
        print(f"Błąd parsowania: {e}")


    recipe_dict = {'description': 'Roztop masło i czekoladę w kąpieli wodnej.\n'
                'W osobnej misce wymieszaj mąkę, cukier i jajka.\n'
                'Połącz wszystko razem i piecz w 180°C przez 40 minut.',
              'ingredients': [{'amount': 200.0, 'name': 'Mąka', 'unit': 'g'},
                 {'amount': 150.0, 'name': 'Cukier', 'unit': 'g'},
                 {'amount': 3.0, 'name': 'Jajka', 'unit': 'sztuka'},
                 {'amount': 100.0, 'name': 'Masło', 'unit': 'g'},
                 {'amount': 200.0, 'name': 'Czekolada', 'unit': 'g'}],
              'tags': ['#przepis', '#naslodko', '#zajebisteciasto'],
              'title': 'Ciasto czekoladowe'}

    recipe2_dict = {'description': 'nieistotne',
              'ingredients': [{'amount': 200.0, 'name': 'Mąka', 'unit': 'g'},
                              {'amount': 150.0, 'name': 'Cukier trzcinowy', 'unit': 'g'},
                              {'amount': 3.0, 'name': 'Jajka', 'unit': 'sztuka'},
                              {'amount': 1.0, 'name': 'Masło', 'unit': 'kostka'},
                              {'amount': 200.0, 'name': 'Czekolada', 'unit': 'g'}],
              'title': 'inne ciasto'}

    recipe_obj = Recipe.from_dict(recipe_dict)
    recipe2_obj = Recipe.from_dict(recipe2_dict)

    recipes = []
    recipes.append(recipe_obj)
    recipes.append(recipe2_obj)

    ShoppingListGenerator.generate_txt(recipes, 'lista_zakupow.txt')



