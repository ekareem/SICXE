# SICXE

**how to run** 
    
  py main.py (args)
   
  get help

  py main.py help
    
    -asm : required flag creates object code and object program from assembly file
            <asm file> : assembles file to object code of .obj

    -bug : required flag debugs assembly or object file
            -o <obj file> : debug program from object file
            -a <asm file> : debug program from assembly file
            -l <memory file> : loads to memory file to machine memory

    -run : required flag runs an object file or assembly file
            -a <asm file> : run program from assmble file
            -o <obj file> : run program from object file
            -w <optional memory file> : writes to memory file
            -l <optional memory file> : loads to memory file to machine memory
 
  **ASSEMBLER**
  
  py main.py -asm (filename)

  **DEBUGGER**
  
  py main.py -bug -a  (assembleyfile)
  
  or
  
  py main.py -bug -o (objectfile)
  
  **RUN PROGRAM**

  py main.py -run -a  (assembleyfile)
  
  or
  
  py main.py -run -o (objectfile)
