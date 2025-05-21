from collections import defaultdict

from typing import List

from Recipe import *


class ShoppingListGenerator:
    @staticmethod
    def generate_txt(recipes: List['Recipe'], file_path: str):
        combined_ingredients = defaultdict(float)

        for recipe in recipes:
            for ing in recipe.ingredients:
                key = (ing['name'].lower(), ing['unit'].lower())
                try:
                    amount = float(ing['amount'])
                except (ValueError, TypeError):
                    amount = 0
                combined_ingredients[key] += amount

        lines = ["Lista zakupów:\n"]
        for (name, unit), amount in sorted(combined_ingredients.items()):
            if amount.is_integer():
                amount = int(amount)
            lines.append(f"{name} - {amount} {unit}")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
