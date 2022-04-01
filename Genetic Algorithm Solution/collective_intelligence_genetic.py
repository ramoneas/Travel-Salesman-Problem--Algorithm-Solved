import random
import numpy as np

infinf = f"1000" #infinity number
population = 4

GENERATIONS = 100
BEST_FITNESS_QUANTITY = int(population/2) #50% of the population
MUTATION_PERCENTAGE = 30
ROAD_LETTERS = "BCDEFG"
ROAD_ARRAY = list(ROAD_LETTERS)


parents = []
children = []
distance = {"AB": random.randint(0,100), "AC": random.randint(0,100), "AE": random.randint(0,100),
            "BD": random.randint(0,100), "CD": random.randint(0,100), "DF": random.randint(0,100),
            "EF": random.randint(0,100), "FG": random.randint(0,100)}
#Initialize
adj_matrix = [[infinf, distance["AB"], distance["AC"], infinf, distance["AE"], infinf, infinf],#A / #abcdef Index
              [distance["AB"],  infinf, infinf, distance["BD"], infinf, infinf , infinf],#B
              [distance["AC"], infinf, infinf, distance["CD"], infinf, infinf, infinf ],#C
              [infinf,  infinf, distance["CD"], infinf, infinf, distance["DF"] , infinf],#D
              [distance["AE"], infinf, infinf, infinf, infinf, distance["EF"], infinf],#E
              [infinf, infinf, infinf, distance["DF"], distance["EF"],  infinf, distance["FG"]], #F
              [infinf, infinf, infinf, infinf, infinf,  infinf, distance["FG"]]]#G

############################################################ Selection ###########################################################
#Random String function
def parents_string_generation():  
     
    # define the condition for random.sample() method  
    return "A"+"".join((random.sample(ROAD_LETTERS, len(ROAD_LETTERS))))+"A" #join is to convert the list to an string

#Parent Generation / RE-Combination function
def parents_generation(population, parents = [], children = []): 
    roads = []
    if not parents and not children:
        for i in range(population):
            roads.append(parents_string_generation())
        return roads
    else:
        return parents + children
    

#fitness function    
def fitness(selection):
    
    finest_dict = { "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6 } #Relation between matrix position with string
    finest_weight = []
    best_routes = []
    
    for i in selection:
        weight = []
        for j in range(len(i)-1): 
            weight.append(adj_matrix[finest_dict[f"{i[j]}"]][finest_dict[f"{i[j+1]}"]])#Convert letter in a position
            
        finest_weight.append(np.sum(weight, dtype=int))    
        

    best_routes = sorted(enumerate(finest_weight), key = lambda x:x[1])[:BEST_FITNESS_QUANTITY]
    
    return [selection[i[0]] for i in best_routes], best_routes
    
############################################################ Cross combination ###################################################
#Reproduction function 
def parents_reproduction(parents):
        
    children = []    
    index = 0    
    for i in range(len(parents)):  
        index += 1
        if index == len(parents):
            children.append(f"{parents[i][1:int(len(parents[i])/2)]}{parents[i-1][int(len(parents[i])/2):len(parents[i])-1]}")
        else: #Generate child without first and last character
           children.append(f"{parents[i][1:int(len(parents[i])/2)]}{parents[i+1][int(len(parents[i])/2):len(parents[i])-1]}")
    
    new_gen1, new_gen2 = cross_and_clean_children(children)
    
    return ["A" + "".join(new_gen1) + "A", "A" + "".join(new_gen2) + "A"]
                      
#Clean duplicate items in children array function
def cross_and_clean_children(child):    
    
    new_child = []
    for i in child:           
        #Check the left items      
        unique_value = check_left_items(i)        
            
        for j in range(int(len(i)/2), len(i)):   
            if unique_value and [x for x in range(int(len(i)/2)) if i[j].find(i[x])==0]: 
                #if find 0 is because is duplicated                
                i = i[:j] + unique_value.pop() + i[j+1:] #REWRITE VALUE IN i
                
        new_child.append(i)
    
    return new_child

#Check items left in the new generation
def check_left_items(i):
    unique_value = []
    for e in range(len(ROAD_ARRAY)): # Save the lefting items in an array  
        if not ROAD_ARRAY[e] in i and not ROAD_ARRAY[e] in unique_value:
            unique_value.append(ROAD_ARRAY[e])           
    
    return unique_value

############################################################# Mutation ############################################################  
def mutation(children):
    
    for i in range(len(children)):
        mutation_porcentage = random.randint(0,100) 
        swap_right_index = random.randint(1,3)
        swap_left_index = random.randint(4,6)
        child = list(children[i])
        
            
        letter_left = child[swap_left_index]
        letter_right = child[swap_right_index]
        
        
        if mutation_porcentage <= MUTATION_PERCENTAGE: # porcentage of mutation
            child[swap_right_index] = letter_left
            child[swap_left_index] = letter_right
            children.pop(i)
            children.insert(i,"".join(child))
    
        
    return children


############################################################# Main ################################################################
gen = 0    
for gen in range(GENERATIONS):
    selection = parents_generation(population, parents, children)
    parents, values = (fitness(selection)) 
    children = (parents_reproduction(parents))
    children = mutation(children)

    #CONCLUSION OF GENETIC ALGORITHM
    print("GEN: ", gen,  " SELECTION: ", selection, " BEST ROADS: ", values) 
    





   





 
        