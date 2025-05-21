from pprint import pformat

class Recipe:
    def __init__(self, title, ingredients, description, tags=None):
        self.title = title
        self.ingredients = ingredients  # lista słowników: {'name', 'amount', 'unit'}
        self.description = description
        self.tags = tags or []

    def __repr__(self):
        return f"<Recipe: {self.title}>"

    def __str__(self):
        return pformat(self.to_dict())

    def to_dict(self):
        return {
            'title': self.title,
            'ingredients': self.ingredients,
            'description': self.description,
            'tags': self.tags
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data['title'],
            ingredients=data['ingredients'],
            description=data['description'],
            tags=data.get('tags', [])
        )
