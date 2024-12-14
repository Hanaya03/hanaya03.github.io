import sys, re

# use regex to find the keywords and capture the variable and desired quanity
# then record the instructions until you reach the ending keyword
# execute the recorded instructions until the variable reaches the desired value
def handleForLoop(commands):
    tmp = re.search(r'pours (\w+) like ((\w+)+)',commands[0])
    # print(tmp)
    var = tmp.group(1)
    varMap[var] = summationOf(tmp.group(2))
    
    i = 2
    
    tmp = re.search(r'((?:\b\w+\b\s*)+)(and|under|underneath|over|above)\s*((\b\w+\b\s*)+)', commands[1])
    # print(tmp)
    lhs = tmp.group(1)
    operand = tmp.group(2)
    rhs = tmp.group(3)
    # print('lhs: {}, operand: {}, rhs: {}'.format(lhs, operand, rhs))
    while True:
        if 'and' in operand:
            if not (performAlgebra(lhs) == performAlgebra(rhs)):
                return
        elif 'under' in operand:
            if not (performAlgebra(lhs) < performAlgebra(rhs)):
                return
        elif 'underneath' in operand:
            if not (performAlgebra(lhs) <= performAlgebra(rhs)):
                return
        elif 'over' in operand:
            if not (performAlgebra(lhs) > performAlgebra(rhs)):
                return
        elif 'above' in operand:
            if not (performAlgebra(lhs) >= performAlgebra(rhs)):
                return
        if 'rain pours' in commands[i]:
            toExec = []
            while not 'rain ends' in commands[i]:
                toExec.append(commands[i])
                i += 1
            # print(toExec)
            # print(varMap)
            handleForLoop(toExec)
        if 'blossom' in commands[i] or 'born' in commands[i]:
            handleCreation(commands[i])
        if 'like' in commands[i]:
            handleAssignment(commands[i])
        if 'howl' in commands[i]:
            handlePrint(commands[i])
        if 'with' in commands[i]:
            toExec = []
            while 'then' != commands[i]:
                toExec.append(commands[i])
                i += 1
            handleIfStatement(toExec)
        if 'seasons pass' in commands[i]:
            toExec = []
            while 'seasons end' != commands[i]:
                toExec.append(commands[i])
                i += 1
            handleWhileLoop(toExec)
        varMap[var] = varMap[var] + 1

# use regex to find the keywords and capture the variables for the condition
# then record the instructions until you reach the ending keyword
# execute the recorded instructions until the condition is satisfied
def handleWhileLoop(commands):
    # print(commands)
    tmp = re.search(r'seasons\s+pass\s+((?:\b\w+\b\s*)+)(and|above|over|underneath|under)\s*((?:\b\w+\b\s*)+)',re.sub(r'[^a-z ]', '', commands[0].lower()))
    # print(tmp)
    lhs = tmp.group(1).strip()
    operand = tmp.group(2).strip()
    rhs = tmp.group(3).strip()
    # print('lhs:{}, operand:{}, rhs:{}'.format(lhs,operand,rhs))

    while True:
        if 'and' in operand:
            if not (performAlgebra(lhs) == performAlgebra(rhs)):
                return
        elif 'under' in operand:
            if not (performAlgebra(lhs) < performAlgebra(rhs)):
                return
        elif 'underneath' in operand:
            if not (performAlgebra(lhs) <= performAlgebra(rhs)):
                return
        elif 'over' in operand:
            if not (performAlgebra(lhs) > performAlgebra(rhs)):
                return
        elif 'above' in operand:
            if not (performAlgebra(lhs) >= performAlgebra(rhs)):
                return
        
        i = 1
        
        while i < len(commands):
            # print(commands[i])
            if 'blossom' in commands[i] or 'born' in commands[i]:
                handleCreation(commands[i])
            if 'like' in commands[i]:
                # print('assignment')
                handleAssignment(commands[i])
            if 'howl' in commands[i]:
                # print(commands[i])
                handlePrint(commands[i])
            if 'with' in commands[i]:
                toExec = []
                while 'then' != commands[i]:
                    toExec.append(commands[i])
                    i += 1
                # print(toExec)
                handleIfStatement(toExec)
            i += 1    

# helper function for math.
# iterate through a list of words and add their values up.
def summationOf(line):
    tmp = line.split()
    val = 0

    for word in tmp:
        if word in varMap:
            val += varMap[word]
        elif word in positiveWords:
            val += 1
        elif word in neutralWords:
            val += 0
        elif word in negativeWords:
            val -= 1

    return val

# use regex to recursively breakdown a string into smaller equations around higher order operands.
# returns the value of the equation
def performAlgebra(line):
    for keyword in ['spare', 'kill','breed', 'seed']:
        if keyword in line:
            tmp = line.split(keyword)
            # print(tmp)
            lhs = tmp[0]
            rhs = tmp[1]
            match keyword:
                case 'seed':
                    # print('performing {} * {}, returning {}'.format(lhs, rhs, performAlgebra(lhs) * performAlgebra(rhs)))
                    return performAlgebra(lhs) * performAlgebra(rhs)
                case 'breed':
                    return performAlgebra(lhs) * performAlgebra(rhs)
                case 'kill':
                    return performAlgebra(lhs) / performAlgebra(rhs)
                case 'spare':
                    # print('performing {} % {}, returning {}'.format(lhs, rhs, performAlgebra(lhs) % performAlgebra(rhs)))
                    return performAlgebra(lhs) % performAlgebra(rhs)
                case None:
                    return summationOf(lhs)
    tmp = re.search(r"((?:\b\w+\b\s*)+)", line)
    # print(tmp)
    return summationOf(tmp.group(1))

# use regex to break down the string where the command was detected to find the condition
# records the instructions until the ifend keyword is found
# executes the instructions only while the condtion is true
def handleIfStatement(commands):
    isTrue = False
    delimiterFound = False
    tmp = re.search(r"with\s+((?:\b\w+\b\s*)+)(and|above|over|underneath|under)\s*((?:\b\w+\b\s*)+)", re.sub(r'[^a-z ]', '', commands[0].lower()))
    lhs = tmp.group(1).strip()
    operand = tmp.group(2).strip()
    rhs = tmp.group(3).strip()
    # print('lhs: {}, operand: {}, rhs: {}'.format(lhs,operand,rhs))

    if 'and' in operand:
        isTrue = performAlgebra(lhs) == performAlgebra(rhs)
    elif 'under' in operand:
        isTrue = performAlgebra(lhs) < performAlgebra(rhs)
    elif 'underneath' in operand:
        isTrue = performAlgebra(lhs) <= performAlgebra(rhs)
    elif 'over' in operand:
        isTrue = performAlgebra(lhs) > performAlgebra(rhs)
    elif 'above' in operand:
        isTrue = performAlgebra(lhs) >= performAlgebra(rhs)

    i = 1
    while i < len(commands):
        # print(isTrue)
        delimiterFound = False
        if isTrue:
            # print(commands[i])
            if 'blossom' in commands[i] or 'born' in commands[i]:
                handleCreation(commands[i])
            if 'like' in commands[i]:
                handleAssignment(commands[i])
            if 'howl' in commands[i]:
                handlePrint(commands[i])
            if 'but' == commands[i]:
                return
            i += 1
        else:
            while (not delimiterFound):
                if 'but' == commands[i]:
                    delimiterFound = True
                i+=1
            # print('does have with?:' + commands[i])
            if 'with' in commands[i]:
                tmp = re.search(r"with\s+((?:\b\w+\b\s*)+)(and|above|over|underneath|under)\s*((?:\b\w+\b\s*)+)", re.sub(r'[^a-z ]', '', commands[i].lower()))
                # print('tmp: {}'.format(tmp))
                lhs = tmp.group(1).strip()
                operand = tmp.group(2).strip()
                rhs = tmp.group(3).strip()
                # print('lhs: {}, operand: {}, rhs: {}'.format(lhs,operand,rhs))

                if 'and' in operand:
                    # print('{}, {}'.format(performAlgebra(lhs), performAlgebra(rhs)))
                    isTrue = performAlgebra(lhs) == performAlgebra(rhs)
                    # print(isTrue)
                elif 'under' in operand:
                    isTrue = performAlgebra(lhs) < performAlgebra(rhs)
                elif 'underneath' in operand:
                    isTrue = performAlgebra(lhs) <= performAlgebra(rhs)
                elif 'over' in operand:
                    isTrue = performAlgebra(lhs) > performAlgebra(rhs)
                elif 'above' in operand:
                    isTrue = performAlgebra(lhs) >= performAlgebra(rhs)
                i+=1
            else:
                if 'blossom' in commands[i] or 'born' in commands[i]:
                    handleCreation(commands[i])
                if 'like' in commands[i]:
                    handleAssignment(commands[i])
                if 'howl' in commands[i]:
                    handlePrint(commands[i])
                if 'but' in command[i]:
                    return
                i += 1
    return

# finds the variable or string after the keyword
# prints out the appropriate value
def handlePrint(line):
    toPrint = re.search(r"\b(?:howl|howls)\b\s+(\b\w+\b|'[^']*')", re.sub(r'[^a-z \']', '', line.lower()))
    if 'howls' in line:
        if '\'' in toPrint.group(1):
            print(re.search(r"'([^']*)'", toPrint.group(1)).group(1))
        else:
            if toPrint.group(1) in varMap:
                print(varMap[toPrint.group(1)])
    else:
        if '\'' in toPrint.group(1):
            tmp = re.search(r"'([^']*)'", toPrint.group(1))
            print(tmp.group(1), end='')
        else:
            if toPrint.group(1) in varMap:
                print(varMap[toPrint.group(1)], end='')

# handles the assignment of the value into variable after the assignment keyword is found
def handleAssignment(line):
    tmp = re.sub(r'[^a-z ]', '', line.lower())
    var = re.search(r"(\b\w+\b)(?=\slike)", tmp).group(1)

    if 'breed' in line or 'seed' in line:
        values = re.search(r"like\s+((?:\b\w+\b\s*)+)\s(?:breed|seed)\s+((?:\b\w+\b\s*)+)", tmp)
        lhs = values.group(1).strip().split()
        rhs = values.group(2).strip().split()
        val1 = 0
        val2 = 0
        for word in lhs:
            if word in positiveWords:
                val1 += 1
            elif word in neutralWords:
                val1 += 0
            elif word in negativeWords:
                val1 -= 1
            elif word in varMap:
                val1 += varMap[word]
        for word in rhs:
            if word in positiveWords:
                val2 += 1
            elif word in neutralWords:
                val2 += 0
            elif word in negativeWords:
                val2 -= 1
            elif word in varMap:
                val2 += varMap[word]
        varMap[var] = val1 * val2
    else:
        values = re.search(r"like\s+((?:\b\w+\b\s*)+)", tmp).group(1).strip().split()
        val = 0
        for word in values:
            if word in positiveWords:
                val += 1
            elif word in neutralWords:
                val += 0
            elif word in negativeWords:
                val -= 1
            elif word in varMap:
                val += varMap[var]
        
        varMap[var] = val

# handles variable creation after creation keyword is found 
def handleCreation(line):
    tmp = re.search(r"(\b\w+\b)\s+(?=blossom|born)", line)
    varMap[tmp.group(1)] = 0

# ensures that the stanzas have correct number of syllables
# prints error and stops program if not
def checkSyllableCount(line):
    if countSyllablesInLine(line[0]) == 5:
        if countSyllablesInLine(line[1]) == 7:
            if countSyllablesInLine(line[2]) == 5:
                return
            else:
                print(line[2])
                print("ERROR: Final stanza should be 5 syllables long.")
                exit()
        else:
            print(line[1])
            print("ERROR: Second stanza should be 7 syllables long.")
            exit()
    else:
        print(line[0])
        print("ERROR: First stanza should be 5 syllables long.")
        exit()

# turns a string into a list of words and iterates through it to count syllables of each word and
# returns total syllable count
def countSyllablesInLine(line):
    lineSyllables = 0
    tmp = re.findall(r"\w+", line)
    for words in tmp:
        lineSyllables += countSyllablesInWord(words.lower())
    
    return lineSyllables

# syllable predictor algorithm
# creates syllable groups and counts them
# then changes syllable count based of edge cases(ending e, 'rl', multiples, etc.)
def countSyllablesInWord(word):
    syllableCount = 1
    word = re.sub(r'[^a-z]', '', word)
    vowelGroups = re.findall(r'[aeiouy]+',word)
    syllableCount = len(vowelGroups)

    if word[-1] == 'e' and syllableCount > 1:
        if word[-2] == 'l':
            syllableCount += 1
        syllableCount -= 1

    if word.endswith('ely'):
        syllableCount -= 1

    if word.endswith('es'):
        syllableCount -= 1

    if 'rl' in word:
        syllableCount += 1
    
    if word.find('wl') > 0 and ('e' in vowelGroups or 'o' in vowelGroups):
        syllableCount += 1
    
    # print('word: {}, count: {}'.format(word, syllableCount))
    return syllableCount


# ensure that the provided file is a .haiku file
if not sys.argv[1].endswith('.haiku'):
    print('ERROR: please provide a .haiku file')
    exit()

fileContents = open(sys.argv[1], 'r').read()
lines = fileContents.split("\n")

if '' in lines:
    lines.remove('')

words = []
poems = []
instructions = []
stateMap = {}
varMap = {}
positiveWords = ['warm','sun', 'bright', 'active', 'play', 'joy', 'healthy', 'lovely', 'great', 'plant', 'tall', 'beautiful']
neutralWords = ['serene', 'day', 'naught']
negativeWords = ['ugly', 'foul', 'putrid', 'rotten', 'scummy', 'sick']

# every line should have a valid poem
for line in lines:
    if line.count('...') + line.count('-') != 3:
        print('ERROR: Every stanza should be followed by a \'...\' or -' + line)
        exit()
    poems.append(re.findall(r"(.*?)(?:\.\.\.|-)", line))

for i, poem in enumerate(poems):
    if len(poem) != 3:
        print('ERROR: There must be 3 stanzas in line: {}, {}'.format(i + 1, poem))
        exit()
    checkSyllableCount(poem)

commands = fileContents.replace('\n', ' ')
numOfWith = len(re.findall(r'\bwith\b', commands.lower()))
numOfBut = len(re.findall(r'\bbut\b', commands.lower()))
numOfThen = len(re.findall(r'\bthen\b', commands.lower()))
numOfSeasons = len(re.findall(r'\bseasons pass\b',commands.lower()))
numOfSeasonsEnds = len(re.findall(r'\bseasons end\b',commands.lower()))
numOfRainPours = len(re.findall(r'\brain pours\b',commands.lower()))
numOfRainEnds = len(re.findall(r'\brain ends\b', commands.lower()))
commands = re.findall(r"(.*?)(?:\.\.\.|\.)", commands.lower().strip())

counter = 0

# pull the ending keywords out of lines that contain them
for i, command in enumerate(commands):
    commands[i] = re.sub(r'[^a-z \']', '', command)
    if 'then' in command and 'then' != command:
        tmp = command.split('then')
        if '' == tmp[1].strip():
            commands[i] = tmp[0]
            commands.insert(i + 1, 'then')
        if '' == tmp[0].strip():
            commands[i] = tmp[1]
            commands.insert(i, 'then')
    if 'but' in command and 'but' != command:
        tmp = command.split('but')
        commands[i] = tmp[0]
        commands.insert(i + 1, 'but')
        commands.insert (i + 2, tmp[1])
    if 'seasons end' in command and 'seasons end' != command:
        tmp = command.split('seasons end')
        if '' == tmp[1].strip():
            commands[i] = tmp[0]
            commands.insert(i + 1, 'seasons end')
        if '' == tmp[0].strip():
            commands[i] = tmp[1]
            commands.insert(i, 'seasons end')
    if 'rain ends' in command and 'rain ends' != command:
        tmp = command.split('rain ends')
        if '' == tmp[1].strip():
            commands[i] = tmp[0]
            commands.insert(i + 1, 'rain ends')
        if '' == tmp[0].strip():
            commands[i] = tmp[1]
            commands.insert(i, 'rain ends')

# validate the syntax of if, while, and for statements
if numOfBut>0:
    if numOfWith != numOfBut and 1 == numOfThen:
        print('ERROR: Every \'with\' or \'but\' statement should have a corresponding \'then\' keyword')
        exit()
else:
    if numOfWith != numOfThen:
        print('ERROR: Every \'with\' statement should have a corresponding \'then\' keyword')
        exit()

if numOfSeasonsEnds != numOfSeasons:
    print('ERROR: every \'seasons pass\' keyword must have a corresponding \'seasons end\' keyword')
    exit()

if numOfRainEnds != numOfRainPours:
    print('ERROR: every \'rain pours\' keyword should have a corresponding \'rain ends\' keyword')
    exit()

# iterate and execute every command in program
while counter < len(commands):
    if 'rain pours' in commands[counter]:
        toExec = []
        while not 'rain ends' in commands[counter]:
            toExec.append(commands[counter])
            counter += 1
        handleForLoop(toExec)
    if 'blossom' in commands[counter] or 'born' in commands[counter]:
        handleCreation(commands[counter])
    if 'like' in commands[counter]:
        handleAssignment(commands[counter])
    if 'howl' in commands[counter]:
        handlePrint(commands[counter])
    if 'with' in commands[counter]:
        toExec = []
        while 'then' != commands[counter]:
            toExec.append(commands[counter])
            counter += 1
        handleIfStatement(toExec)
    if 'seasons pass' in commands[counter]:
        toExec = []
        while 'seasons end' != commands[counter]:
            toExec.append(commands[counter])
            counter += 1
        handleWhileLoop(toExec)
    counter += 1