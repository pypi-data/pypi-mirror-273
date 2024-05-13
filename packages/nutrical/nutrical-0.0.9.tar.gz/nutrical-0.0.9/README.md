Nutritional value calculation for recipes and ingredients
=========================================================

`nutrical` provides an object-oriented interface for defining and manipulating the nutritional value of ingredients and recipes.

<!-- pandoc test/test.ipynb --to gfm | xclip/pbcopy -->
<div class="cell markdown">

## Installation

``` sh
pip install nutrical
```

## Usage

### Ingredients

</div>

<div class="cell code" execution_count="1">

``` python
from nutrical import Ingredient, Recipe

apple = Ingredient("apple", amount='160g', calories=80, protein=.5, fiber=1, dollars=10)
banana = Ingredient("banana", amount='80g', calories=70, protein=1, fiber=1.6, dollars=9)
peanut = Ingredient("peanut", amount='20g', calories=110, protein=5.7, fat=20, fiber=1.8, dollars=10)
milk = Ingredient("milk", amount="1 cup", calories=200, protein=3, dollars=15)
```

</div>

<div class="cell code" execution_count="2">

``` python
# Programmatic construction
data = {'name': 'hi', 'amount': '150g', 'dollar': 20, 'Soluble Fiber': 1}
Ingredient(**data)
```

<div class="output execute_result" execution_count="2">

    Nutrition            Quantity
    -------------------  ----------
    Servings             1
    Total amount         150 gram
    Total dollar         20
    Total soluble fiber  1

</div>

</div>

<div class="cell code" execution_count="3">

``` python
# nutritional value of 2 apples (summed)
2 * apple
```

<div class="output execute_result" execution_count="3">

    Nutrition       Quantity
    --------------  ----------
    Servings        2
    Total amount    320 gram
    Total calories  160
    Total protein   1.0
    Total fiber     2
    Total dollars   20

</div>

</div>

<div class="cell markdown">

#### Change of basis

A new ingredient can be created from an old one by setting a new amount,
as well as any `kwargs` (except `name`) used in the definition of the
ingredient. This makes it easy to calculate the nutritional value of the
same ingredient with a different weight/volume, such as for a smaller
apple.

</div>

<div class="cell code" execution_count="4">

``` python
# A smaller apple
apple2 = apple.to(amount='130g')
apple2.set_servings(1)
apple2
```

<div class="output execute_result" execution_count="4">

    Nutrition       Quantity
    --------------  ----------
    Servings        1
    Total amount    160 gram
    Total calories  80
    Total protein   0.5
    Total fiber     1
    Total dollars   10

</div>

</div>

<div class="cell markdown">

You might also want to know the amount required to reach an intake of,
say 3 grams of fiber. Simple, just supply fiber as the parameter of the
`.to()` method.

</div>

<div class="cell code" execution_count="5">

``` python
# How much to eat to reach 3g of fibers?
apple.to(fiber=3)
```

<div class="output execute_result" execution_count="5">

    Nutrition       Quantity
    --------------  ----------
    Servings        3.0
    Total amount    480.0 gram
    Total calories  240.0
    Total protein   1.5
    Total fiber     3.0
    Total dollars   30.0

</div>

</div>

<div class="cell markdown">

Different ingredients can be added together. For instance, the code
below calculates the nutritional value of apple milk.

</div>

<div class="cell code" execution_count="6">

``` python
# Apple milk nutritional value per 1g of protein
# Note that amount is (auto-)discarded since 
# milk is measured in volume while apple in weights
apple + milk
```

<div class="output execute_result" execution_count="6">

    Nutrition         Quantity
    --------------  ----------
    Servings               1
    Total calories       280
    Total dollars         25
    Total fiber            1
    Total protein          3.5

</div>

</div>

<div class="cell markdown">

Adding together different ingredients to arrive at a new one may seem a
bit counter-intuitive. Indeed, that's why there's a `nutrical.Recipe`
class to represent recipes directly.

</div>

<div class="cell markdown">

### Recipes

</div>

<div class="cell code" execution_count="7">

``` python
# Create recipe from ingredients
recipe = Recipe("Fruit Cake", [
    1   * banana,   # 1 banana
    1.5 * peanut    # 1.5 servings of peanut butter
])
recipe
```

<div class="output execute_result" execution_count="7">

    <Recipe (Fruit Cake)>

    Ingredient      Servings  Quantity
    ------------  ----------  ----------
    banana               1    80 gram
    peanut               1.5  30.0 gram

    Nutrition       Quantity
    --------------  ----------
    Servings        1
    Total amount    110.0 gram
    Total calories  235.0
    Total fat       30.0
    Total fiber     4.3
    Total protein   9.55
    Total dollars   24.0

</div>

</div>

<div class="cell code" execution_count="8">

``` python
recipe.add(1.5*apple)  # add 1 and a half apples to ingredient
recipe
```

<div class="output execute_result" execution_count="8">

    <Recipe (Fruit Cake)>

    Ingredient      Servings  Quantity
    ------------  ----------  ----------
    banana               1    80 gram
    peanut               1.5  30.0 gram
    apple                1.5  240.0 gram

    Nutrition       Quantity
    --------------  ----------
    Servings        1
    Total amount    350.0 gram
    Total calories  355.0
    Total fat       30.0
    Total fiber     5.8
    Total protein   10.3
    Total dollars   39.0

</div>

</div>

<div class="cell markdown">

#### Some Recipe methods

</div>

<div class="cell code" execution_count="9">

``` python
recipe.rename("Cake")  # rename recipe
recipe
```

<div class="output execute_result" execution_count="9">

    <Recipe (Cake)>

    Ingredient      Servings  Quantity
    ------------  ----------  ----------
    banana               1    80 gram
    peanut               1.5  30.0 gram
    apple                1.5  240.0 gram

    Nutrition       Quantity
    --------------  ----------
    Servings        1
    Total amount    350.0 gram
    Total calories  355.0
    Total fat       30.0
    Total fiber     5.8
    Total protein   10.3
    Total dollars   39.0

</div>

</div>

<div class="cell code" execution_count="10">

``` python
recipe.to(amount = '100gram')  # change of basis
```

<div class="output execute_result" execution_count="10">

    <Recipe (Cake)>

    Ingredient      Servings  Quantity
    ------------  ----------  ----------
    banana              0.29  22.86 gram
    peanut              0.43  8.57 gram
    apple               0.43  68.57 gram

    Nutrition       Quantity
    --------------  ----------
    Servings        1
    Total amount    100.0 gram
    Total calories  101.43
    Total fat       8.57
    Total fiber     1.66
    Total protein   2.94
    Total dollars   11.14

</div>

</div>

<div class="cell code" execution_count="11">

``` python
recipe.to(amount = '100gram')  # change of basis
```

<div class="output execute_result" execution_count="11">

    <Recipe (Cake)>

    Ingredient      Servings  Quantity
    ------------  ----------  ----------
    banana              0.29  22.86 gram
    peanut              0.43  8.57 gram
    apple               0.43  68.57 gram

    Nutrition       Quantity
    --------------  ----------
    Servings        1
    Total amount    100.0 gram
    Total calories  101.43
    Total fat       8.57
    Total fiber     1.66
    Total protein   2.94
    Total dollars   11.14

</div>

</div>

<div class="cell markdown">

#### Import/Export

</div>

<div class="cell code" execution_count="12">

``` python
recipe
```

<div class="output execute_result" execution_count="12">

    <Recipe (Cake)>

    Ingredient      Servings  Quantity
    ------------  ----------  ----------
    banana               1    80 gram
    peanut               1.5  30.0 gram
    apple                1.5  240.0 gram

    Nutrition       Quantity
    --------------  ----------
    Servings        1
    Total amount    350.0 gram
    Total calories  355.0
    Total fat       30.0
    Total fiber     5.8
    Total protein   10.3
    Total dollars   39.0

</div>

</div>

<div class="cell code" execution_count="13">

``` python
# Export nutritional value
recipe.export_csv("FruitCake.csv") 
recipe.export_xlsx("FruitCake.xlsx") 
```

</div>

<div class="cell code" execution_count="14">

``` python
from nutrical import import_recipe

# Import recipe from csv/excel
recipe = import_recipe("FruitCake.csv")
recipe
```

<div class="output execute_result" execution_count="14">

    <Recipe (FruitCake)>

    Ingredient      Servings  Quantity
    ------------  ----------  ----------
    banana               1    80.0 gram
    peanut               1.5  30.0 gram
    apple                1.5  240.0 gram

    Nutrition       Quantity
    --------------  ----------
    Servings        1
    Total amount    350.0 gram
    Total calories  355.0
    Total fat       30.0
    Total fiber     5.8
    Total protein   10.3
    Total dollars   39.0

</div>

</div>

<div class="cell code" execution_count="15">

``` python
recipe = import_recipe("FruitCake.xlsx")
recipe
```

<div class="output execute_result" execution_count="15">

    <Recipe (FruitCake)>

    Ingredient      Servings  Quantity
    ------------  ----------  ----------
    banana               1    80.0 gram
    peanut               1.5  30.0 gram
    apple                1.5  240.0 gram

    Nutrition       Quantity
    --------------  ----------
    Servings        1
    Total amount    350.0 gram
    Total calories  355.0
    Total fat       30.0
    Total fiber     5.8
    Total protein   10.3
    Total dollars   39.0

</div>

</div>

<div class="cell markdown">

## Example: Home-made Yogurt

</div>

<div class="cell code" execution_count="16">

``` python
from nutrical.utils import UREG
from nutrical import Ingredient, Recipe

powder = Ingredient("milk powder", amount='32g', protein=7.8)
water = Ingredient("water", amount='200g')
probio = Ingredient("probiotics (yogurt)", amount="75g", protein=2.7)

target_protein_concentration = 6
target_total_weight = 700
protein_from_milk = target_protein_concentration * (target_total_weight/100) - 2.7
powder_to_add = powder.to(protein=protein_from_milk)
water_weight = UREG(f"{target_total_weight} gram") - probio.total_amount - powder_to_add.total_amount
```

</div>

<div class="cell code" execution_count="17">

``` python
yogurt = Recipe("yogurt", components=[
    powder_to_add,
    water.to(amount=water_weight),
    probio
])
yogurt
```

<div class="output execute_result" execution_count="17">

    <Recipe (yogurt)>

    Ingredient             Servings  Quantity
    -------------------  ----------  -----------
    milk powder                5.04  161.23 gram
    water                      2.32  463.77 gram
    probiotics (yogurt)        1     75 gram

    Nutrition      Quantity
    -------------  ----------
    Servings       1
    Total amount   700.0 gram
    Total protein  42.0

</div>

</div>

<div class="cell code" execution_count="18">

``` python
yogurt.to(amount='100g')
```

<div class="output execute_result" execution_count="18">

    <Recipe (yogurt)>

    Ingredient             Servings  Quantity
    -------------------  ----------  ----------
    milk powder                0.72  23.03 gram
    water                      0.33  66.25 gram
    probiotics (yogurt)        0.14  10.71 gram

    Nutrition      Quantity
    -------------  ----------
    Servings       1
    Total amount   100.0 gram
    Total protein  6.0

</div>

</div>
