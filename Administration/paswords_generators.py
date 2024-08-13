from random import sample,randint
def generateur_mdp():    
    password = "@##0AZERTYUI#OPQSD#F$GH@@@@$!@MWXCV!BNmlkjhgfdsqnbvpoiuytcxwreza@"
    mdp=("".join(sample(password,8)))+str(randint(100,1000))
    mdp_genere=""
    for k in mdp.split():
        mdp_genere+=k
    return mdp_genere