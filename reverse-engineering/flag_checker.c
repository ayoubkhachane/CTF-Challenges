/*
 * CTF Reverse-Engineering challenge - "SecureVault key checker"
 *
 * Build:   gcc -O2 -o flag_checker flag_checker.c
 * Solve path (documented in writeup):
 *   1. `strings flag_checker`  -> decoy flag visible, real one is not
 *   2. Disassemble (objdump -d / Ghidra) -> XOR loop with key 0x5A
 *   3. Extract the `enc` byte array, XOR each byte with 0x5A -> real flag
 *
 * The flag itself is never stored in cleartext in the binary.
 */
#include <stdio.h>
#include <string.h>

/* "flag{x0r_h1dd3n_k3y}" XOR 0x5A */
static const unsigned char enc[] = {
    0x3c, 0x36, 0x3b, 0x3d, 0x21, 0x22, 0x6a, 0x28, 0x05, 0x32,
    0x6b, 0x3e, 0x3e, 0x69, 0x34, 0x05, 0x31, 0x69, 0x23, 0x27
};
#define ENC_LEN (sizeof(enc) / sizeof(enc[0]))
#define XOR_KEY 0x5A

/* Decoy planted for `strings` - solving hint, not the answer */
static const char *decoy = "flag{n0t_th3_r34l_0ne}";

int main(void) {
    char input[64];

    puts("SecureVault Access Terminal v1.0");
    puts("(c) 2024 - authorized keys only");
    printf("Enter access key: ");

    if (!fgets(input, sizeof(input), stdin)) {
        return 1;
    }
    input[strcspn(input, "\n")] = '\0';

    if (strlen(input) != ENC_LEN) {
        puts("Access denied.");
        return 1;
    }

    for (size_t i = 0; i < ENC_LEN; i++) {
        if (((unsigned char)input[i] ^ XOR_KEY) != enc[i]) {
            puts("Access denied.");
            return 1;
        }
    }

    (void)decoy; /* keep the decoy in the binary, unused on purpose */
    puts("Access granted. Flag accepted!");
    return 0;
}
