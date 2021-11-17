from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
sentence_0 = And(AKnight, AKnave) # => Initial knowledge added based on what A said (on top of the rule of the game)
knowledge0 = And(

############################ REASONING Version Long ###################################################################
    # Knowledge Base based on the game rule
    #Or(AKnight, AKnave), # A can either be only a Knight or a Knave
    #Not(And(AKnight, AKnave)), # Since A can only be a Knight or a Knave, then A can't be both at a time!
    
    # Knowledge Base based on what A said
    #Implication(Not(AKnight), Not(sentence_0)), # If A is not a Knight, then sentence_0 will be a lie
    #Implication(AKnight, sentence_0) # If A is a Knight, then sentence_0 will be True. But its against the game rule! So line 24 will be True!

########################################################################################################################
########################### Reasoning Version Short ####################################################################
    # Knowledge Base based on the game rule
    Biconditional(AKnight, Not(AKnave)), # A is a Knight if and only if A is not A knave => Game Rule!

    # Knowledge Base based on what A said
    # A Knight never lies! So if A is a Knight, then the sentence_0 will be True. But since the basic rule is A and B can only be of a one class,
    # then the sentence_0 is a lie (False), hence A is not a Knight either (False)
    Biconditional(AKnight, sentence_0)

)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
sentence_1 = And(AKnave, BKnave) # => Initial knowledge added based on what A said (on top of the rule of the game)
knowledge1 = And(

############################ REASONING Version Long ###################################################################
    # Knowledge Base based on the game rule
    #Or(AKnight, AKnave), # A can either be only a Knight or a Knave
    #Or(BKnight, BKnave), # B can either be only a Knight or a Knave
    #Not(And(AKnight, AKnave)), # Since A can only be a Knight or a Knave, then A can't be both at a time!
    #Not(And(BKnight, BKnave)), # Since B can only be a Knight or a Knave, then B can't be both at a time!

    # # Knowledge Base based on what A said
    #Implication(Not(AKnight), Not(sentence_1)), # If A is not a Knight, then the sentence_1 must be a lie!
    #Implication(AKnight, sentence_1) # If A is a Knight, then a knight will never lie and the sentence_1 must be True! But since sentence_1 against the rule (False), then A being a Knight is also a lie (False)!

########################################################################################################################
########################### Reasoning Version Short ####################################################################
    # Knowledge Base based on the game rule
    Biconditional(AKnight, Not(AKnave)), # A is a Knight if and only if A is not a Knave => The sentence_1 will be True
    Biconditional(BKnight, Not(BKnave)), # B is also a Knight if and only if B is not a Knave

    # Knowledge Base based on what A said
    # As a Knight never tells lies, A will be proven a Knight, if and only if sentence_1 is True! But because sentence_1 is against the rule of game, then its a False, hence A is not a Knight! 
    Biconditional(AKnight, sentence_1)
)

# Puzzle 2
# A says "We are the same kind."
sentence_2_A = Or(And(AKnight, BKnight), And(AKnave, BKnave))

# B says "We are of different kinds."
sentence_2_B = Or(And(AKnight, BKnave), And(AKnave, BKnight)) 
knowledge2 = And(
############################ REASONING Version Long ###################################################################
    # Knowledge Base based on the game rule
    #Or(AKnight, AKnave), # A can either be only a Knightor a Knave
    #Or(BKnight, BKnave), # B can either be only a Knight or a Knave
    #Not(And(AKnight, AKnave)), # Since A can only be a Knave or a Knight, then A can't be both at a time!
    #Not(And(BKnight, BKnave)), # Since B can only be a Knave or a Knight, then B can't be both at a time!

    # Knowledge Base based on what A and B said
    #Implication(AKnight, sentence_2_A), # if A is a Knight then sentence_2_A must be True
    #Implication(AKnave, Not(sentence_2_A)), # If A is a Knave (lier), then sentence_2_A must be False
    #Implication(BKnight, sentence_2_B), # If B is the Knight, then sentence_2_B must be True
    #Implication(BKnave, Not(sentence_2_B)), # if B is the Knave, then sentence_2_B must be False

########################################################################################################################
########################### Reasoning Version Short ####################################################################
    # Knowledge Base based on the game rule
    Biconditional(AKnight, Not(AKnave)), # A is a Knight if and only if A is not a Knave => The sentence_1 will be True
    Biconditional(BKnight, Not(BKnave)), # B is also a Knight if and only if B is not a Knave

    # Knowledge Base based on what A and B said
    Biconditional(AKnight, sentence_2_A), # A can only be the Knight, if and only if sentence_2_A is True, otherwise (False) A is the Knave
    Biconditional(BKnight, sentence_2_B), # B can only be the Knight, if and only if sentence_2_B is True, otherwise (False) B is the KNave
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
sentence_3_A = Or(AKnight, AKnave)

# B says "A said 'I am a knave'."
# B says "C is a knave."
sentence_3_B = And(AKnave, CKnave)

# C says "A is a knight."
sentence_3_C = AKnight

knowledge3 = And(
########################### REASONING Version Long ###################################################################
    # Knowledge Base based on the game rule
    #Or(AKnight, AKnave),
    #Or(BKnight, BKnave), # ===>  A, B, C is either a Knight or a Knave
    #Or(CKnight, CKnave),
    #Not(And(AKnight, AKnave)),
    #Not(And(BKnight, BKnave)), # ===> A, B, C can't be both classes at the same time! 
    #Not(And(CKnight, CKnave)),

    # Knowledge Base based on what A, B, and C said
    #Implication(AKnight, And(BKnave, CKnight)), # If A is a Knight, then most probably A said "I am a Knight"
    #Implication(AKnave, And(BKnight, Not(sentence_3_A))), # If A is the Knave, then B is the Knight cause B told the turth about A said that A is a Knave which means A lied to say that A is either a Knight or a Knave.
    #Implication(BKnight, sentence_3_B), # If B is the Knight, then A and B must be Knaves! Otherwise B is the Knave!
    #Implication(BKnave, And(AKnight, Not(sentence_3_B))), # If so, then sentence_3_B is a lie. This confirms that B is the Knave!
    #Implication(CKnight, And(BKnave, sentence_3_C)), # If C is a Knight, then A must be a Knight since he told that A is a Knight and a Knight never lies
    #Implication(CKnave, And(BKnight, Not(sentence_3_C))) # If C is a Knave, then A must be a Knave too and in this case B must be the Knight since B told A and C are the Knaves

########################################################################################################################
########################### Reasoning Version Short ####################################################################
    # Knowledge Base based on the game rule
    Biconditional(AKnight, Not(AKnave)), # A is a Knight if and only if A is not a Knave
    Biconditional(BKnight, Not(BKnave)), # B is also a Knight if and only if B is not a Knave
    Biconditional(CKnight, Not(CKnave)), # C is also a Knight if and only if C is not a Knave

    # Knowledge Base based on what A, B, and C said
    Biconditional(AKnight, sentence_3_A), # A can only be the Knight, if and only if sentence_3_A is True which is A can be either a Knight or a Knave, otherwise (False) A is the Knave
    Biconditional(BKnight, sentence_3_B), # B can only be the Knight, if and only if sentence_3_B is True which is both A and C are Knaves, otherwise (False) B lied and is the Knave
    Biconditional(CKnight, sentence_3_C) # C can only be the Knight, if and only if sentence_3_C is True which is A is a Knight, otherwise (False) C is the Knave
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"\n    {symbol}\n")


if __name__ == "__main__":
    main()
