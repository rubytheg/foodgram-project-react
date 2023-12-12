from django.db import models
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

class Recipe(models.Model):
    # Модель рецепта
    author = models.ForeignKey(CustomUser, verbose_name=_("Автор рецепта"), foreign_name="user_recipes")
    tags = models.ManyToManyField(Tag, verbose_name=_("Тэги"), help_text=_("Проставьте тэги"))

    name = models.CharField(
        max_length=250,
        verbose_name=_("Название рецепта"),
        help_text=_("Введите название рецепта"))

    cooking_time = models.PositiveIntegerField(
        verbose_name=_("Время приготовления в минутах"),
        validators=[
            MinValueValidator(1,
                              _("Время приготовления должно быть больше минуты")),
            MaxValueValidator(4320,
                              _("Время приготовления должно быть меньше 3-х суток"))],
        help_text=_("Введите время приготовления в минутах"))

    upload_date = models.DateTimeField(
        verbose_name=_("Дата публикации"),
        auto_now_add=True,
        db_index=True,
        editable=False)

    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(verbose_name=_("Ссылка на изображение"),
                                  upload_to='recipes/',
                                  help_text=_("Загрузите картинку"),
                                  blank=True, null=True)

    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        through_fields=("recipe", "ingredient"),
        help_text=_("Выберите ингредиенты"),
        verbose_name=_("Список ингредиентов"))

    text = models.CharField(max_length=5000,
                            verbose_name=_("Описание рецепта"),
                            help_text=_("Добавьте описание"))


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Рецепт")
        verbose_name_plural =  _("Рецепты")
        ordering = ('-upload_date',)
        default_related_name = 'recipes'


class Tag(models.Model):
    # Модель тэга
    name = models.CharField(max_length=50, verbose_name=_("Тэг"), unique=True)
    color = models.ColorField(default="F5F5FF", verbose_name=_("Цвет тэга"))
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Тэг")
        verbose_name_plural = _("Тэги")

class Ingredient(models.Model):
    # Модель ингредиента
    name = models.CharField(max_length=150, verbose_name=_("Название ингредиента"))
    measurement_unit = models.CharField(max_length=50, verbose_name=_("Единицы измерения"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Ингредиент")
        verbose_name = _("Ингредиенты")
        constraints = [
            models.UniqueConstraint(fields=["name", "measurement_unit"])
        ]


class Favorite(models.Model):
    # модель избранного
    user = models.ForeignKey(
        CustomUser,
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
        related_name='user_favorites')

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name=_("Рецепт"))

    def __str__(self):
        return f'{self.user} >> {self.recipe}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','recipe'])
        ]

class RecipeIngredient(models.Model):
    # through-Модель Рецепт-Ингредиент
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_("Рецепт"),
        on_delete=models.CASCADE,
        related_name='recipe_ingredients')

    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name=_("Ингредиент"),
        on_delete=models.CASCADE,
        related_name='ingredient_recipes')

    amount = models.PositiveIntegerField(verbose_name = _("Количество"))

    def __str__(self):
        return f'{self.recipe} >> {self.ingredient} >> {self.amount}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'])
        ]

class ShoppingCart(models.Model):
    # Модель списка покупок
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"))

    recipes = models.ManyToManyField(
        Recipe,
        verbose_name=_("Список рецептов"),
        on_delete=models.CASCADE)

    def __str__(self):
        return self.user
