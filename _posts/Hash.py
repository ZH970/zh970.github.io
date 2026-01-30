# 383.赎金信 link:https://leetcode.cn/problems/ransom-note/submissions/694430733/
# hash表练习，记录相应的出现次数
def canConstruct(self, ransomNote: str, magazine: str) -> bool:

    if  (ransomNote in magazine) or (ransomNote in magazine[::-1]):
        return True
    hash = {}
    for m in magazine:
        if m not in hash:
            hash[m] = 0
        hash[m] += 1
    for r in ransomNote:
        if hash.get(r, 0) == 0:
            return False
        else:
            hash[r] -= 1
            continue
            
    
    return True
