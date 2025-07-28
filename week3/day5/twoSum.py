nums = [2,7,11,15]
target = 17


def twoSum(numbers):
    for i in range (len(numbers)):
        for j in range (i+1, len(numbers)):

            if (numbers[i] + numbers[j]) == target:     
                print (f"index {i} and index {j} ({nums[i]} + {nums[j]} = {target})")
                exit()

indices = twoSum(nums)

   





