from django.db import models

RARITY = (('最上級', '最上級'), ('上級', '上級'), ('中級', '中級'))

class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    thumbnail = models.ImageField()
    rarity = models.CharField(
        max_length=100,
        choices=RARITY
    )

    def __str__(self):
        return self.name

class Composite(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='composite_items',
    )
    material = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='composite_materials',
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.item.name

class Comp_List(models.Model):
    comp_item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='composite_composites',
    )
    comp_quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.comp_item.name} x{self.comp_quantity}"

class Previous_List(models.Model):
    previous_item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='composite_previous',
    )
    previous_quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.previous_item.name} x{self.previous_quantity}"