ttt		START	0
first		JSUB	stackinit

		JSUB	echoclr
		JSUB	printInstr
		JSUB	resetBoard	. board was modified by instr
		JSUB	echoclr
		JSUB	printBoard

play		JSUB	getMove		. A = player1's move
		RMO	A,X		. move is index to board
		LDA	#88		. store player1's token to board
		STCH	board,X
		JSUB	echoclr		. update screen
		JSUB	printBoard
		JSUB	checkWinner	. check if player1 won
		COMP	#88
		JEQ	player1win
		LDA	moves		. Check if this move is last. This
		ADD	#1		. check is only needed after
		STA	moves		. player1's move because a tie
		COMP	#9		. happens on 9th move that player1
		JEQ	tie		. always has.

		JSUB	getMove		. A = player2's move
		RMO	A,X		. move is index to board
		LDA	#79		. store player2's token to board
		STCH	board,X
		JSUB	echoclr		. update screen
		JSUB	printBoard
		JSUB	checkWinner	. check if player2 won
		COMP	#79
		JEQ	player2win
		LDA	moves		. increase moves
		ADD	#1
		STA	moves
		J	play

player1win	LDA	#88		. print player1's token
		JSUB	echoch
		J	printWin

player2win	LDA	#79
		JSUB	echoch		. print player2's token

printWin	LDA	#winStr
		JSUB	echostr
		JSUB	echonl
		J	halt

tie		LDA	#tieStr		. print tie result
		JSUB	echostr
		JSUB	echonl

halt		J	halt

moves		WORD	0
winStr		BYTE	C' winsn'
endWinStr	BYTE	0
tieStr		BYTE	C'It is a tien'
endTieStr	BYTE	0


.----------------------------  STDOUT ROUTINES ---------------------------.
. write character given in A to stdout
echoch	WD	stdout
	RSUB


. write new line character to stdout
echonl	STA	@stackptr	. push A
	
	LDA	#10
	WD	stdout

	LDA	@stackptr	. pop A
	RSUB


. write C-style string on address in A to stdout
echostr	STA	addr

char	LDCH	@addr	. while character != 0 print character, increase ptr
	AND	#255
	COMP	#0
	JEQ	return
	WD	stdout
	LDA	addr
	ADD	#1
	STA	addr
	J	char
return	RSUB
addr	RESW	1


. jump to the start of the screen
echoclr	STL	@stackptr	. push L
	JSUB	stackpush
	STA	@stackptr	. push A
	JSUB	stackpush

	LDA	#escapec
	JSUB	echostr
	LDA	#escapem
	JSUB	echostr

	JSUB	stackpop	. pop A
	LDA	@stackptr
	JSUB	stackpop	. pop L
	LDL	@stackptr
	RSUB
escapec	BYTE	X'1B'
	BYTE	C'[2J'
endescc	BYTE	0
escapem	BYTE	X'1B'
	BYTE	C'[0;0H'
endescm	BYTE	0


teststr	BYTE	C'MERLJAK'
null		BYTE	0
number		WORD	1284993


.------------------------- TIC TAC TOE ROUTINES --------------------------.

. Print board.
printBoard	STL	@stackptr	. push L
		JSUB	stackpush
		STA	@stackptr	. push A
		JSUB	stackpush
		STX	@stackptr	. push X
		JSUB	stackpush

		CLEAR	X
			
		. print lines in a loop
printLine	LDCH	board,X	. load left token, print it
		JSUB	printCell
		LDA	#1		. X++
		ADDR	A,X

		LDCH	#124		. print |
		WD	stdout

		LDCH	board,X	. load middle token, print it
		JSUB	printCell
		LDA	#1		. X++
		ADDR	A,X

		LDCH	#124		. print |
		WD	stdout

		LDCH	board,X	. load right token, print it
		JSUB	printCell
		LDA	#1		. X++
		ADDR	A,X

		JSUB	echonl

		LDA	#8		. last line?
		COMPR	X,A
		JGT	endBoard	. yes, go to end
		JSUB	printDashLine	. no, print dash line
		J	printLine

endBoard	JSUB	stackpop	. pop X
		LDX	@stackptr
		JSUB	stackpop	. pop A
		LDA	@stackptr
		JSUB	stackpop	. pop L
		LDL	@stackptr
		RSUB


. Print instructions for game. Routine overwrites global variable
. board, with values 0 - 8.
printInstr	STL	@stackptr	. push L
		JSUB	stackpush
		STA	@stackptr	. push A
		JSUB	stackpush
		STX	@stackptr	. push X
		JSUB	stackpush
		STT	@stackptr	. push T
		JSUB	stackpush

		LDA	#instr0		. print first two lines
		JSUB	echostr
		JSUB	echonl
		LDA	#instr1
		JSUB	echostr
		JSUB	echonl
		JSUB	echonl

		LDA	#48
		CLEAR	X
		LDT	#1
instrCells	STCH	board,X	. fill board with ascii numbers
		ADDR	T,A
		ADDR	T,X
		STA	cellNum
		RMO	X,A
		COMP	#9
		LDA	cellNum
		JLT	instrCells

		JSUB	printBoard	. print board
		JSUB	echonl

		LDA	#instr2		. print instr2,3,4,5,6
		JSUB	echostr
		JSUB	echonl
		LDA	#instr3
		JSUB	echostr
		JSUB	echonl
		LDA	#instr4
		JSUB	echostr
		JSUB	echonl
		LDA	#instr5
		JSUB	echostr
		JSUB	echonl
		LDA	#instr6
		JSUB	echostr
		JSUB	echonl

		LDA	#instr7		. print prompt and wait
		JSUB	echostr
		RD	stdin

		JSUB	stackpop	. pop T
		LDT	@stackptr
		JSUB	stackpop	. pop X
		LDX	@stackptr
		JSUB	stackpop	. pop A
		LDA	@stackptr
		JSUB	stackpop	. pop L
		LDL	@stackptr
		RSUB
instr0		BYTE	C'Welcome to Tic Tac Toe!'
endinstr0	BYTE	0
instr1		BYTE	C'Board cells are numbered as follows:'
endinstr1	BYTE	0
instr2		BYTE	C'When prompted, type in a cell number to'
endinstr2	BYTE	0
instr3		BYTE	C'place your token theren'
endinstr3	BYTE	0
instr4		BYTE	C'When entering cell number PLEASE enter only'
endinstr4	BYTE	0
instr5		BYTE	C'one digit or you will break the programn'
endinstr5	BYTE	0
instr6		BYTE	C'Player 1 is X and player 2 is On'
endinstr6	BYTE	0
instr7		BYTE	C'Press ENTER to continue nnn'
endinstr7	BYTE	0
cellNum		RESW	1


. Return board index (0-8) in A. Function is not robust, it expects
. only one character entered on every prompt. If more or less is
. given, program will behave incorrectly.
getMove		STL	@stackptr	. push L
		JSUB	stackpush

getIndex	LDA	#prompt		. print question
		JSUB	echostr

		CLEAR	A		. get board index
		RD	stdin
		STA	@stackptr	. store A on stack temporarily
		RD	stdin		. read newline from ENTER press
		LDA	@stackptr	. get given character back to A
		COMP	#48		. check for errors
		JLT	rangeError
		COMP	#56
		JGT	rangeError
		SUB	#48		. right ascii num, convert to int
		RMO	A,X		. check if this cell is taken
		LDCH	board,X
		COMP	#32		. error if different from SPACE
		JGT	takenError	
		RMO	X,A		. not taken, copy index back to A
		J	endMove

rangeError	LDA	#rangeMsg
		JSUB	echostr
		J	getIndex

takenError	LDA	#takenMsg
		JSUB	echostr
		J	getIndex

endMove		JSUB	stackpop	. pop L
		LDL	@stackptr
		RSUB
prompt		BYTE	C'Enter a digit (0-8): '
endPrompt	BYTE	0
rangeMsg	BYTE	C'Invalid inputn '
endRangeMsg	BYTE	0
takenMsg	BYTE	C'Space is already takenn '
endTakenMsg	BYTE	0


. Print line of dashes and new line at the end.
.
. Function uses static string to print line because it's faster than
. calling printch for every dash.
printDashLine	STL	@stackptr	. push L
		JSUB	stackpush

		LDA	#dashLine
		JSUB	echostr
		JSUB	echonl

		JSUB	stackpop
		LDL	@stackptr	. pop L
		RSUB
dashLine	BYTE	C'-----------'	. dash C-string
endLine		BYTE	0


. Print one cell of board. Character is in A. 
printCell	STL	@stackptr	. push L
		JSUB	stackpush

		STCH	character	. store character locally
		LDA	#32		. print space
		WD	stdout
		LDCH	character	. print character
		WD	stdout
		LDA	#32		. print space
		WD	stdout
		LDCH	character	. function returns A untouched

		JSUB	stackpop
		LDL	@stackptr
		RSUB
character	RESB	1


. Return winning token or SPACE if no winner in A.
checkWinner	STL	@stackptr	. push L
		JSUB	stackpush
		STS	@stackptr	. push S
		JSUB	stackpush
		STT	@stackptr	. push T
		JSUB	stackpush
		STX	@stackptr	. push X
		JSUB	stackpush

		LDA	#winPositions	. store pointer to win positions
		STA	positionPtr	. to local var
nextPosition	LDA	@positionPtr	. store current position to
		STA	position	. position
		CLEAR	A		. reset index for position
		STA	positionIx
		LDX	positionIx
		LDCH	position,X	. load first board index
		RMO	A,T		. save board index to T
		LDA	positionIx	. increase position index
		ADD	#1
		STA	positionIx	
		RMO	T,X		. move board index to X
		LDCH	board,X	. use index to fetch token
		RMO	A,S		. S holds current token
		COMP	#32		. if token is space continue
		JEQ	increasePosPtr

nextIndex	LDX	positionIx	. get next index for position
		LDCH	position,X	. get new board index
		RMO	A,T		. save board index to T
		LDA	positionIx	. increase position index
		ADD	#1
		STA	positionIx	
		RMO	T,X		. move board index to X
		LDCH	board,X	. use index to fetch token
		COMPR	A,S		. position[i] == position[i-1]?
		JGT	increasePosPtr	. different; try next pos
		JLT	increasePosPtr	. different; try next pos
		LDA	positionIx	. compare if last index
		COMP	#3
		JLT	nextIndex	. loop if not last
		CLEAR	A		. last element, equal all previous
		RMO	S,A		. so this is winner; return it
		J	returnWinner

increasePosPtr	LDA	positionPtr	. increase pos pointer
		ADD	#3
		STA	positionPtr
		SUB	#winPositions	. compare if over last pos
		COMP	#24
		JLT	nextPosition
		LDA	#32		. over last pos, return SPACE

returnWinner	JSUB	stackpop	. pop X
		LDX	@stackptr
		JSUB	stackpop	. pop T
		LDT	@stackptr
		JSUB	stackpop	. pop S
		LDS	@stackptr
		JSUB	stackpop	. pop L
		LDL	@stackptr
		RSUB
winPositions	BYTE	X'000102'
		BYTE	X'030405'
		BYTE	X'060708'
		BYTE	X'000306'
		BYTE	X'010407'
		BYTE	X'020508'
		BYTE	X'000408'
		BYTE	X'060402'
positionPtr	WORD	1	. used for iteration over all positions
position	WORD	1	. stores current position
positionIx	WORD	1	. used to iterate over position


. Reset board: set all cells to spaces.
resetBoard	STL	@stackptr	. push L
		JSUB	stackpush
		STA	@stackptr	. push A
		JSUB	stackpush
		STX	@stackptr	. push X
		JSUB	stackpush

		CLEAR	X		. set index to 0
resetCell	LDA	#32		. load SPACE character in A
		STCH	board,X
		LDA	#1
		ADDR	A,X
		LDA	#9
		COMPR	X,A
		JLT	resetCell

		JSUB	stackpop	. pop X
		LDX	@stackptr
		JSUB	stackpop	. pop A
		LDA	@stackptr
		JSUB	stackpop	. pop L
		LDL	@stackptr
		RSUB


.---------------------------- STACK ROUTINES -----------------------------.
stackinit	LDA	#stack
		STA	stackptr
		RSUB


stackpush	STA	tempa
		LDA	stackptr
		ADD	#3
		STA	stackptr
		LDA	tempa
		RSUB


stackpop	STA	tempa
		LDA	stackptr
		SUB	#3
		STA	stackptr
		LDA	tempa
		RSUB
tempa		RESW	1		. variable used in routines


.--------------------------------- DATA ----------------------------------.
board		BYTE	C'         '
player		RESB	1
computer	RESB	1
stdin		BYTE	0xf1
stdout		BYTE	0x05
stackptr	RESW	1
stack		RESW	100	. stack size is 100 words