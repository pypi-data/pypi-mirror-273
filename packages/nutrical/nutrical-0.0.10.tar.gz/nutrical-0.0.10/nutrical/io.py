#%%

import csv
from .nutrical import Recipe, Ingredient  # testing only
# from .nutrical import Recipe  # testing only
from .utils import UREG
from pathlib import Path

EXCEL_EXT = ('.xlsx', '.xls', '.xlsm', '.xlsb')

def import_recipe(fp):
    fp = Path(fp)
    if fp.suffix in EXCEL_EXT:
        from pandas import read_excel
        d = read_excel(fp, na_filter=False)
        x = []
        for r in d.iterrows():
            if r[1]['name'] == "<TOTAL>": continue
            x.append( parse_recipe_row(r[1]) )
        d = Recipe(fp.stem, components=x)

    elif fp.suffix == ".csv":
        with open(fp, encoding="UTF-8", newline="") as f:
            reader = csv.DictReader(f)
            x = []
            for r in reader:
                if r['name'] == "<TOTAL>": continue
                x.append( parse_recipe_row(r) )
            d = Recipe(fp.stem, components=x)
    else:
        raise Exception("Unsupported format!")

    return d


def parse_recipe_row(r):
    obj = parse_num_dict({ c:r[c] for c in r.keys() if c != "servings" })
    I = Ingredient(**obj)
    I.set_servings(float(r["servings"]))
    return(I)


def parse_num_dict(x):
    out = {}
    for k, v in x.items():
        if k == 'name':
            out[k] = v
            continue
        if v == '':
            out[k] = 0
            continue
        try: 
            v = float(v)
        except:
            v = UREG(v)
        out[k] = v
    return out