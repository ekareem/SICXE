	LDS	#3	.Initialize Register S to 3
	LDT	#15	.Initialize Register T to 15
	LDX	#0	.Initialize Index Register to 0
ADDLP	LDA	ALPHA,X	.Load Word from ALPHA into Register A
	ADD	BETA,X	.Add ord From BETA
	STA	GAMMA,X	.Store the Result in a work in GAMMA
	ADDR	S,X	.ADD 3 to INDEX value
	COMPR	X,T	.Compare new INDEX value to 15
	JLT	ADDLP	.Loop if INDEX value is less than 15
	HALT
ALPHA	RESW	5
BETA	RESW	5
GAMMA	RESW	5