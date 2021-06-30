        START   0x1000
FIRST   LDA     #1
        LDS     #2
        COMPR   A,S
        JNE     FIRST
        END FIRST
