from .product_model import Product
from .ingredient_model import Ingredient
from .recipe_model import Recipe
from .recipe_ingredient_model import RecipeIngredients
from .supplier_model import Supplier
from .supplier_ingredient_model import SupplierIngredient


# Define los modelos que se exportan al importar este módulo
__all__ = ["Product","Ingredient", "Supplier","Recipe", "RecipeIngredients" "SupplierIngredient"]
