first	LDA	#stack
	JSUB	stackinit

push	STL	@stackptr	. push L
	JSUB	stackpush

pop	JSUB	stackpop	. pop X
	LDX	@stackptr

.---------------------------- STACK ROUTINES -----------------------------.
stackinit	STA	stackptr
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
stackptr	RESW	1
stack		RESW	100	. stack size is 100 words

		END	first