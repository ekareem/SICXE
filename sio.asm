.
.	gets length of string
.	A string address
.	S return address
.
STRLEN	CLEAR	X			.get registers ready
	STA	CHRPTR			.character address
	STS	TEMP
	CLEAR	A
INCR	LDCH	@CHRPTR,X		.get byte at address			.
	COMP	#0
	JEQ	EOS			.if char == 0x00 jump to end of string
	TIXR	X
	J	INCR
EOS	STX	@TEMP			.save lenght of string
	LDA	@TEMP
	SUB	#1
	STA	@TEMP
	RSUB
TEMP	RESW	1
CHRPTR 	WORD	0			.address of string	
.
.	adds input to memory
.

READ		CLEAR	X
	STA	STRADR			.buffer addres
	CLEAR	A
TREAD	TD	STDIN
	JEQ	TREAD
	RD	STDIN
	COMP	#0x0A
	JEQ	EOB
	STCH	@STRADR,X
	TIXR	X	
	J	TREAD
EOB	LDCH	#0x00
	STCH	@STRADR,X
	RSUB
STRADR	RESW	1
STDIN	BYTE	X'F1'

.
.	prints char from spcified memory location until a null is hit
.
WRITE		CLEAR X
	STA	WSTRADR		.location to print from
	CLEAR	A
TWRITE	TD	STDOUT
	JEQ	TWRITE
	LDCH	@WSTRADR,X
	WD	STDOUT
	TIXR	X
	COMP	#0x00
	JEQ	WEOB
	J	TWRITE
WEOB	RSUB
	
.
.
POW	LDA	P2
	COMP	#0	.if p2 == 0
	LDA	#1
	STA	PPR
	JEQ	PD

	LDA	P2
	COMP	#1	.if p2 == 1
	LDA	P1
	STA	PPR
	JEQ	PD

	LDA	P1
	STA	PPR

POWS	LDA	PPR
	MUL	P1
	STA	PPR
	LDA	P2
	SUB	#1
	STA	P2
	SUB	#1
	COMP	#0
	JEQ	PD
	J	POWS
PD	RSUB

P1	RESW	1
P2	RESW	1
PPR	RESW	1
.
.

WSTRADR RESW	1
STDOUT	BYTE	X'05'

FIRST	LDA	#BUFFER
	JSUB	READ

	LDA	#BUFFER
	LDS	#CHARLEN
	JSUB	STRLEN
	CLEAR	X

SOI	LDA 	#10
	STA	P1
	LDA	CHARLEN
	STA	P2
	JSUB	POW

	
	LDCH	BUFFER,X
	AND	#0xff
	SUB	#0x30
	MUL	PPR
	LDS	NUM
	ADDR	S,A
	STA	NUM
	
	LDA	CHARLEN
	COMP	#0
	JEQ	halt
	SUB	#1
	STA	CHARLEN
	TIXR	X
	J	SOI	

halt 	HALT
TEMP	RESW	1
NUM	RESW	1
CHARLEN	RESW	1
BUFFER	RESB	10

	END	FIRST