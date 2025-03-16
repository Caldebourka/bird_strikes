#Cleaning data from "Bird_strikes.csv"
import pandas as pd
import matplotlib.pyplot as plt
#from firebase import firebase as fb
import os

strk_data = pd.read_csv("Bird_strikes.csv", encoding="ISO-8859-1")

csv_breed_lst = strk_data["WildlifeSpecies"].tolist()
breed_df = sorted(csv_breed_lst)

csv_strike_lst = strk_data["NumberStruckActual"].tolist()
strike_df = sorted(csv_strike_lst)

size_df = strk_data["WildlifeSize"].tolist()


#small sorting algorithm to ensure there aren't multiples of each bird name in breed_lst

def sortbreed(df):
    bl = []
    for x in range(len(df)):
        if bl.count(df[x]) == 0 and df[x] != "Hawks, eagles, vultures" and df[x] != "Pigeons, doves":
            bl.append(df[x])
    return bl
breed_lst = sortbreed(breed_df)

#writing a csv file to show the amount of strikes for each species

with open("temp_bird_data.csv", "w+") as f:
    f.write("Breed,Strikes\n")
    #cycles thru each breed alphabetically to add them to the csv properly
    total_strike_lst = []
    for x in range(len(breed_lst)):
        b = breed_lst[x]
        c = 0
        #totals the amount of each breed involved in a crash for each index pos
        for y in range(len(csv_strike_lst)):
            if csv_breed_lst[y] == b:
                c += csv_strike_lst[y]

        f.write(f"{breed_lst[x]}, {c}\n ")
        #total_strike_lst = total_strike_lst.append(c)
    

new_strk_data = pd.read_csv("temp_bird_data.csv", encoding="ISO-8859-1")
new_strike_df = new_strk_data["Strikes"].tolist()

#runs the lists to find the top n most common breeds
#n = input number, b = list of breeds, s = no. strikes
def topnbirds(n, b, s):    
    temp_s = s
    l = []
    bl = []
    x = 0
    while x < int(n):
        m = max(temp_s)
        ip = b[s.index(m)]
        hit_list = ["Unknown bird - small", "Unknown bird - medium", "Unknown bird - large"]
        if ip not in hit_list:
            l.append(ip)
            bl.append(m)
            x += 1
        temp_s.remove(m)
        
    return l, bl


state_df = strk_data["OriginState"].tolist()
def sortstate(df):
    sl = []
    
    for x in range(len(df)):
        if sl.count(df[x]) == 0 and not pd.isna(df[x]):
            sl.append(df[x])
    return sl

#makes a list of the total strikes in each state for use in graphs
def strikestate(s_state, us_state, strike):
    total_strikestate_lst = []
    for x in range(len(s_state)):
        b = s_state[x]
        c = 0
        #totals the amount of each breed involved in a crash for each index pos
        for y in range(len(strike)):
            if us_state[y] == b:
                c += strike[y]
        total_strikestate_lst.append(int(c))
    return total_strikestate_lst


#function to determine the top n costliest strikes
cost_lst = strk_data["Cost"].tolist()

def cost_strike(lst):
    filtered_lst = []
    
    for x in range(len(lst)):
        el = str(lst[x])
        if el != "0":
            el = el.replace(",", "")
            filtered_lst.append(int(el))
            
    sorted_lst = sorted(filtered_lst, reverse=True)
    return sorted_lst

def topn_cost(s_lst, us_lst, n):
    temp_s_lst = []
    #quick loop to remove duplicate values in the sorted list
    for x in range(len(s_lst)):
        if s_lst[x] not in temp_s_lst:
            temp_s_lst.append(s_lst[x])
        
    s_lst = temp_s_lst     
        
    for x in range(len(us_lst)):
        string = us_lst[x]
        us_lst[x] = string.replace(",", "")
    
    new_cost_lst = s_lst[:n]
    #getting the index position of the costs in new_cost_lst
    id_pos = []
    for x in range(len(new_cost_lst)):
        id_pos.append(us_lst.index(str(new_cost_lst[x])))

    
    return new_cost_lst, id_pos




def pie(lab, data, title):
    #Plot pie chart
    plt.pie(data, labels=lab)

    #Add title
    plt.title(title)
    plt.tight_layout()
    plt.savefig(f'images/{title}.png')
    plt.show()
    plt.close()
    
    
import matplotlib.pyplot as plt

def bar(x, y, xlab, ylab, title):
    plt.figure(figsize=(12, 6))  
    plt.bar(x, y)
    
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    
    plt.xticks(rotation=45, ha='right')  
    plt.ticklabel_format(style='plain', axis='y')  
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)  
    plt.tight_layout()  
    
    plt.savefig(f'images/{title}.png')
    plt.show()
    plt.close()

    
    

print('\033[3m' + """
x	x	x	x	x	x	x	x	x	x	x	x	x	x	x
x														x
x				Welcome to the Computer Science Project of 					x
x					Exam No: 258530								x
x														x
x														x
x														x
x														x
x														x
x	x	x	x	x	x	x	x	x	x	x	x	x	x	x
   
""" + '\033[3m')

    
graph = int(input('\033[3m' + """
What graph would you like then?

1. Top n most common birds
2. Number of strikes in each state
3. Top n most costly strikes
x	x	x	x	x	x	x	x	x
""" + '\033[3m'))
while graph in (1, 2, 3):
    if graph == 1:
        n = input("Show the n most common birds\n(Enter num): ")
        topnbirds = topnbirds(n, breed_lst, new_strike_df)

        #stores the 2 lists created in topnbirds() in variables
        topnbreeds_lst = topnbirds[:1]
        topnstrikes_lst = topnbirds[1]

        #topnbreeds_lst stores as a tuple therefore it needs to be stored as a list for matplotlib
        #loop iterates thru the tuple and stores it as a list
        temp_lst = []
        for t in topnbreeds_lst:
            for x in t:
                temp_lst.append(x)
        topnbreeds_lst = temp_lst
        pie(topnbreeds_lst, topnstrikes_lst, f'top_{n}_breeds')
        break
    
    elif graph == 2:
        #no of strikes in each state
        #state = list of state names sans repeats
        sortstate = sortstate(state_df)
        strikes_perstate = strikestate(sortstate, state_df, csv_strike_lst)
        bar(sortstate, strikes_perstate, "State Names", "Total Strikes Per State", "Strikes_perState")
        
        graph = 0
    
    elif graph == 3:
        #top n most costly strikes
        n = int(input("Enter a number (n):\n"))
        
        sorted_cost_lst = cost_strike(cost_lst)
        #topn_cost_lst is a tuple, contains the list and the index positions theyre located in on the unsorted list
        topn_cost_tuple = topn_cost(sorted_cost_lst, cost_lst, n)
        
        #top n costs
        topn_cost_lst = topn_cost_tuple[0]
        #index positions of each cost
        topn_id_pos = topn_cost_tuple[1]
        print("Costliest Strikes: ",  topn_cost_lst)
        
        df_airline = strk_data["Operator"].tolist()
        airline_costs = []
        for x in range(n):
            airline_costs.append(df_airline[topn_id_pos[x]])
        bar(airline_costs, topn_cost_lst, "Airlines", "Costliest Strikes", "Costliest_strikes")
        """
        #filtering -->> What aspects of each strike is the user interested in seeing?
        remark_lst = strk_data["Remarks"].tolist()
        airline_lst = strk_data["Operator"].tolist()
        
        filt_q = 0
        while filt_q not in (1,2,3):
            filt_q = int(input("""

"""))
        #with open("readableStrikeData(from the top n costliest strikes)", "w+") as f:
        def remark(topn_id_pos, remark_lst):
            remarks = []
            for x in range(len(topn_id_pos)):
                remarks.append(remark_lst[topn_id_pos[x]])
                #remarks is a list of the remarks in the correct order
            return remarks
        
        def airline(topn_id_pos, airline_lst):
            airlines =[]
            for x in range(len(topn_id_pos)):
                airlines.append(airline_lst[topn_id_pos[x]])
                #airlines is a list of the airlines in the correct order
            return airlines
        
        def breed(topn_id_pos, csv_breed_lst):
            breeds =[]
            for x in range(len(topn_id_pos)):
                breeds.append(csv_breed_lst[topn_id_pos[x]])
                #breeds is a list of the airlines in the correct order
            return breeds
        
        funct_lst = [remark(topn_id_pos, remark_lst), airline(topn_id_pos, airline_lst), breed(topn_id_pos, csv_breed_lst)]        
        funct_titles = ["Cost: ", "Remark: ", "Airline: ", "Breed: "]
        #with open("sdfbvskbs.txt", "w+") as f:
        for x in funct_lst[:filt_q]:
            #f.write(str(x) + "\n")
            data_lst = x
            for y in data_lst:
         """       #print(y)
                

        
#break
#graph = 0
                
                
            
            
"""         
    elif gorb == 2:
        n = int(input("Show the n most common birds\n(Enter num): "))
        fb_con = fb.FirebaseApplication("https://birds-2b89b-default-rtdb.europe-west1.firebasedatabase.app/", None)
        topnbirds = topnbirds(n, breed_lst, new_strike_df)

        #stores the 2 lists created in topnbirds() in variables
        topnbreeds_lst = topnbirds[:1]
        topnstrikes_lst = topnbirds[1]

        #topnbreeds_lst stores as a tuple therefore it needs to be stored as a list for matplotlib
        #loop iterates thru the tuple and stores it as a list
        temp_lst = []
        for t in topnbreeds_lst:
            for x in t:
                temp_lst.append(x)
        topnbreeds_lst = temp_lst
        for x in range(n):
            fb_con.post("/Breeds/",topnbreeds_lst[x]) 
        print("CROSS OVER TO HTML ARTIFACT")
        
        #ask for a dead input to allow the program to continue when the user comes back after bird maker
        fbread = input("When you have created your bird, return to this page\nHit enter if ready to resume\n\n")
        #fb_data takes in the firebase data in dictionary format
        fb_data = fb_con.get("/userBird", None)
        #creates a sub-dictionary containing the child nodes and grandchild node
        user_bird_dict = {}
        user_bird_deets = []
        for x, y in fb_data.items():
            birddict = y
            #loops thru sub-dictionary and appends each value to a list without their keys
            for i, c in birddict.items():
                user_bird_deets.append(c)
                #user_bird_deets contains just the values needed for statistics      
        
        """
"""
        Start of the statistics section with the bird maker
        - Working iteration done (only works with 1 bird from firebase)
        -future plans: make a choice for what bird's chance is displayed 
        
     
#fwd counted (doesn't work with the list indexxing)
#removes unknown values to ensure an accurate total
        for x in range(len(breed_df)):
            if breed_df[x] == "Unknown bird - small" or breed_df[x] == "Unknown bird - medium" or breed_df[x] == "Unknown bird - large":
                breed_df.remove(breed_df[x])
        print(len(breed_df))

        #removes unknown values to ensure an accurate total
        for x in range(len(breed_df) - 1, -1, -1):
            if breed_df[x] == "Unknown bird - small" or \
               breed_df[x] == "Unknown bird - medium" or \
               breed_df[x] == "Unknown bird - large":
                breed_df.pop(x)

                
        #Count no of appearances of the chosen breed & size value in the total lists
        print("x	x	x	x	x	x	x	x	x	x")
        chances_lst = []
        names_lst = []
        for y in range(int(len(user_bird_deets)/3)):
            breed_count = 0
            size_count = 0
            #counts the appearances for each bird (each bird's data takes up 3 index positions hence the y*3s)
            for x in range(len(breed_df)):
                if breed_df[x] == user_bird_deets[y * 3]:
                    breed_count += 1
                if size_df[x] == user_bird_deets[(y * 3) + 2]:
                    size_count += 1
                    
            #chance that the breed will be in a strike = no of appearances of the value in question/total no of all breeds
            #chance that the size will be in a strike = no of appearances of the value in question/total no of sizes
            ch_breed_n_size = round((100 *(breed_count / len(breed_df)) * (size_count / len(size_df))), 5)
            print(f"There is a {ch_breed_n_size}% chance that {user_bird_deets[(y * 3) + 1]} will be in a strike\n")
            
            chances_lst.append(ch_breed_n_size)
            names_lst.append(user_bird_deets[(y * 3) + 1])
            
        #graphing this user inputted bird data
        userBird_graph = input("Do You want to see the values on a graph?\n(input: y or n): ")
        if userBird_graph == "y":
            pie(names_lst, chances_lst, "chance of each bird being in a strike relative to each other")
        elif userBird_graph == "n":
            print("")
        gorb == 0
        

    else:
        print("invalid input")
    """

