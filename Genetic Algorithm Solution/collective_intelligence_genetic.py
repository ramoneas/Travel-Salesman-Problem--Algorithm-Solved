import random, re
import numpy as np

infinf = f"1000" #infinity number

population = 4
parents = []
children = []
distance = {"AB": random.randint(0,100), "AC": random.randint(0,100), "AE": random.randint(0,100),
            "BD": random.randint(0,100), "CD": random.randint(0,100), "DF": random.randint(0,100),
            "EF": random.randint(0,100), "FG": random.randint(0,100)}

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
    
    selection_weights = []
    selection_value = []
    best_roads_value = []
    string_to_array = []
        
    
    #Convert string to list every two characters
    for select in selection:
        
        weight = []
        for j in range(0, len(selection[0]), 2): #Run from 0 to len of first index of selection and every 2 steps
            string_to_array[:0:] = select #Convert string to list
            selector = f"{string_to_array[j]}{string_to_array[j+1]}"
            
            weights = get_road_value_by_letter(weight, selector)
            selector = ""            
            string_to_array = []
        
        selection_weights.append(weights) #Save the new list
        
        
    #Sum the selection weights in the array
    for i in selection_weights:
        selection_value.append(np.sum(i, dtype=int))      
    
      
    pos1 = selection_value.index(min(selection_value)) #Get the position of the minimun value  
    best_roads_value.append(selection_value[pos1])    
    selection_value[pos1] = int(f"{infinf}{infinf}")*4 #Maximize the last position    
    pos2 = selection_value.index(min(selection_value)) #Get the position of the second minimun value  
    best_roads_value.append(selection_value[pos2])  
    
    if pos1 == pos2:# Force to send another position 
        pos2 = 1 #Works when all the values in selection are inf
    
    return [selection[pos1], selection[pos2]], best_roads_value #Return the road with min values / BEST ROADS
    
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
for gen in range(1000):
    selection = parents_generation(population, parents, children)
    parents, values = (fitness(selection)) 
    children = (parents_reproduction(parents))
    children = mutation(children)

    #CONCLUSION OF GENETIC ALGORITHM
    print("GEN: ", gen,  " SELECTION: ", selection, " BEST ROADS: ", values) 
    

#Initialize
adj_matrix = [[infinf, distance["AB"], distance["AC"], infinf, distance["AE"], infinf],#A / #abcdef Index
              [distance["AB"],  infinf, infinf, distance["BD"], infinf, infinf ],#B
              [distance["AC"], infinf, infinf, distance["CD"], infinf, infinf ],#C
              [infinf,  infinf, distance["CD"], infinf, infinf, distance["DF"] ],#D
              [distance["AE"], infinf, infinf, infinf, infinf, distance["EF"]],#E
              [infinf, infinf, infinf, distance["DF"], distance["EF"],  infinf], #F
              [infinf, infinf, infinf, infinf, infinf,  infinf, distance["FG"]]]#G



   





 
