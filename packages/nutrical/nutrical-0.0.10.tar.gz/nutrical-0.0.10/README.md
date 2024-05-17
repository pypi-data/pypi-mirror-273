Nutritional value calculation for recipes and ingredients
=========================================================

`nutrical` provides an object-oriented interface for defining and manipulating the nutritional value of ingredients and recipes.

- [Live demo](https://yongfu.name/nutrical-demo/)


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

    name      servings  amount      dollar    soluble fiber
    ------  ----------  --------  --------  ---------------
    hi               1  150 gram        20                1

</div>

</div>

<div class="cell code" execution_count="3">

``` python
# nutritional value of 2 apples (summed)
2 * apple
```

<div class="output execute_result" execution_count="3">

    name      servings  amount      calories    protein    fiber    dollars
    ------  ----------  --------  ----------  ---------  -------  ---------
    apple            2  320 gram         160          1        2         20

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

    name      servings  amount      calories    protein    fiber    dollars
    ------  ----------  --------  ----------  ---------  -------  ---------
    apple            1  160 gram          80        0.5        1         10

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

    name      servings  amount        calories    protein    fiber    dollars
    ------  ----------  ----------  ----------  ---------  -------  ---------
    apple            3  480.0 gram         240        1.5        3         30

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

      servings  amount      dollars    calories    fiber    protein
    ----------  --------  ---------  ----------  -------  ---------
             1                   25         280        1        3.5

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

        servings  amount        calories    dollars    protein    fat    fiber
      ----------  ----------  ----------  ---------  ---------  -----  -------
               1  110.0 gram         235         24       9.55     30      4.3

      [INGREDIENTS]
            name      servings  amount       calories    protein    fiber    dollars    fat
        --  ------  ----------  ---------  ----------  ---------  -------  ---------  -----
         1  banana         1    80 gram            70       1         1.6          9
         2  peanut         1.5  30.0 gram         165       8.55      2.7         15     30

</div>

</div>

<div class="cell code" execution_count="8">

``` python
recipe.add(1.5*apple)  # add 1 and a half apples to ingredient
recipe
```

<div class="output execute_result" execution_count="8">

    <Recipe (Fruit Cake)>

        servings  amount        calories    dollars    protein    fat    fiber
      ----------  ----------  ----------  ---------  ---------  -----  -------
               1  350.0 gram         355         39       10.3     30      5.8

      [INGREDIENTS]
            name      servings  amount        calories    protein    fiber    dollars    fat
        --  ------  ----------  ----------  ----------  ---------  -------  ---------  -----
         1  banana         1    80 gram             70       1         1.6          9
         2  peanut         1.5  30.0 gram          165       8.55      2.7         15     30
         3  apple          1.5  240.0 gram         120       0.75      1.5         15

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

        servings  amount        calories    dollars    protein    fat    fiber
      ----------  ----------  ----------  ---------  ---------  -----  -------
               1  350.0 gram         355         39       10.3     30      5.8

      [INGREDIENTS]
            name      servings  amount        calories    protein    fiber    dollars    fat
        --  ------  ----------  ----------  ----------  ---------  -------  ---------  -----
         1  banana         1    80 gram             70       1         1.6          9
         2  peanut         1.5  30.0 gram          165       8.55      2.7         15     30
         3  apple          1.5  240.0 gram         120       0.75      1.5         15

</div>

</div>

<div class="cell code" execution_count="10">

``` python
recipe.to(amount = '100gram')  # change of basis
```

<div class="output execute_result" execution_count="10">

    <Recipe (Cake)>

        servings  amount        calories    dollars    protein    fat    fiber
      ----------  ----------  ----------  ---------  ---------  -----  -------
               1  100.0 gram      101.43      11.14       2.94   8.57     1.66

      [INGREDIENTS]
            name      servings  amount        calories    protein    fiber    dollars    fat
        --  ------  ----------  ----------  ----------  ---------  -------  ---------  -----
         1  banana    0.285714  22.86 gram       20          0.29     0.46       2.57
         2  peanut    0.428571  8.57 gram        47.14       2.44     0.77       4.29   8.57
         3  apple     0.428571  68.57 gram       34.29       0.21     0.43       4.29

</div>

</div>

<div class="cell code" execution_count="11">

``` python
recipe.to(amount = '100gram')  # change of basis
```

<div class="output execute_result" execution_count="11">

    <Recipe (Cake)>

        servings  amount        calories    dollars    protein    fat    fiber
      ----------  ----------  ----------  ---------  ---------  -----  -------
               1  100.0 gram      101.43      11.14       2.94   8.57     1.66

      [INGREDIENTS]
            name      servings  amount        calories    protein    fiber    dollars    fat
        --  ------  ----------  ----------  ----------  ---------  -------  ---------  -----
         1  banana    0.285714  22.86 gram       20          0.29     0.46       2.57
         2  peanut    0.428571  8.57 gram        47.14       2.44     0.77       4.29   8.57
         3  apple     0.428571  68.57 gram       34.29       0.21     0.43       4.29

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

        servings  amount        calories    dollars    protein    fat    fiber
      ----------  ----------  ----------  ---------  ---------  -----  -------
               1  350.0 gram         355         39       10.3     30      5.8

      [INGREDIENTS]
            name      servings  amount        calories    protein    fiber    dollars    fat
        --  ------  ----------  ----------  ----------  ---------  -------  ---------  -----
         1  banana         1    80 gram             70       1         1.6          9
         2  peanut         1.5  30.0 gram          165       8.55      2.7         15     30
         3  apple          1.5  240.0 gram         120       0.75      1.5         15

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

        servings  amount        calories    dollars    protein    fat    fiber
      ----------  ----------  ----------  ---------  ---------  -----  -------
               1  350.0 gram         355         39       10.3     30      5.8

      [INGREDIENTS]
            name      servings  amount        calories    dollars    protein    fat    fiber
        --  ------  ----------  ----------  ----------  ---------  ---------  -----  -------
         1  banana         1    80.0 gram           70          9       1         0      1.6
         2  peanut         1.5  30.0 gram          165         15       8.55     30      2.7
         3  apple          1.5  240.0 gram         120         15       0.75      0      1.5

</div>

</div>

<div class="cell code" execution_count="15">

``` python
recipe = import_recipe("FruitCake.xlsx")
recipe
```

<div class="output execute_result" execution_count="15">

    <Recipe (FruitCake)>

        servings  amount        calories    dollars    protein    fat    fiber
      ----------  ----------  ----------  ---------  ---------  -----  -------
               1  350.0 gram         355         39       10.3     30      5.8

      [INGREDIENTS]
            name      servings  amount        calories    dollars    protein    fat    fiber
        --  ------  ----------  ----------  ----------  ---------  ---------  -----  -------
         1  banana         1    80.0 gram           70          9       1         0      1.6
         2  peanut         1.5  30.0 gram          165         15       8.55     30      2.7
         3  apple          1.5  240.0 gram         120         15       0.75      0      1.5

</div>

</div>

<div class="cell markdown">

## Example 1: Home-made Yogurt

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

        servings  amount        protein
      ----------  ----------  ---------
               1  700.0 gram         42

      [INGREDIENTS]
            name                   servings  amount         protein
        --  -------------------  ----------  -----------  ---------
         1  milk powder             5.03846  161.23 gram       39.3
         2  water                   2.31885  463.77 gram
         3  probiotics (yogurt)     1        75 gram            2.7

</div>

</div>

<div class="cell code" execution_count="18">

``` python
yogurt.to(amount='100g')
```

<div class="output execute_result" execution_count="18">

    <Recipe (yogurt)>

        servings  amount        protein
      ----------  ----------  ---------
               1  100.0 gram          6

      [INGREDIENTS]
            name                   servings  amount        protein
        --  -------------------  ----------  ----------  ---------
         1  milk powder            0.71978   23.03 gram       5.61
         2  water                  0.331264  66.25 gram
         3  probiotics (yogurt)    0.142857  10.71 gram       0.39

</div>

</div>

<div class="cell markdown">

## Example 2: Cost-efficient Protein

Say, I have a limited budget on protein supplements. In order to reach
the recommened amount of protein intake, I would like to find the most
cost-efficient protein source available to me.

| Product         | Unit     | Protein (g) | Price (NTD) |
|-----------------|----------|-------------|-------------|
| Whey            | 1 bag    | 1000 \* .8  | 499         |
| Casein          | 1 bag    | 907 \* .8   | 1200        |
| Egg (7-11)      | 1 egg    | 6           | 10          |
| Egg (raw)       | 1 box    | 10 \* 6     | 59          |
| Tofu            | 1 box    | 4 \* 8.5    | 35          |
| Dry milk        | 1 can    | 7.8 \* 81   | 789         |
| Soy milk (7-11) | 1 bottle | 3.4 \* 4    | 25          |

Above are some of the candidates. Let's find out which of them has the
**lowest price per gram of protein**. The `nutrical.Rank` function can
help with this.

</div>

<div class="cell code" execution_count="19">

``` python
from nutrical import Rank
from nutrical import Ingredient as I

sources_of_protein = [
    I("Whey",            protein = 1000 * .8, price = 499),
    I("Casein",          protein =  907 * .8, price = 1200),
    I("Egg (7-11)",      protein = 6        , price = 10),
    I("Egg (raw)" ,      protein = 6        , price = 6),
    I("Tofu",            protein = 8.5 * 4  , price = 35),
    I("Dry milk",        protein = 7.8 * 81 , price = 789),
    I("Soy milk (7-11)", protein = 3.4 * 4  , price = 25),
]

Rank( sources_of_protein, by='dollars', protein=1 )
```

<div class="output stream stdout">

        name               dollars    protein
    --  ---------------  ---------  ---------
     1  Whey                  0.62          1
     2  Egg (raw)             1             1
     3  Tofu                  1.03          1
     4  Dry milk              1.25          1
     5  Casein                1.65          1
     6  Egg (7-11)            1.67          1
     7  Soy milk (7-11)       1.84          1

</div>

</div>
