from django.db import models
from users.models import CustomUser


class Recipe(models.Model):
    # Модель рецепта
    author = models.ForeignKey(CustomUser, verbose_name="Автор рецепта", foreign_name="user_recipes")
    tags = models.ManyToManyField(Tag, verbose_name="Тэги")
    name = models.CharField(max_length=250, verbose_name="Название рецепта")
    cooking_time = models.PositiveIntegerField(verbose_name="Время приготовления в минутах")
    upload_date = models.DateTimeField(verbose_name="Дата публикации")

    thumbnail = models.ImageField(verbose_name="Ссылка на изображение",
                                  upload_to='recipes/',
                                  blank=True, null=True)

    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        through_fields=("recipe", "ingredient"),
        verbose_name="Список ингредиентов")
    text = models.CharField(max_length=5000, verbose_name="Описание рецепта")


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Рецепт"


class Tag(models.Model):
    # Модель тэга
    name = models.CharField(max_length=50, verbose_name="Тэг", unique=True)
    color = models.ColorField(default="F5F5FF", verbose_name="Цвет тэга")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тэг"

class Ingredient(models.Model):
    # Модель ингредиента
    name = models.CharField(max_length=150, verbose_name="Название ингредиента")
    measurement_unit = models.CharField(max_length=50, verbose_name="Единицы измерения")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ингредиент"
        constraints = [
            models.UniqueConstraint(fields=["name"])
        ]


class Favorite(models.Model):
    # модель избранного
    user = models.ForeignKey(CustomUser, verbose_name="Пользователь", related_name='user_favorites')
    recipe = models.ForeignKey(Recipe, verbose_name="Рецепт")

    def __str__(self):
        return f'{self.user} >> {self.recipe}'

class RecipeIngredient(models.Model):
    # through-Модель Рецепт-Ингредиент
    recipe = models.ForeignKey(Recipe, verbose_name="Рецепт", related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, verbose_name="Ингредиент", related_name='ingredient_recipes')
    amount = models.PositiveIntegerField(verbose_name = "Количество")

    def __str__(self):
        return f'{self.recipe} >> {self.ingredient} >> {self.amount}'

class ShoppingCart(models.Model):
    # Модель списка покупок
    user = models.ForeignKey(CustomUser, verbose_name="Пользователь")
    recipes = models.ManyToManyField(Recipe, verbose_name="Список рецептов")

    def __str__(self):
        return self.user
