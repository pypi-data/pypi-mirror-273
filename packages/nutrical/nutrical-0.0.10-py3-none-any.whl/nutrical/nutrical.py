'''API examples

>>> apple = Ingredient(protein=0.5, fat=9, calories=100, amount='100g', dollar=1.5)
>>> apple.to(amount='170g')  # Equivalent: 1.7 * apple
>>> apple.to(dollar=3)        # Equivalent: 3   * apple
>>> apple.to(protein=2)       # Equivalent: 4   * apple
'''

import csv
from pathlib import Path
from numbers import Number
from .utils import parse_amount, add_amount, round2
from .tabulate import *

RDIGIT = 2

class Recipe:

    def __init__(self, name=None, components=None):
        self.name = name
        self.components = components
        self.total = sum(self.components)
    

    def __repr__(self):
        # ingredients = tabulate(self.ingredients, headers=["Ingredient", "Servings", "Quantity"])
        h = f"<Recipe ({self.name})>" if self.name is not None else "<Recipe>"

        headers = ['servings', 'amount', *self.total.nutrition]
        if self.total.total_amount is None:
            headers = [x for x in headers if x != 'amount']
        total = Table( [self.total], headers=headers, cat=False, rowIndex=False, noName=True)
        total = indent_block(total)

        ingredients = "[INGREDIENTS]\n" + indent_block(Table(self.components, cat=False))
        ingredients = indent_block(ingredients)
        
        return f"{h}\n\n{total}\n\n{ingredients}\n"


    @property
    def ingredients(self):
        """Internal display use
        """
        return [ (x.name, round2(x.servings,RDIGIT), round2(x.total_amount,RDIGIT)) for x in self.components ]
    

    def to(self, **kwargs):
        '''Only the first kwarg is taken
        '''
        k, v = kwargs.popitem()
        k = k.lower()
        if k == 'amount' and self.total.amount is not None:
            fct = float(parse_amount(v) / self.total.amount)
        elif k in self.total.nutrition:
            fct = v / self.total.nutrition[k]
        else:
            raise Exception("Conversion unit not found!")

        return fct * self


    def __add__(self, recipe):
        return Recipe(name=self.name, components=[*self.components, *recipe.components])


    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)
    

    def __mul__(self, fct: Number):
        if not isinstance(fct, Number): 
            raise Exception("Multiplication on numbers only!")
        return Recipe(name=self.name, components=[fct * c for c in self.components])


    __rmul__ = __mul__


    def add(self, ingredient):
        self.components.append(ingredient)
        self.total = sum(self.components)


    def rename(self, name):
        self.name = name

    
    def export_csv(self, outfp):
        cols = [ "name", "servings", "amount", *self.total.nutrition ]
        
        rows = []
        for item in [ *self.components, self.total ]:
            item = { **item.__dict__, **item.__dict__['nutrition'] }
            row = []
            for k in cols:
                row.append( item.get(k, None) )
            rows.append(row)
        rows[-1][0] = "<TOTAL>"

        with open(outfp, "w", encoding="UTF-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(cols)
            writer.writerows(rows)


    def export_xlsx(self, outfp):
        import pandas as pd
        
        tmp = Path("nutrical.tmp.export")
        self.export_csv(tmp)
        pd.read_csv(tmp).to_excel(outfp, index=False)
        tmp.unlink()


class Ingredient:
    servings = 1
    
    def __init__(self, name=None, amount=None, **kwargs):
        self.name = name
        self.amount = parse_amount(amount)
        self.nutrition = {}
        
        for k, v in kwargs.items():
            self.nutrition[k.lower()] = v

    @property
    def total_amount(self):
        try:
            return self.servings * self.amount
        except:
            return None


    def get_agg_nutri(self, nutrient):
        return self.servings * self.nutrition.get(nutrient, 0)
    

    def to(self, **kwargs):
        '''Only the first kwarg is taken
        '''
        k, v = kwargs.popitem()
        k = k.lower()
        if k == 'amount' and self.amount is not None:
            fct = float(parse_amount(v) / self.amount)
        elif k in self.nutrition:
            fct = v / self.nutrition[k]
        else:
            raise Exception("Conversion unit not found!")

        return fct * self


    def __repr__(self):
        return Table([self], headers=None, digits=2, cat=False, rowIndex=False, noName=(self.name is None))

    ########################################################################################
    #### To Do: think clearly about how amount/unit gets added when defining servings #####
    ########################################################################################

    def __add__(self, item):
        """When addition is performed, servings is set to one and all other
            properties are summed together using aggregated quantity 
            (i.e., orignal servings * property quantity)
        """
        args = {}
        amount = add_amount(self.total_amount, item.total_amount)
        for k in set( [*self.nutrition.keys(), *item.nutrition.keys()] ):
            args[k] = self.get_agg_nutri(k) + item.get_agg_nutri(k)
        return Ingredient(amount=amount, **args)


    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)
    

    def __mul__(self, fct: Number):
        """Multiplication preserves the property quantity and only modifies servings.
        """
        if not isinstance(fct, Number): 
            raise Exception("Multiplication on numbers only!")
        new = Ingredient(name=self.name, amount=self.amount, **self.nutrition)
        new.set_servings(fct*self.servings)
        return new


    __rmul__ = __mul__


    def rename(self, name):
        self.name = name


    def set_servings(self, x):
        self.servings = x

