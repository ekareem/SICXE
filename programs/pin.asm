PIN	START	0

.
.	gets length of string
.	A string address
.	S return address
.
STRLEN		CLEAR	X			.get registers ready
		STA	CHRPTR			.character address
		STS	TEMP
		CLEAR	A
	INCR	LDCH	@CHRPTR,X		.get byte at address			.
		COMP	#0
		JEQ	EOS			.if char == 0x00 jump to end of string
		TIXR	X
		J	INCR
	EOS	STX	@TEMP			.save lenght of string
		RSUB
	TEMP	RESW	1
	CHRPTR 	WORD	0			.address of string	
.
.	adds input to memory
.

READ		CLEAR	X
		STA	STRADR			.buffer addres
		CLEAR	A
	TREAD	TD	STDIN			.test device
		JEQ	TREAD
		RD	STDIN			.read input buffer
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
		

	WSTRADR RESW	1
	STDOUT	BYTE	X'05'
.
.	STRCMP TOW STRING
.	RETURNS ANSWER IN SW REGISER
STRCMP		CLEAR	X
		STA	STR1			.string one addre
		STS	STR2			.string tow address
		STT	CLEN			.string length addres
		CLEAR	A
	CFOR	LDCH	@STR1,X
		STA	CTEMP
		LDCH	@STR2,X
		COMP	CTEMP
		JEQ	SAME
		RSUB

	SAME	TIX	@CLEN
		JLT	CFOR
		RSUB

	CTEMP	RESW	1

	STR1  	RESW	1
	STR2 	RESW	1
	CLEN	RESW	1
.
.
.
CHRCMP		STA	BUFADR			.string addre
		STS	INDEX			.string index
		STT	NUM			.number expected at index
		CLEAR	A
		LDX	INDEX
		LDCH	@BUFADR,X
		COMP	NUM
		JNE FAIL
		RSUB
	BUFADR	RESW	1
	INDEX	RESW	1
	NUM	RESW	1
	

P1PR	LDA	#INTRO		.intro statement
	JSUB	WRITE
	
PIN1RD	LDA	#BUFFER		.get pin 1
	JSUB	READ

P1LEN	LDA	#BUFFER		.get lenth of pin
	LDS	#CHRLEN
	JSUB	STRLEN

	LDA	CHRLEN		.get if length of input pin is the same
	COMP	PIN1LEN
	JEQ	PIN1CMP
	J	FAIL

PIN1CMP	LDA	#PIN1
	LDS	#BUFFER
	LDT	#PIN1LEN
	JSUB	STRCMP
	JEQ	P2PR
	J	FAIL
.
.
.
.
P2PR	LDA	#P2INTRO	.intro statement
	JSUB	WRITE

PIN2RD	LDA	#BUFFER		.get pin 2
	JSUB	READ

P2LEN	LDA	#BUFFER		.get lenth of pin 2
	LDS	#CHRLEN
	JSUB	STRLEN

	LDA	CHRLEN		.if length of input pin is the same
	COMP	PIN2LEN
	JEQ	PIN2CMP
	J	FAIL

PIN2CMP	LDA	#BUFFER		.516847923
	LDS	#1
	LDT	#0x31
	JSUB	CHRCMP

	LDA	#BUFFER
	LDS	#7
	LDT	#0x32
	JSUB	CHRCMP

	LDA	#BUFFER
	LDS	#8
	LDT	#0x33
	JSUB	CHRCMP

	LDA	#BUFFER
	LDS	#4
	LDT	#0x34
	JSUB	CHRCMP

	LDA	#BUFFER
	LDS	#0
	LDT	#0x35
	JSUB	CHRCMP

	LDA	#BUFFER
	LDS	#2
	LDT	#0x36
	JSUB	CHRCMP

	LDA	#BUFFER
	LDS	#5
	LDT	#0x37
	JSUB	CHRCMP

	LDA	#BUFFER
	LDS	#3
	LDT	#0x38
	JSUB	CHRCMP

	LDA	#BUFFER
	LDS	#6
	LDT	#0x39
	JSUB	CHRCMP

	LDA	#SUCCESS
	JSUB	WRITE
	J	halt


FAIL	LDA	#FMSG
	JSUB	WRITE

halt	HALT
	

INTRO	BYTE	C'Please input your first PIN (Note--the length of your PIN<=15):'
	BYTE	X'00'
P2INTRO BYTE	C'Please input your second PIN of length 9 (only digits):'
	BYTE	X'00'
SUCCESS BYTE	C'GREAT!! You have deciphered both of your PINs successfully!!'
	BYTE	X'0A'
	BYTE	X'00'
FMSG	BYTE	C'Failure'
	BYTE	X'0A'
	BYTE	X'00'

PIN1	BYTE	C'kc4360715829'
	BYTE	X'00'
PIN1LEN	WORD	*-PIN1-1

PIN2LEN	WORD	9

CHRLEN	WORD	0		.lenth of string
BUFFER	RESB	100

	END	P1PR
