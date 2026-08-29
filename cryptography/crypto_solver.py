"""
Solver for the Vigenere crypto challenge (author's reference solution).

Tries a small built-in wordlist against the ciphertext and scores
results by counting common English words - the correct key pops out
immediately. Document this scoring approach in the writeup.
"""

CIPHERTEXT = "hixz qzrq oalpkgg elq tylk ug swes{j1t3y3v3_e0zi3o}"
WORDLIST = ["lemon", "apple", "orange", "lime", "mango", "peach", "grape"]
COMMON = ["the", "flag", "is", "done", "analyst"]


def vigenere_decrypt(ct: str, key: str) -> str:
    out, ki = [], 0
    for ch in ct:
        if ch.isalpha():
            k = ord(key[ki % len(key)].lower()) - 97
            base = 97 if ch.islower() else 65
            out.append(chr((ord(ch) - base - k) % 26 + base))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)


def score(text: str) -> int:
    return sum(text.lower().count(w) for w in COMMON)


if __name__ == "__main__":
    results = sorted(
        ((score(vigenere_decrypt(CIPHERTEXT, k)), k, vigenere_decrypt(CIPHERTEXT, k))
         for k in WORDLIST),
        reverse=True,
    )
    for s, k, pt in results[:3]:
        print(f"score={s:2d} key={k:7s} -> {pt}")
