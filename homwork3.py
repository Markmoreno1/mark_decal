#power funtion without ** or pow
def computepower(x, y):
    result = 1
    for n in range(y):
        result *= x
    return result
print(computepower(2, 3))

# how hot is it
def  temperatureRange(readings):
     return(min(readings),max(readings))    
readings = [15, 14, 17, 20, 23, 28, 20]
print(temperatureRange(readings))

# is it weekend
def isWeekend(day):
    if day == 7 or day == 6:
        print("yes")
        return True
    else:
        print("no")
        return False
day = 6
print(isWeekend(day))

# fuel efficency
def fuel_efficiency(distance, fuel):
    mpg = distance/fuel
    return round(mpg,2)
print(fuel_efficiency(70, 21.5))

#secret code possibly use modulus % or floor devision \\
def  decodeNumbers(n):
    a=n % 10
    remainder= n // 10
    num_digits = 0
    b = remainder
    while remainder > 0:
        remainder//= 10
        num_digits += 1
    c = a*(10**num_digits) + b
    return c
print(decodeNumbers(12345))

# min max without min max for loop
def find_min_with_for_loop(nums):
    min_val = nums[0]
    for num in nums:
        if num < min_val:
            min_val = num
    return min_val

nums = [2024, 98, 131, 2, 3, 72]
print(find_min_with_for_loop(nums))

def find_max_with_for_loop(nums):
    max_val = nums[0]
    for num in nums:
        if num > max_val:
            max_val = num
    return max_val

nums = [2024, 98, 131, 2, 3, 72]
print(find_max_with_for_loop(nums))

# find min max without min max while loop
def find_min_with_while_loop(nums):
    min_val = nums[0]
    i = 1
    while i < len(nums):
        if nums[i] < min_val:
            min_val = nums[i]
        i += 1
    return min_val
nums = [2024, 98, 131, 2, 3, 72]
print(find_min_with_while_loop(nums))

def find_max_with_while_loop(nums):
    max_val = nums[0]
    i = 1
    while i < len(nums):
        if nums[i] > max_val:
            max_val = nums[i]
        i += 1
    return max_val
nums = [2024, 98, 131, 2, 3, 72]
print(find_max_with_while_loop(nums))

#vowel problem
def vowel_and_consonant_count(text):
    vowels = "aeiouAEIOU"
    vowel_count = 0
    con_count = 0
    for char in text:
        if char .isalpha():
            if char in vowels:
                vowel_count += 1
            else:
                con_count += 1
    return(vowel_count,con_count)           

text = "UC Berkeley, founded in 1868!"  
print(vowel_and_consonant_count(text)) 

# digit sum
def digital_root(num):
    sum = 0
    while num > 0:
        digit = num % 10
        sum += digit
        num = num // 10
    return(sum)

num = 2468
print(digital_root(num))