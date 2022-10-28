

# https://stackoverflow.com/a/64927461/14892663
# 123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-
chars = "JhdXpZ_LsyD9biSk7AVWGzHgYqx41Nm6MKOI5eow-Qnv2lrtBjUcRuCfaEFP38T"
length = len(chars)

def int_to_id(n):
    if n == 0:
        return "000"

    result = ""
    remain = n
    while remain > 0:
        pos = remain % length
        remain = remain // length
        result = chars[pos] + result

    if len(result) < 3:
        result = "0" * (3 - len(result)) + result
        
    return result
