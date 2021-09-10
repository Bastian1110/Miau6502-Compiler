import os 
import sys

option = sys.argv[1]
catfile = sys.argv[2]
if(not os.path.exists(catfile+'.miau')):
    print('Error : Miau file does not exist')
    exit()
code = open(catfile+'.miau',"r")
codeLines = code.read()
codeLines = codeLines.split('\n')
code.close()

def separateCode(line):
    banned = ['',' ','(',')']
    newLine = []
    word = ''
    last = len(line) - 1
    x = 0
    for i in line:
        if(i not in banned):
            word = word + i
        else:
            newLine.append(word)
            word = ''
        if(x == last):
            newLine.append(i)
        x = x + 1
    return newLine



compareSym = ['<','>','<=','>=','==','!=']
pureCode = []
for i in codeLines:
    compare = any(check in compareSym for check in i)
    if (compare):
        line = separateCode(i)
    else:
        line = i.split(' ')
        while '' in line:
            blank = line.index('')
            line.pop(blank)
    if line:
        pureCode.append(line)

if(pureCode[0][1] == 'Display!'):
    libary = open('Template.s',"r")
    assemblyCode = libary.read()
    assemblyCode = assemblyCode.split('\n')
    libary.close()
    vaiablePointer = 14 
else:
    assemblyCode = ["  .org $8000","reset:","loop:","  jmp loop"," ","  .org $fffc","  .word reset","  .word $0000"]
    vaiablePointer = 0

variableAddrs = 0x204
variableList = {}
labelList = {}
labelCaunter = 0


def variableDeclaration(line):
    global assemblyCode, variableAddrs, variableList, vaiablePointer
    symbols = ['+','-','*','/']
    variableName = line[0]
    declaration = line
    declaration.pop(0)
    declaration.pop(0)
    out = not(any(check in symbols for check in declaration))
    if(variableName not in variableList):
        variableList[variableName] = variableAddrs
        #assemblyCode.insert(0,variableName + ' = $'+hex(variableAddrs)[2:])
        variableAddrs = variableAddrs + 2
    location = assemblyCode.index('reset:') + vaiablePointer
    if(out):
        direction = '  sta $'+hex(variableList[variableName])[2:]
        if(declaration[0].isdigit()):
            value = '{}{} {}{}'.format(*format(int(declaration[0]), '04x')).split()
            assemblyCode.insert(location + 1,'  lda #$'+ value[1])
            assemblyCode.insert(location + 2, direction)
            assemblyCode.insert(location + 3,'  lda #$'+ value[0])
            assemblyCode.insert(location + 4, direction + ' + 1')
            assemblyCode.insert(location + 5, ' ')
        else:
            directionV = '  lda $'+hex(variableList[declaration[0]])[2:]
            assemblyCode.insert(location + 1,directionV)
            assemblyCode.insert(location + 2, direction)
            assemblyCode.insert(location + 3,directionV+ ' + 1')
            assemblyCode.insert(location + 4, direction + ' + 1')
            assemblyCode.insert(location + 5, ' ')
        vaiablePointer = vaiablePointer + 5
    else :
        handleCalculation(declaration,location)
        assemblyCode.insert(location + 7, '  sty $'+hex(variableList[variableName])[2:])
        assemblyCode.insert(location + 8, '  sta $'+hex(variableList[variableName])[2:] + ' + 1')
        assemblyCode.insert(location + 9, ' ')
        vaiablePointer = vaiablePointer + 9

    assemblyCode[location + 1] = assemblyCode[location + 1] + '  ; '+ variableName + '='+ ''.join(declaration)


def handleCalculation(line,location):
    global assemblyCode, variableAddrs, variableList, vaiablePointer
    first = hex(variableList[line[0]])[2:]
    second = hex(variableList[line[2]])[2:] 
    if('+' in line):
        if((line[0].isalpha())and(line[2].isalpha())):
            assemblyCode.insert(location + 1, '  ')
            assemblyCode.insert(location + 2, '  lda $'+first)
            assemblyCode.insert(location + 3, '  adc $'+second)
            assemblyCode.insert(location + 4,'  tay')
            assemblyCode.insert(location + 5, '  lda $'+first + ' + 1')
            assemblyCode.insert(location + 6, '  adc $'+second + ' + 1')
        elif((line[0].isdigit())and(line[2].isalpha())):
            value = '{}{} {}{}'.format(*format(int(line[0]), '04x')).split()
            assemblyCode.insert(location + 1, '  ')
            assemblyCode.insert(location + 2, '  lda #$'+value[1])
            assemblyCode.insert(location + 3, '  adc $'+second)
            assemblyCode.insert(location + 4,'  tay')
            assemblyCode.insert(location + 5, '  lda #$'+value[0])
            assemblyCode.insert(location + 6, '  adc $'+second + ' + 1')
        elif((line[0].isalpha())and(line[2].isdigit())):
            value = '{}{} {}{}'.format(*format(int(line[0]), '04x')).split()
            assemblyCode.insert(location + 1, '  ')
            assemblyCode.insert(location + 2, '  lda $'+first)
            assemblyCode.insert(location + 3, '  adc #$'+value[1])
            assemblyCode.insert(location + 4,'  tay')
            assemblyCode.insert(location + 5, '  lda $'+first + ' + 1')
            assemblyCode.insert(location + 6, '  adc #$'+value[0])
    elif('-' in line):
        if((line[0].isalpha())and(line[2].isalpha())):
            assemblyCode.insert(location + 1, '  sec')
            assemblyCode.insert(location + 2, '  lda $'+first)
            assemblyCode.insert(location + 3, '  sbc $'+second)
            assemblyCode.insert(location + 4,'  tay')
            assemblyCode.insert(location + 5, '  lda $'+first + ' + 1')
            assemblyCode.insert(location + 6, '  sbc $'+second + ' + 1')
        elif((line[0].isdigit())and(line[2].isalpha())):
            value = '{}{} {}{}'.format(*format(int(line[0]), '04x')).split()
            assemblyCode.insert(location + 1, '  sec')
            assemblyCode.insert(location + 2, '  lda #$'+value[1])
            assemblyCode.insert(location + 3, '  sbc $'+second)
            assemblyCode.insert(location + 4,'  tay')
            assemblyCode.insert(location + 5, '  lda #$'+value[0])
            assemblyCode.insert(location + 6, '  sbc $'+second + ' + 1')
        elif((line[0].isalpha())and(line[2].isdigit())):
            value = '{}{} {}{}'.format(*format(int(line[0]), '04x')).split()
            assemblyCode.insert(location + 1, '  sec')
            assemblyCode.insert(location + 2, '  lda $'+first)
            assemblyCode.insert(location + 3, '  sbc #$'+value[1])
            assemblyCode.insert(location + 4,'  tay')
            assemblyCode.insert(location + 5, '  lda $'+first + ' + 1')
            assemblyCode.insert(location + 6, '  sbc #$'+value[0])
        
def handleIf(line,elseflag):
    global assemblyCode, variableAddrs, variableList, vaiablePointer, declarationList, labelCaunter
    location = assemblyCode.index('reset:') + vaiablePointer
    if (not elseflag):
        labelNameBegin = 'IF' + str(labelCaunter) + ':'
        labelNameEnd = 'END'+ str(labelCaunter) + ':'
        labelCaunter = labelCaunter + 1
        comparation = line
        comparation.pop(0)
        comparation.pop(-1)
        if(comparation[1] == '>'):
            if((line[0].isalpha())and(line[2].isalpha())):
                assemblyCode.insert(location + 1,'  lda $'+hex(variableList[comparation[0]])[2:])
                assemblyCode.insert(location + 2,'  cmp $'+hex(variableList[comparation[2]])[2:])
            elif((line[0].isdigit())and(line[2].isalpha())):
                assemblyCode.insert(location + 1,'  lda #'+comparation[0])
                assemblyCode.insert(location + 2,'  cmp $'+hex(variableList[comparation[2]])[2:])
            elif((line[0].isalpha())and(line[2].isdigit())):
                assemblyCode.insert(location + 1,'  lda $'+hex(variableList[comparation[0]])[2:])
                assemblyCode.insert(location + 2,'  cmp #'+comparation[2])

            assemblyCode.insert(location + 3,'  bmi ' + labelNameEnd)
            assemblyCode.insert(location + 4, ' ')
            assemblyCode.insert(location + 5,labelNameBegin)
            assemblyCode.insert(location + 6, ' ')
            assemblyCode.insert(location+ 7, labelNameEnd )
            assemblyCode.insert(location + 8, '  nop')
            vaiablePointer = vaiablePointer + 8
    else:
        labelNameBegin = 'IF' + str(labelCaunter) + ':'
        labeNambeMiddle = 'ELSE' + str(labelCaunter) + ':'
        labelNameEnd = 'END'+ str(labelCaunter) + ':'
        labelCaunter = labelCaunter + 1
        labelCaunter = labelCaunter + 1
        comparation = line
        comparation.pop(0)
        comparation.pop(-1)
        if(comparation[1] == '>'):
            if((line[0].isalpha())and(line[2].isalpha())):
                assemblyCode.insert(location + 1,'  lda $'+hex(variableList[comparation[0]])[2:])
                assemblyCode.insert(location + 2,'  cmp $'+hex(variableList[comparation[2]])[2:])
            elif((line[0].isdigit())and(line[2].isalpha())):
                assemblyCode.insert(location + 1,'  lda #'+comparation[0])
                assemblyCode.insert(location + 2,'  cmp $'+hex(variableList[comparation[2]])[2:])
            elif((line[0].isalpha())and(line[2].isdigit())):
                assemblyCode.insert(location + 1,'  lda $'+hex(variableList[comparation[0]])[2:])
                assemblyCode.insert(location + 2,'  cmp #'+comparation[2])
            assemblyCode.insert(location + 3,'  bmi ' + labeNambeMiddle)
            assemblyCode.insert(location + 4, ' ')
            assemblyCode.insert(location + 5,labelNameBegin)
            assemblyCode.insert(location + 6, '  jmp '+labelNameEnd)
            assemblyCode.insert(location + 7, ' ')
            assemblyCode.insert(location+ 8, labeNambeMiddle)
            assemblyCode.insert(location + 9, ' ')
            assemblyCode.insert(location+ 10, labelNameEnd )
            assemblyCode.insert(location + 11, '  nop')
            vaiablePointer = vaiablePointer + 11    
        




def handlePrint(line):
    global assemblyCode, variableAddrs, variableList, vaiablePointer, declarationList, labelCaunter
    location = assemblyCode.index('reset:') + vaiablePointer
    assemblyCode.insert(location + 1, '  lda $'+hex(variableList[line[1]])[2:])
    assemblyCode.insert(location + 2, '  sta value')
    assemblyCode.insert(location + 3, '  lda $'+hex(variableList[line[1]])[2:]+' + 1')
    assemblyCode.insert(location + 4, '  sta value + 1')
    assemblyCode.insert(location + 5, '  jsr printNumber')
    assemblyCode.insert(location + 6, '  jsr delay')
    assemblyCode.insert(location + 7, '  ')
    assemblyCode[location + 1] = assemblyCode[location + 1] + '  ; print ' + line[1]
    vaiablePointer = vaiablePointer + 7
                

conditionFlag = False
programSateTrack = []
for i in pureCode:
    if('{' in i):
        conditionFlag = True
    elif('}' in i):
        conditionFlag = False
    programSateTrack.append(conditionFlag)

x = 0
ifInfo = [0,0]
elseInfo = [0,0]
elseFlag = False
for i in pureCode:
    state = programSateTrack[x]
    x = x + 1
    if(state):
        if('{' in i):
            if('if' in i):
                lineS = x - 1
                while(programSateTrack[lineS] != False):
                    lineS = lineS + 1
                if('else' in pureCode[lineS + 1]):
                    handleIf(i,True)
                    ifInfo[0] = x
                    ifInfo[1] = lineS - 1
                    elseInfo[0] = lineS + 2
                    elseEnd = lineS + 1
                    while(programSateTrack[elseEnd] != False):
                        elseEnd = elseEnd + 1
                    elseInfo[1] = elseEnd - 1
                    elseFlag = True
                else:
                    handleIf(i,False)
                    ifInfo[0] = x
                    ifInfo[1] = lineS - 1
                    elseFlag = False
        if(elseFlag):
            if('print' in i and x - 1 in list(range(ifInfo[0],ifInfo[1]+1))):
                vaiablePointer = vaiablePointer - 6
                handlePrint(i)
                vaiablePointer = vaiablePointer + 6
            elif('print' not in i and x - 1 in list(range(ifInfo[0],ifInfo[1]+1))):
                vaiablePointer = vaiablePointer - 6
                variableDeclaration(i)
                vaiablePointer = vaiablePointer + 6
            elif('print' in i and x - 1 in list(range(elseInfo[0],elseInfo[1]+1))):
                vaiablePointer = vaiablePointer - 2
                handlePrint(i)
                vaiablePointer = vaiablePointer + 2
            elif('print' not in i and x - 1 in list(range(elseInfo[0],elseInfo[1]+1))):
                vaiablePointer = vaiablePointer - 2
                variableDeclaration(i)
                vaiablePointer = vaiablePointer + 2
        else:
            if('print' in i and x - 1 in list(range(ifInfo[0],ifInfo[1]+1))):
                vaiablePointer = vaiablePointer - 2
                handlePrint(i)
                vaiablePointer = vaiablePointer + 2
            elif('print' not in i and x - 1 in list(range(ifInfo[0],ifInfo[1]+1))):
                vaiablePointer = vaiablePointer - 2
                variableDeclaration(i)
                vaiablePointer = vaiablePointer + 2
    else:
        if('=' in i):
            variableDeclaration(i)
        elif('print' in i):
            handlePrint(i)

def writeAssembly():
    assembly = open(catfile+'.s','x')
    for line in assemblyCode:
        assembly.write(line + '\n')
    assembly.close()


def compilee():
    os.system("./vasm/vasm6502_oldstyle -Fbin -dotdir "+catfile+".s")
    os.system('mv a.out '+catfile+'.out')
def removeAss():
    os.system("rm -r "+catfile+'.s')


if option == '-C':
    writeAssembly()
    compilee()
    removeAss()
elif option == '-A':
    writeAssembly()
elif option == '-AC':
    writeAssembly()
    compilee()