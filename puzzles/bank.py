# Sudoku puzzle bank for benchmarking.
# Format: one puzzle per line, 81 chars, 0 for empty.
# Difficulty roughly: easy (45+ clues), medium (30-35), hard (25-30), expert (~22), minimum (17 clues)

# Easy puzzles
EASY = [
    "530070000600195000098000060800060003400803001700020006060000280000419005000080079",
    "070000043040009610800634900094052000358460020000800530080070091902100005007040802",
    "200300806080070002000508003807005400500030001003400208300106000400080050609002007",
]

# Medium
MEDIUM = [
    "000260701680070090190004500820100040004602900050003028009300074040050036703018000",
    #"300000000050703008000028070700000043000000000003600600040002001000080100200090000",
    #"060000000004302600000007050000000040030000080090430000800200000003067800000900003",
    "530070000600195000098000060800060003400803001700020006060000280000419005000080079",
    "000260701680070090190004500820100040004602900050003028009300074040050036703018000"
]

# Hard
HARD = [
    "100007090030020008009600500005300900010080002600004000300000010040000007007000300",
    "000600400007000003000000000000050020005000700001000300004000800006000005000700010",
    "043080250600000000000001094900004070000608000010200003820500000000000005034090710",
]

# Expert / very hard
EXPERT = [
    "800000000003600000070090200050007000000045700000100030001000068008500010090000400",  # arto inkala "hardest"
    "000000000000003085001020000000507000004000100090000000500000073002010000000040009",
    "020000000000600003074080000000003002080040010600500000000010780500009000000000040",
]

# 17-clue minimum puzzles (from Royle's collection)
SEVENTEEN_CLUE = [
    "000700000100000000000430200000000006000509000000000418000081000002000050040000300",
    "000600400700003600000091080000000000050180003000306045004000300001020080000004007",
    "000000010400000000020000000000050407008000300001090000300400200050100000000806000",
]


def all_puzzles():
    """Return a list of (difficulty, puzzle_str) tuples."""
    bank = []
    for p in EASY:
        bank.append(("easy", p))
    with open("puzzles/puzzle_bank/easy.txt", "r") as f:
        easy_file = f.readlines()
    for line in easy_file:
        bank.append(("easy", line.split(' ')[1]))

    for p in MEDIUM:
        bank.append(("medium", p))
    with open("puzzles/puzzle_bank/medium.txt", "r") as f:
        medium_file = f.readlines()
    for line in medium_file:
        bank.append(("medium", line.split(' ')[1]))

    for p in HARD:
        bank.append(("hard", p))
    with open("puzzles/puzzle_bank/hard.txt", "r") as f:
        hard_file = f.readlines()
    for line in hard_file:
        bank.append(("hard", line.split(' ')[1]))

    for p in EXPERT:
        bank.append(("expert", p))
    with open("puzzles/puzzle_bank/expert.txt", "r") as f:
        expert_file = f.readlines()
    for line in expert_file:
        bank.append(("expert", line.split(' ')[1]))

    for p in SEVENTEEN_CLUE:
        bank.append(("17-clue", p))
    with open("puzzles/puzzle_bank/17.txt", "r") as f:
        file_17 = f.readlines()
    for line in file_17:
        bank.append(("17-clue", line))
    return bank
