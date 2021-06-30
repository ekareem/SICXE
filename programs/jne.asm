        START   0
FIRST   LDA     #1
        LDS     #2
        COMPR   A,S
        LDB     #10
        BASE    10
        JNE     FIRST
        END FIRST
