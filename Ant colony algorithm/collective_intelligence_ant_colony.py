import numpy as np
import math

infinf = f"1000" #infinity number

number_ants = 8
ITERATIONS = 100
ALPHA = 1 #EXPONENT OF PHEROMONE
BETA = 1 #EXPONENT OF DISTANCE
DECAY = 0.6 #RATE IT WHICH PHEROMONE DECAYS 

adj_matrix = [[infinf, 3, 3, 5, 2], 
             [3, infinf, 1, 7, infinf], 
             [3, 1, infinf, infinf, 3], 
             [5, 7, infinf, infinf, 2], 
             [2, infinf, 3, 2, infinf]]


pheromone_matrix = [[1, 1, 1, 1, 1],#A / #abcdef Index
                    [1, 1, 1, 1, 1],#B
                    [1, 1, 1, 1, 1],#C
                    [1, 1, 1, 1, 1],#D
                    [1, 1, 1, 1, 1]]#E

#get routes     
def get_ant_road(adj_matrix):
    finest_dict = { "0": "A", "1": "B", "2": "C", "3": "D", "4": "E"} #Relation between matrix position with string
    ant_route = []
    ant_route.append("A")
    index_matrix = 0
    
    for i in range(0,len(adj_matrix) - 1):
        possible_paths_index = []
        possible_paths_distance = []
        paths_probabilistic_weights = []
        probabilities_prob = []
        ant_route_index = []
        
        idx = 0    
        for row in adj_matrix[index_matrix]:                   
            if row != infinf and finest_dict[f"{idx}"] not in ant_route:
                possible_paths_index.append(idx)                
                possible_paths_distance.append(row)                
            idx +=1        
        
        for index in possible_paths_index:
            paths_probabilistic_weights.append(round(math.pow(pheromone_matrix[index_matrix][index], ALPHA) * math.pow((1/int(adj_matrix[index_matrix][index])), BETA), 3))
            max_weight = np.sum(paths_probabilistic_weights)    

        for probability in paths_probabilistic_weights:
            probabilities_prob.append(probability/max_weight)
        
        
        random_path_str = np.random.choice(possible_paths_index, p=probabilities_prob)           
        ant_route_index.append(random_path_str)            
        ant_route.append(finest_dict[f"{random_path_str}"])       
        index_matrix = random_path_str
                    
        if index_matrix == len(adj_matrix):
            break        
        
    return "".join(ant_route) + "A"
        
#distance function    
def get_distance(selection):    
    finest_dict = { "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6 } #Relation between matrix position with string
    finest_weight = []
    
    for i in selection:
        weight = []
        for j in range(len(i)-1): 
            weight.append(adj_matrix[finest_dict[f"{i[j]}"]][finest_dict[f"{i[j+1]}"]])#Convert letter in a position
            
        finest_weight.append(np.sum(weight, dtype=int))    
    
    return finest_weight    

#update pheromone function    
def update_pheromone(selection, distances):    
    finest_dict = { "A": 0, "B": 1, "C": 2, "D": 3, "E": 4 } #Relation between matrix position with string     
    
    idx = 0
    for i in selection:
        for j in range(len(i)-1):   
            pheromone_matrix[finest_dict[f"{i[j]}"]][finest_dict[f"{i[j+1]}"]] += 1/distances[idx] 
            pheromone_matrix[finest_dict[f"{i[j+1]}"]][finest_dict[f"{i[j]}"]] += 1/distances[idx]  
        idx += 1    
           
           
n_iter = 0
for iter in range(ITERATIONS):
    ant_list = []
    values = []
    n_iter += 1    
    
    for ants in range(number_ants):
        route = get_ant_road(adj_matrix)        
        ant_list.append(route)
        
    values = get_distance(ant_list)    
    
    #DECOY Function
    array_list = np.array(pheromone_matrix)
    pheromone_matrix = (array_list * DECAY).tolist()  
    
    update_pheromone(ant_list, values) #UPDATE PHEROMONES  
    ######################################################################  
    
    print("\nIteracion: " , n_iter , ant_list, "Pesos: " , values)  
 
    

    





   





 
        