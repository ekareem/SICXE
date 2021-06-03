.***** PROGRAM MAIN START *****
bf          START   0
loop        TD      idev            .check if device is ready
            JEQ     loop

            JSUB    stackinit       .initialise stack state
            JSUB    cleartape       .clear tape state
            JSUB    readinstr       .load program string from stdin
            JSUB    stackinit       .reset stack pointer to starting position
            JSUB    execute         .execute loaded program
            J       loop            .when program finishes, wait for next one

halt        J       halt

.***** INTERPRETER EXECUTION *****
execute     STL     retaddr         .save return address
            LDA     #tape2          .initialise tape state
            STA     tapeptr

execloop    CLEAR   A               .load instruction
            LDCH    @stackptr       .if 0x00 finish execution
            COMP    #0x00
            JEQ     endexec

            COMP    cinc            .otherwise, check for appropriate command
            JEQ     incr

            COMP    clshift
            JEQ     lshift

            COMP    crshift
            JEQ     rshift

            COMP    cdec
            JEQ     decr

            COMP    cwrite
            JEQ     writeout

            COMP    cloops
            JEQ     loops

            COMP    cloope
            JEQ     loope

            COMP    cread
            JEQ     readin

continue    JSUB    stackpush       .go to next instruction
            J       execloop

endexec     LDCH    #0x0A
            WD      odev
            LDL     retaddr         .restore return address, finish program execution
            RSUB

.***** BRAINFUCK PROGRAM COMMAND EXECUTION *****
loops       LDCH    @tapeptr        .handle command for loop start, load current cell
            COMP    #0x00
            JGT     endls
            LDX     #1
            RMO     X,S
            LDT     #0
whiles      COMPR   T,S
            JEQ     endls
            JSUB    stackpush
            LDCH    @stackptr
            COMP    cloope
            JEQ     ldecs
            COMP    cloops
            JEQ     lincs
            J       endifs
ldecs       SUBR    X,S
            J       endifs
lincs       ADDR    X,S
endifs      J       whiles
endls       JSUB    clr
            J       continue

loope       LDCH    @tapeptr    .handle command for loop end, load current cell
            COMP    #0x00
            JEQ     endle       .check if cell is empty
            LDX     #1          .set initial loop counter state
            RMO     X,S
            LDT     #0
whilee      COMPR   T,S         .until loop counter is 0 (checking nested loops)
            JEQ     endle
            JSUB    stackpop	.check if current instruction is loop start/end
            LDCH    @stackptr
            COMP    cloops
            JEQ     ldece
            COMP    cloope
            JEQ     lince

            J       endife      .increment or decrement program loop counter
ldece       SUBR    X,S
            J       endife
lince       ADDR    X,S
endife      J       whilee      .continue Brainfuck program loop execution
endle       JSUB    clr         .continue to execution
            J       continue

lshift      LDA     tapeptr     .shift tape left
            SUB     #1
            STA     tapeptr
            J       continue

rshift      LDA     tapeptr     .shift tape right
            ADD     #1
            STA     tapeptr
            J       continue

incr        LDCH   @tapeptr     .increment cell value
            ADD     #1
            STCH   @tapeptr
            J       continue

decr        LDCH    @tapeptr    .decrement cell value
            .COMP    =0          .cannot go lower than 0
            .JEQ     enddecr
            SUB     #1
            STCH    @tapeptr
enddecr     J       continue

readin      RD      idev        .read character from stdin
            STCH    @tapeptr
            J       continue

writeout    LDCH    @tapeptr    .print character to stdout
            WD      odev
            J       continue

.***** HELPER ROUTINES *****
clr         CLEAR   A           .clear register state
            CLEAR   X
            CLEAR   S
            CLEAR   T
            RSUB

.subroutine reads instructions from stdin to memory
readinstr   STL     retaddr
readloop    CLEAR   A
            RD      idev        .while not end of line, read commands from input
            COMP    #0x0A  .check for EOT character
            JEQ     finish
            STCH    @stackptr   .save each command to stack
            JSUB    stackpush
            J       readloop

finish      LDA     #0
            STCH    @stackptr   .null byte signifies end of instructions
            LDL     retaddr
            RSUB

cleartape   STL     retaddr
            CLEAR   A
            CLEAR   S
            LDX     #tapeend    .reset tape pointer, set final address
            LDA     #tape1
            STA     tapeptr

loopclear   CLEAR   A
            STCH    @tapeptr    .set memory cell to 0x00
            LDA     tapeptr     .load current tape pointer and increment
            ADD     #1
            COMPR   X,A         .if end of tape, finish clearing
            JEQ     cleared
            STA     tapeptr

            J       loopclear

cleared     JSUB    clr
            LDL     retaddr
            RSUB

.***** STACK ROUTINES *****
stackinit   LDA     #stackstart
            STA     stackptr
            CLEAR   A
            RSUB

stackpush   STA     tmpA        .temporarily save value of A
            LDA     stackptr    .load stackptr to A and increment
            ADD     #1
            STA     stackptr
            LDA     tmpA
            RSUB

stackpop    STA     tmpA
            LDA     stackptr    .load stackptr to A and decrement
            SUB     #1
            STA     stackptr
            LDA     tmpA
            RSUB

.***** VARIABLES *****
idev        BYTE    X'f1'       .stdin
odev        BYTE    X'05'       .stdout

stackptr    RESW    1           .pointer to current instruction on stack
tapeptr     RESW    1           .pointer to current cell on tape

tmpA        RESW    1           .temporary A register variable
stackstart  RESB    400         .reserve 400B on stack, increase at own peril

.Brainfuck commands
crshift     WORD    X'00003C'   .< shift tape right
clshift     WORD    X'00003E'   .> shift tape left
cinc        WORD    X'00002B'   .+ increment cell value
cdec        WORD    X'00002D'   .- decrement cell value
cread       WORD    X'00002C'   ., read byte(1 character) from stdin
cwrite      WORD    X'00002E'   .. write byte (1 character) to stdout
cloops      WORD    X'00005B'   .[ start of a loop (can be nested)
cloope      WORD    X'00005D'   .] end of a loop (can be nested)

tape1       RESB    200         .tape divided in 2 halves, starts at middle
tape2       RESB    200         .limited to 400B, increase at own peril
tapeend     EQU     *

retaddr     RESW    1           .temporary link register variable
            
            END     loop