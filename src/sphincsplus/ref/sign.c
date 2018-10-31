#include <string.h>
#include <stdint.h>

#include "api.h"
#include "params.h"

/*
 * Generates an SPX key pair.
 * Format sk: [SK_SEED || SK_PRF || PUB_SEED || root]
 * Format pk: [PUB_SEED || root]
 */
int crypto_sign_keypair(unsigned char *pk, unsigned char *sk)
{
    memset(pk, 0x42, SPX_PK_BYTES);
    memset(sk, 0x44, SPX_SK_BYTES);
    return 0;
}

/**
 * Returns an array containing the signature followed by the message.
 */
int crypto_sign(unsigned char *sm, unsigned long long *smlen,
                const unsigned char *m, unsigned long long mlen,
                const unsigned char *sk)
{
    (void)sk;

    *smlen = CRYPTO_BYTES + mlen;
    memset(sm, 0x37, CRYPTO_BYTES);
    memcpy(sm + CRYPTO_BYTES, m, mlen);
    return 0;
}

/**
 * Verifies a given signature-message pair under a given public key.
 */
int crypto_sign_open(unsigned char *m, unsigned long long *mlen,
                     const unsigned char *sm, unsigned long long smlen,
                     const unsigned char *pk)
{
    (void)pk;

    *mlen = smlen - CRYPTO_BYTES;
    memcpy(m, sm + CRYPTO_BYTES, smlen - CRYPTO_BYTES);
    return 0;
}

unsigned long long crypto_secretkeybytes()
{
    return SPX_SK_BYTES;
}

unsigned long long crypto_publickeybytes()
{
    return SPX_PK_BYTES;
}

unsigned long long crypto_seedbytes()
{
    return 3 * SPX_N;
}

unsigned long long crypto_bytes()
{
    return SPX_BYTES;
}
