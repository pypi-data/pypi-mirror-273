import regex
from   typing import Iterator

__all__ = 'finditer', 'findany', 'iterall'

REPL  = '`'                                  # character to represent substitution and deletion points
TOKEN = regex.compile(r'\{(!{0,1}\d+|\?)\}') # for splitting on token guts
FLAGS = regex.V1, regex.V1|regex.I           # case-sensitive, case-insensitive

FORMAT = {# https://github.com/mrabarnett/mrab-regex?tab=readme-ov-file#approximate-fuzzy-matching-hg-issue-12-hg-issue-41-hg-issue-109
    '.':r'{{{over}i+1d+1s<={limit}:\S}}',    # suggestive range
    '!':r'{{{limit}<=s<={limit}:\S}}'   ,    # strict range
    '?':r'(\w+\W+)*?'                   ,}   # 0 or more unknown words 
    

# convert query to expression
def __expr(query:str, group:bool=True) -> str:

    # convert term segment to expression
    def subexpr(segment:str) -> str:
        # assume this is a token and get alleged integer range
        limit = int(''.join(filter(str.isdigit, segment)) or 0)
        
        # alias some facts
        d, t  = segment.isdigit(), segment[0]
        
        # if digit or strict get replacement characters group
        expr  = ('', fr'({REPL * limit})')[d | (t == '!')] 
        
        # append respective value and format compatible results with limits
        expr += FORMAT.get((t, '.')[d], regex.escape(segment)).format(over=limit+1, limit=limit)
        
        return expr
    
    # map[list] of term segments
    segmap = map(TOKEN.split, query.split(' '))
    
    # generator of terms from processed term segments
    terms = (r''.join(map(subexpr, filter(None, segments))) for segments in segmap)
    expr  = r'\s*'.join(terms)
    grp   = (0,1)[group is True]
    
    # create final expression
    return f'{"("*grp}{expr}{")"*grp}'
   
""" execute expression on text
    `expr` : final regex pattern
    `text` : the text to be searched
    `skip` : Iterable of words and/or characters that trigger a skip when found in a result - DEFAULT: []
    `ci`   : case insensitive matching                                                      - DEFAULT: False
"""      
def __exec(expr:str, text:str, skip:None|list|tuple|set=None, ci:bool=False) -> Iterator:
    skip = skip or []
    
    for match in regex.finditer(expr, text, flags=FLAGS[ci]):
        result = match['result']
        
        # determine if result should be skipped
        for item in skip:
            if item in result: break
        else:
            yield match.span(), result

""" format query into an expression and yield matches
    `text`           : the text to be searched
    `query`          : the term to search for
    `*args|**kwargs` : passed to `__exec` as remaining args
    
    \m\M: https://github.com/mrabarnett/mrab-regex?tab=readme-ov-file#start-and-end-of-word
"""  
def finditer(text:str, query:str, *args, **kwargs) -> Iterator:
    expr = fr'\m(?P<result>{__expr(query, False)})\M'
    
    for span, result in __exec(expr, text, *args, **kwargs):
        yield span, result
                      
""" format and OR queries into a singular expression and yield matches
    `text`           : the text to be searched
    `queries`        : Iterable of search terms
    `*args|**kwargs` : passed to `__exec` as remaining args
    
    \m\M: https://github.com/mrabarnett/mrab-regex?tab=readme-ov-file#start-and-end-of-word
"""   
def findany(text:str, queries:list|tuple|set, *args, **kwargs) -> Iterator:
    expr = r'|'.join(map(__expr, queries))
    expr = fr'\m(?P<result>{expr})\M'
    
    for span, result in __exec(expr, text, *args, **kwargs):
        yield span, result
            
""" make multiple consecutive searches
    `text`           : the text to be searched
    `queries`        : Iterable of search terms
    `*args|**kwargs` : passed to `.finditer` as remaining args
"""    
def iterall(text:str, queries:list|tuple|set, *args, **kwargs) -> Iterator:
    # query is managed internally
    if kwargs.get('query'): del kwargs['query']
    
    for query in queries:
        q = query
            
        for span, match in finditer(text, query, *args, **kwargs):
            yield q, span, match
            q = None # only yield `query` the first time it is encountered

