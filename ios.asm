.MOD_____________________________________________________________________.
MOD		LDA	M1	
		DIV	M2	
		MUL	M2	
		LDS	M1
		SUBR	A,S
		STS	MR
		RSUB
.PARAM__________________________________________________________________.
M1   		RESW	1	.quotient
M2   		RESW 	1	.dividend
MR   		RESW	1	.modular
._______________________________________________________________________.


.STACK ROUTINES ________________________________________________________.
SINIT		LDA	#STACK
		STA	STACKPTR
		RSUB

PUSH		STA	STEMP
		LDA	STACKPTR
		ADD	#3
		STA	STACKPTR
		LDA	STEMP
		RSUB

POP		STA	STEMP
		LDA	STACKPTR
		SUB	#3
		STA	STACKPTR
		LDA	STEMP
		RSUB
STEMP		RESW	1		. variable used in routines
.PARAM__________________________________________________________________.
STACKPTR	RESW	1
STACK		RESW	10
._______________________________________________________________________.

._______________________________________________________________________.
IOS		LDA	#10
		STA	@STACKPTR
		JSUB	PUSH
		LDA	NUM
IOSS		STA	M1
		LDT	#10
		STT	M2
		JSUB	MOD
		STA	NUM
		LDA	MR

		COMP	#0
		JEQ	IFS
		ADD	#0x30
		STA	@STACKPTR

		JSUB	PUSH
		
		LDA	NUM
		DIV	#10
		STA	NUM

		J	IOSS
	
IFS		JSUB	POP
		LDX	#2
		LDCH	@STACKPTR,X
		WD	#0x05

		LDA	#STACK
		COMP	STACKPTR

		JLT	IFS
		HALT

.PARAM__________________________________________________________________.
NUM		RESW	1
._______________________________________________________________________.

FIRST		JSUB	SINIT

		LDA	#1245		.number to be printed
		STA	NUM
		JSUB	IOS
		HALT

		END	FIRST

