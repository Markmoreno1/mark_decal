#pwd
#ls
#cd brianna_repo, giy pull
#mv homework.py /judy_decal/homework
#cat homework.py or less homework.py
# either nano homework/homework.py or the same with vim
# git add homework.py, git commit -m"adding homework.py", git push origin main, --- it gets mad at me, git push origin master
# git pull, git push origin main, if that dosent work git push origin master
# ~/Recent/

def checkdata(input):
    return type(input)
print(checkdata(3.14))
print(checkdata(True))

def evenorodd(input):
    if input % 2 == 0:
        return 'even'
    else:
        return 'odd'

print(evenorodd(7))
print(evenorodd(10))

def loopsum(input):
    total = 0
    for input in numbers:
        total += input
    return total
numbers=[1, 2, 3, 4, 5]
print(loopsum(numbers))

def doublelist(list):
    list2=[]
    for item in list:
        list2.extend([item,item])
    return list2
print(doublelist(['a','b','c']))

def square(num):
    return num * num
print(square(7))
#the issue was a missing ":" which gives a syntax error..... i do this way too often :'[
