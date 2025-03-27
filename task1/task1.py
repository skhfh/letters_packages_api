def simple_solution(nums):
    result = []
    n = len(nums)
    if n > 2:
        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    if nums[i] * nums[j] * nums[k] == 0:
                        result.append([nums[i], nums[j], nums[k]])
    return result


def simple_solution_without_duplicates(nums):
    result = []
    n = len(nums)
    if n > 2:
        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    if (nums[i] * nums[j] * nums[k] == 0 and
                            not [nums[i], nums[j], nums[k]] in result):
                        result.append([nums[i], nums[j], nums[k]])
    return result


# Не учитывает все возможные комбинации элементов
# (если принимать каждый 0 за уникальный элемент
# с дублирующимися триплетами
def updated_solution(nums):
    result = []
    zeros_count = 0
    positive_nums = []

    if len(nums) < 3:
        return result

    for num in nums:
        if num == 0:
            zeros_count += 1
        else:
            positive_nums.append(num)

    if zeros_count == 0:
        return result

    for i in range(len(positive_nums) - 1):
        for j in range(i + 1, len(positive_nums)):
            result.append([positive_nums[i], positive_nums[j], 0])
    if zeros_count > 1:
        for i in range(len(positive_nums)):
            result.append([positive_nums[i],0, 0])
    if zeros_count > 2:
        result.append([0, 0, 0])

    return result
