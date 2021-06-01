COPY	START	0	.copy the file form INPUT to OUTPUT
FIRST	CLEAR   L
	STL	RETADR	.Save Return address
	LDB	#LENGTH	.establish base register
	BASE	LENGTH	
CLOOP	+JSUB	RDREC	.Read INPUT Record
	LDA	LENGTH	.Test for EOF (Length = 0)
	COMP	#0
	JEQ	ENDFIL	.Exit if EOF found
	+JSUB	WRREC	.Write OUTPUT Record
	J	CLOOP	.Loop
ENDFIL	LDA	EOF	.Insert End Of File Marker
	STA	BUFFER
	LDA	#3	.Set LENGTH = 3
	STA	LENGTH
	+JSUB	WRREC	.write EOF
	J	@RETADR	.Return to Caller
EOF	BYTE	C'EOF'
RETADR	RESW	1
LENGTH	RESW	1	.LENGTH of Record
BUFFER	RESB	4096	.4096-BYTE Buffer area
.
.	SUBROUTINE TO READ RECORD INTO BUFFER
.
RDREC	CLEAR	X	.Clear Loop counter
	CLEAR	A	.Clear A to Zero
	LDS	#0x0A	.Clear S to Zero
	+LDT	#4096
RLOOP	TD	INPUT	.Test INPUT device
	JEQ	RLOOP	.LOOP until ready
	RD	INPUT	.READ character into Register A
	COMPR	A,S	.TEST for End Of Record (X'00')
	JEQ	EXIT	.EXIT loop if EOR
	STCH	BUFFER,X	.STORE character in BUFFER
	TIXR	T	.LOOP unless max Length has been reached
	JLT	RLOOP
EXIT	STX	LENGTH	.SAVE record length
	RSUB		.Return to caller
INPUT	BYTE	X'F1'	.CODE for Input device
.
.	SUBROUTINE TO WRITE RECORD FROM BUFFER
.
WRREC	CLEAR	X	.CLEAR loop counter
	LDT	LENGTH	
WLOOP	TD	OUTPUT	.Test OUTPUT Device
	JEQ	WLOOP	.Loop Until Ready
	LDCH	BUFFER,X	.GET character form BUFFER
	WD	OUTPUT	.WRITE character
	TIXR	T	.LOOP until all characters have been written
	JLT	WLOOP
	RSUB		.Return to caller
OUTPUT	BYTE	X'05'	.CODE for OUPUT device
	END	FIRST

	