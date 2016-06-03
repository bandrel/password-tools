import sys
import string
import operator

def calc_mask(password):
    mask = ''
    for x in password:
        if x in string.digits:
            mask += '?d'
        elif x in string.uppercase:
            mask += '?u'
        elif x in string.lowercase:
            mask += '?l'
        else:
            mask += '?s'
    return mask


uniquemasks = {}
with open(sys.argv[1], mode="rb") as passwords:
    for password in passwords:
        mask = calc_mask(password.rstrip())
        try:
            uniquemasks[mask] += 1
        except KeyError:
            uniquemasks[mask] = 1

for item in sorted(uniquemasks.items(), key=operator.itemgetter(1), reverse=True)[0:20]:
    print item[0] + '\t\t\t' + str(item[1])












