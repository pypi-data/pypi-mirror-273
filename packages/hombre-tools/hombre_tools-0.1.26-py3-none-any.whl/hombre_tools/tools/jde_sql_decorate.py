"""
For each line with JDE table or
column object adds comment with JDE object description
Stanislav Vohnik
2019-09-06
"""
import re
from os import path
from pandas import HDFStore, DataFrame

# RAEDING JDE CATALOG
with HDFStore('/'.join(path.realpath(__file__).split('\\')[:-1]) +'/catalog/catalog_new.h5') as store:
    print(store.info())
    TABLES = store.get('tables')
    COLUMNS = store.get('columns')

CATALOG = ((TABLES, 'Table'),
           (COLUMNS, 'Field'))

OPTIONS = {'keyword_case':'upper',
           'identifier_case':'upper',
           'reindent_aligned':True,
           'indent_width':4}

P = re.compile(r'(\w*)')


#creating index to speed _find
TABLES.reset_index()
TABLES.set_index('Table', inplace=True)
COLUMNS.reset_index()
COLUMNS.set_index('Field', inplace=True)

STOP_WORD = {'', 'SELECT', 'FROM', 'AS', 'WHERE', 'GROUP', 'BY',
             'LEFT', 'JOIN', 'IS', 'NOT', 'NULL', 'INNER',
             'OUTER', 'CASE', 'WHEN', 'ELSE', 'THEN', 'END',
             'UNION', 'NOLOCK', 'IN', 'ORDER', 'CREATE', 'OR', 'AND', 'NOT',
             'REPLACE', 'VIEW', 'TO', 'GRANT'}

MEME= {}

def comment(script):
    """
    For each line with JDE table or
    column adds comment with JDE object description
    """
    global STOP_WORD, MEME

    def _find():
        """
        finds description by df index
        """
        descr = None
        try:
            desc = catalog.loc[word].Description
            result =   desc if isinstance(desc, str) else desc.values[0]
            MEME[word]=result
        except KeyError:
           MEME[word] = None
    def meme():
        if MEME.get(word):
            descr = MEME.get(word)
            if descr:
                _comment.append(f'{word}:{descr}')
                return True
            return False

    sqls = []
    for sql in script.split(';'):
        lines = []
        for line in sql.splitlines():
            _comment = []
            if '*/' in line:
                lines.append(line)
                continue
            for word in P.findall(line):
                exists = False
                word = word.upper()
                if word not in STOP_WORD:
                    if meme():
                        continue
                    else:
                        for catalog, _ in CATALOG:
                            _find()
                            if meme():
                                exists = True
                                break
                        if not exists:
                            STOP_WORD = set(list(STOP_WORD) + [word])                                  
            if _comment:
                line += f" /* {', '.join(_comment)} */"
            lines.append(line)
        sqls.append('\n'.join(lines[:]))
    return ';\n'.join(sqls)
