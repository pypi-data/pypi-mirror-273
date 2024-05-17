from typing import Sequence
from .tabulate import Table

def Rank(ingredients: Sequence, by, reverse=False, **kwargs):
    """Rank a list of ingredients by a specific unit.

    Parameters
    ----------
    ingredients : Sequence
        A sequence of nutrical.Ingredient
    by : str
        The basis for comparision. It can be any of the defined
        kwargs in `nutrical.Ingredient`, such as "amount".
    reverse : bool, optional
        Whether to rank from highest to lowest, by default False
    **kwargs
        A kwarg could be provided to first rebase all the ingredients 
        according to a common unit with the `nutrical.Ingredient.to()`
        method before ranking them. This allows normalizing the bases 
        for comparision if the ingredients were not in the first place
        defined according to a common base.
    """
    s = _rank(ingredients, by=by, reverse=reverse, **kwargs)
    nutrition = [n for x in s for n in x.nutrition]
    headers = [by, *kwargs, 'amount', *nutrition]
    if all( x.amount is None for x in s ):
        headers = [x for x in headers if x != 'amount']
    Table(s, headers=headers)


def _rank(ingredients: Sequence, by='amount', reverse=False, **kwargs):
    rebase = [ x.to( **kwargs ) for x in ingredients ]

    if 'amount' == by:
        rebase = sorted(rebase, key=lambda x: x.amount, reverse=reverse) 
    else:
        rebase = sorted(rebase, key=lambda x: x.get_agg_nutri(by), reverse=reverse) 
    return rebase 
