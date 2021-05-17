DEMO 	START	0

COUT	CLEAR X			.X = 0
	STA	BUFADR		.*BUFFER = A
	CLEAR	A
WRITE	TD	STDOUT
	JEQ	WRITE		
	LDCH	@BUFADR,X	.CH = A[X]
	WD	STDOUT		.print CH to output devide
	TIXR	X		.X++
	COMP	#0x00		.if CH == \0		.end of string
	JEQ	WEOB		.	exit 
	J	WRITE		.else: write next index
WEOB	RSUB
	BUFADR RESW	1	.buffer address
	STDOUT	BYTE	X'05'		.output devide

PRINT	LDA	#STRING		.A = addres of STRING		
	JSUB	COUT
	HALT

STRING	BYTE	C'this is a sicxe demo'
	END	PRINT		.first executed instuction
