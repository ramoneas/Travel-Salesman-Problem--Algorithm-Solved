import random, re
import numpy as np

infinf = f"1000" #infinity number

population = 4
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
    road_letters = "BCDEFG" # define the specific string  
    # define the condition for random.sample() method  
    return "A"+"".join((random.sample(road_letters, len(road_letters))))+"A" #join is to convert the list to an string

#Parent Generation / RE-Combination function
def parents_generation(population, parents = [], children = []): 
    roads = []
    if not parents and not children:
        for i in range(population):
            roads.append(parents_string_generation())
        return roads
    else:
        return [parents[0] , parents[1] , children[0] , children[1]]
    
#Convert the letters of the road array to the actual road value
def get_road_value_by_letter(weight, selector):
    if selector == "AB":
        weight.append(selector.replace("AB", str(distance["AB"])))
    elif selector == "AC":
        weight.append(selector.replace("AC", str(distance["AC"])))
    elif selector == "AE":   
        weight.append(selector.replace("AE", str(distance["AE"])))
    elif selector == "BD":
        weight.append(selector.replace("BD", str(distance["BD"])))
    elif selector == "CD":
        weight.append(selector.replace("CD", str(distance["CD"])))
    elif selector == "DF":
        weight.append(selector.replace("DF", str(distance["DF"])))
    elif selector == "EF":
        weight.append(selector.replace("EF", str(distance["EF"])))
    elif selector == "FG":
        weight.append(selector.replace("FG", str(distance["FG"])))
    else:
        weight.append(re.sub('[A-Z]', infinf, selector))
        
    return weight

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
        

    pos1 = finest_weight.index(min(finest_weight))
    best_routes.append(finest_weight[pos1])
    finest_weight[pos1] = 1000000000

    pos2 = finest_weight.index(min(finest_weight))
    best_routes.append(finest_weight[pos2])
    
    return[selection[pos1], selection[pos2]], best_routes
    
############################################################ Cross combination ###################################################
#Reproduction function 
def parents_reproduction(parents):
    parent1, parent2 = parents
        
    child1 = list(f"{parent1[1:4]}{parent2[4:7]}") #Generate child without first and last character
    child2 = list(f"{parent2[1:4]}{parent1[4:7]}")
    children = [child1, child2]  
    
    new_gen1, new_gen2 = cross_and_clean_children(children)
    
    return ["A" + "".join(new_gen1) + "A", "A" + "".join(new_gen2) + "A"]
                      
#Clean duplicate items in children array function
def cross_and_clean_children(child):    
    index = 0
    for i in child:   
        #Check the left items      
        unique_value = check_left_items(i)        
            
        for j in range(3, len(i)):   
            if unique_value and i[j].find(i[0])==0 or i[j].find(i[1])==0 or i[j].find(i[2])==0: #if find 0 is because is duplicated
                #print("duplicate: ", i[j], j, i[j:], "unique: ", unique_value)                     
                i[j] = unique_value.pop(index)
    return child
#Check items left in the new generation
def check_left_items(i):
    unique_value = []
    for e in range(3): # Save the lefting items in an array  
        if not "B" in i and not "B" in unique_value:
            unique_value.append("B")                
        elif not "C" in i and not "C" in unique_value:
            unique_value.append("C")                
        elif not "D" in i and not "D" in unique_value:
            unique_value.append("D")                
        elif not "E" in i and not "E" in unique_value:
            unique_value.append("E")                
        elif not "F" in i and not "F" in unique_value:
            unique_value.append("F")                
        elif not "G" in i and not "G" in unique_value:
            unique_value.append("G")
    return unique_value

############################################################# Mutation ############################################################  
def mutation(children):
    
    
    mutation_porcentage = random.randint(0,100) 
    child_selection = random.randint(0,1) #50% of children 
    swap_right_index = random.randint(1,3)
    swap_left_index = random.randint(4,6)
    child = list(children[child_selection])
    
        
    letter_left = child[swap_left_index]
    letter_right = child[swap_right_index]
     
    
    if mutation_porcentage <= 30: #30% porcentage of mutation
        child[swap_right_index] = letter_left
        child[swap_left_index] = letter_right
        children.pop(child_selection)
        children.insert(child_selection,"".join(child))
        
    return children


############################################################# Main ################################################################
gen = 0    
for gen in range(100):
    selection = parents_generation(population, parents, children)
    parents, values = (fitness(selection)) 
    children = (parents_reproduction(parents))
    children = mutation(children)

    #CONCLUSION OF GENETIC ALGORITHM
    print("GEN: ", gen,  " SELECTION: ", selection, " BEST ROADS: ", values) 
    





   





 
        