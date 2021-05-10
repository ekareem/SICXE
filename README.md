# SICXE

[Demo](https://www.youtube.com/watch?v=tYYF0TpKkwg)

**how to run** 
  
  language: pyhton3
  
  py main.py (args) or python3 main.py (args) or python main.py (args)
  
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
![](https://imgur.com/ex76hcI.png)

  **RUN PROGRAM**

  py main.py -run -a  (assembleyfile)
  
  or
  
  py main.py -run -o (objectfile)
  
![](https://imgur.com/ITbkqFc.png)

  **DEBUGGER**
  
  py main.py -bug -a  (assembleyfile)
  
  or
  
  py main.py -bug -o (objectfile)
  
![](https://imgur.com/ibBNjiG.png)

![](https://user-images.githubusercontent.com/76535260/117469418-b4627680-af23-11eb-98d1-84c12b1e39ee.png)


