# Miau6502-Compiler [DISCONTINUED]
## Check Out The New Super Mega Version (Miau65i)[https://github.com/Bastian1110/Miau65i]
A very primitive "Compiler", with the idea of compiling programs for Ben Eater's 6502 computer.


<p float="left">
  <img src="https://github.com/Bastian1110/Miau6502-Compiler/blob/master/Imgs/Example1.png" width=40% />
  <img src="https://github.com/Bastian1110/Miau6502-Compiler/blob/master/Imgs/Example2.png" width=40% />
</p>

## History

After completing Ben Eater's tutorials on the 6502 processor, I really wanted to create my own programs, for a while, assembler was enough to do several experiments, but I think that although it allows you to understand 100% your programs,but it is not entirely practical. That's why I set out to create my own "programming language," which had the basics to make programs for Ben's computer.





### Features
- 16-bit variables (unsigned int)
- Print function for LCD Display
- Arithmetic operations (for now only addition and subtraction)
- If and Else Statements
- "Library" with the code of [Ben Eater's videos](https://youtu.be/v3-a-zqKfgA)

### Future Features
- Support to make jumps in the program (go to)
- Negative Numbers
- Boolean Values
- Characters and Strings
- Print function for strings
- More comparator (now only <)

## Installation
_Disclaimer : This project was developed on OSX, so for Windows it may change a bit_

1. Download the [VASM assembler](http://www.compilers.de/vasm.html) bin corresponding to your operating system (Many thanks to [Dr. Volker Barthelmann's](http://www.compilers.de/home_eng.html))
2. Clone this repository on your computer

```
git clone https://github.com/Bastian1110/Miau6502-Compiler.git 
```
3. Move into the cloned repo and create a directory called _vasm_

```
cd <Path to the repo>
mkdir vasm
```
4. Move _vasm6502_oldstyle_ and _vobdump_ to the direcotry you just created

```
mv <Path to vasm files> <Path to vasm directory in the cloned repo>
```

5. Everything should be cool, done! :D

## Usage 

1. Create a file with the extension _.miau_ and follow the language syntax
2. Make sure your file is in the same directory as the repository
3. In the terminal, put the following command :

```
python3 Miau.py [-OPTION] <The name of your file (without .miau)>
```
4. Replace [OPTION] depending on what you want

```
-A : Create a file with your code in assembler(.s)
-C : Compile your program so that you can put it in your ROM (.out)
-AC : Create the assembler version of your code(.s) and compile for your ROM (.out)
```

5. Be happy!  

## Creating a Program

#### Assigning a variable
By default, a variable is a number, you can incializrr of three commands: equaling an integer, equaling another variable and equaling an operation.
```
a = 5 
b = a
c = a + b
c = a - 5
```

#### Printing
To print a variable, use the keyword _print_ and the name of the variable you want to print, it should be clarified that for this, the first line of the program must include the "library" of the display.

```
include Display!
a = 69
print a 
b = 351
print b
a = a + b
print a
```
#### If & Else
You can use a _if_ by making a comparison (> only), as in C++, you will have to put the code that runs in brac brackets {}. It is **not** obligatory that there is a _else_ for an _if_, but there **must** always be an _if_ for a _else_.
```
include Display!
a = 69
b = 19
c = a - b
if ( c < 50) {
  print a
}
else {
  print b
}
```

## End 
I know it's not very useful, but I think with a little more work it can become useful for Ben Eater video enthusiasts, we could add ways to control the input chip!




## Dedications and Special Thanks to :
This weird thing I did I dedicate to my girlfriend Harumi, since she encouraged me and inspired me to go ahead with the construction of the computer, since at some point I came to think that it was not worth it, she paid attention to my bizarre (and a little useless) creations even though I think no one cared. Harumi I looove you.

68747470733a2f2f796f7574752e62652f4152635a70596c78694e73 <- Song

After the super drama I did up there, I also thank Ben Ester for his videos, from which I have learned a lot and make me more passionate about computing.
