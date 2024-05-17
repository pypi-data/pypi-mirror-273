from tabulate import tabulate
from .utils import round2


def Table(lst, headers=None, digits=2, cat=True, rowIndex=True, noName=False, **kwargs):
    if headers is not None:
        headers = [ 'name', *headers ]
        if noName:
            headers = [ x for x in headers if x != 'name' ]
    rows = []
    for x in lst:
        row = {
            'name': x.name,
            'servings': x.servings,
            'amount': round2(x.total_amount, digits),
            **{ k: round2(x.get_agg_nutri(k),2) for k in x.nutrition }
        }
        if noName: del row['name']
        if headers is not None:
            row = { k:row.get(k, None) for k in headers }
        rows.append(row)
    
    idx = False
    if rowIndex:
        idx = [i+1 for i, _ in enumerate(rows)]
    t = tabulate(rows, headers='keys', showindex=idx, **kwargs)

    if not cat: return t
    print(t)


def indent_block(x:str, indent="  "):
    return '\n'.join( f"{indent}{line}" for line in x.split('\n') )
