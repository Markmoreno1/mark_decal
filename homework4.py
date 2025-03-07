cats = list(range(21))
print(cats)
#encountered " 'int' object is not iterable" changed from "list(1-20)" to "list(range(21))"
# encountered +       ~~~~~~Unexpected token 'object' in expression or statement.
#At line:1 char:133
#+ ... bleect is not iterableect is not iterableect is not iterable& C:/User ...
#+                                                                 ~
#the ampersand (&) character is not allowed. The & operator is reserved for future use; wrap an ampersand in double quotation marks ("&") to pass it as part of a string.
#    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
 #   + FullyQualifiedErrorId : UnexpectedToken 
 # fixed by adding spaces on either side of "=" now printed sucessfully

def squarelist(list):
    return[i**2 for i in list]
twocats = squarelist(cats)
print(twocats)

def first_fifteen_elements(list):
    return list[:15]
print(first_fifteen_elements(twocats))
# name 'first_fifteen_elements' is not defined
#prints nothing fixed by adding "print(first_fifteen_elements(twocats))"

def every_fifth_element(list):
    return list[::5]
print(every_fifth_element(twocats))
#syntax error forgot to add ":" at end of first line

def fancy_fun(list):
    flipcats = list[2:]
    return flipcats[::-3]
print(fancy_fun(twocats))

def makefive():
    mcats = []
    cat = 1
    for i in range(5):
        row = []
        for j in range(5):
            row.append(cat)
            cat += 1
        mcats.append(row)

    return mcats
print(makefive())
#return statement was inside the frst for loop so i was only getting [1,2,3,4,5] so i deleted an indent then it worked

def confusedcats(matrix):
    modcats = []
    for row in matrix:
        new_row = []
        for num in row:
            new_row.append("?" if num % 3 == 0 else num)
        modcats.append(new_row)
    return modcats
mcats = makefive()
print(confusedcats(mcats))
#syntax error expected else after if expression fixed by changing "elese" to "else"
#would only work for last block because modcats.append(new_row was outside for loop fixed by indenting)
derpcats = confusedcats(mcats)
def smart_cats_unite(matrix):
    return sum(num for row in matrix for num in row if num !="?")
print(smart_cats_unite(derpcats))