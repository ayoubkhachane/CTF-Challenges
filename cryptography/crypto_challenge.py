"""
CTF Cryptography challenge - Vigenere cipher.

Run this to regenerate the challenge file (challenge.txt).
Players receive challenge.txt plus the hint below; the key itself
is NOT given - the hint points to it.

Key:    LEMON  (hint: "a 5-letter citrus fruit")
Cipher: Vigenere, letters only - digits/braces/underscores untouched.
"""

KEY = "LEMON"
PLAINTEXT = "well done analyst the flag is flag{v1g3n3r3_s0lv3d}"
HINT = ("Classical polyalphabetic cipher. "
        "The key is a 5-letter citrus fruit. Letters only were shifted.")


def vigenere_encrypt(plaintext: str, key: str) -> str:
    out, ki = [], 0
    for ch in plaintext:
        if ch.isalpha():
            k = ord(key[ki % len(key)].lower()) - 97
            base = 97 if ch.islower() else 65
            out.append(chr((ord(ch) - base + k) % 26 + base))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)


if __name__ == "__main__":
    ct = vigenere_encrypt(PLAINTEXT, KEY)
    with open("challenge.txt", "w") as f:
        f.write(f"Ciphertext:\n{ct}\n\nHint:\n{HINT}\n")
    print("challenge.txt written:")
    print(ct)
