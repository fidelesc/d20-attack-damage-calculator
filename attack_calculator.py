import random
import tkinter as tk
from tkinter import ttk

def get_enemy_ac(option, cr):
    """ Get the enemy AC by mean or median from multiple source books"""
    ac = None
    mean_ac = {
    '0': 11.7,'1/8': 12.45,'1/4': 12.17,'1/2': 12.78,'1': 13.47,'2': 13.96,
    '3': 14.33,'4': 14.47,'5': 15.06,'6': 15.33,'7': 15.78,'8': 15.3,'9': 16.4,
    '10': 16.51,'11': 16.63,'12': 16.8,'13': 16.65,'14': 17.17,'15': 17.87,
    '16': 18.44,'17': 18.67,'18': 18.5,'19': 18.5,'20': 18.14,'21': 19.18,
    '22': 19.38,'23': 19.87,'24': 20.83,'25': 20,'26': 21.4,'28': 23.5,'30': 25
    }
    
    median_ac = {
    '0': 12,'1/8': 12,'1/4': 12,'1/2': 13,'1': 13,'2': 14,'3': 14,'4': 14,
    '5': 15,'6': 15,'7': 15,'8': 15,'9': 16,'10': 17,'11': 17,'12': 17,'13': 17,
    '14': 18,'15': 18,'16': 18.5,'17': 19,'18': 18.5,'19': 18,'20': 19,'21': 19,
    '22': 19,'23': 21,'24': 20.5,'25': 20.5,'26': 22,'28': 23.5,'30': 25
    }

    if option=="Mean AC per CR":
        try:
            ac = mean_ac[cr]
        except:
            pass
    elif option=="Median AC per CR":
        try:
            ac = median_ac[cr]
        except:
            pass
    return ac

def test_attack_roll(ac, attack_bonus, condition, player):
    """Test the attack roll for a given AC and attack bonus. Accepts different attacking conditions."""
    if condition=="Normal":
        d20_roll = random.randint(1, 20)  # Roll a d20
    elif condition == "Advantage"  or condition=="Enemy paralyzed within 5 ft":
        d20_roll = max(random.randint(1, 20), random.randint(1, 20))  # Roll two d20s and take the higher result
        if player[0] == True: # Elven Accuracy
            d20_roll = max(d20_roll, random.randint(1, 20))
    elif condition == "Disadvantage":
        d20_roll = min(random.randint(1, 20), random.randint(1, 20))  # Roll two d20s and take the lower result

    if player[1]==True and d20_roll == 1:
        d20_roll = random.randint(1, 20)  # Reroll a d20 for halfing luck

    if d20_roll == 20:
        return 2  # Critical hit!
    elif condition=="Enemy paralyzed within 5 ft" and d20_roll + attack_bonus >= ac and d20_roll != 1:
        return 2 # Critical hit!
    elif d20_roll + attack_bonus >= ac:
        return 1 # Hit!
    else:
        return 0  # Critical miss or miss :(


def get_damage(attacks_per_turn, ac, attack_bonus, condition, player, num_dice, dice_size, modifier, critical_option, extra_option, ex_num_dice, ex_dice_size, ex_modifier):
    """Get the average damage rate for a given AC and attack bonus."""
    damage_count = 0
    turn = []
    total_rolls = 100000  # Roll 100,000 times to get an accurate average
    
    hit_damage = calculate_average_damage(num_dice, dice_size, modifier)
    hit_critical = calculate_average_damage(num_dice, dice_size, modifier, critical_option)
    extra_damage = calculate_average_damage(ex_num_dice, ex_dice_size, ex_modifier)
    extra_critical = calculate_average_damage(ex_num_dice, ex_dice_size, ex_modifier, critical_option)
    
    for i in range(total_rolls):
        damage_per_turn = 0
        for j in range(attacks_per_turn):
            test = test_attack_roll(ac, attack_bonus, condition, player)
            if test==1:
                if extra_option == "on hit once per turn" and damage_per_turn==0:
                    damage_count += extra_damage
                    damage_per_turn += extra_damage
                elif extra_option == "on hit":
                    damage_count += extra_damage
                    damage_per_turn += extra_damage
                damage_count += hit_damage
                damage_per_turn += hit_damage

            elif test==2:
                if extra_option == "on hit once per turn" and damage_per_turn==0:
                    damage_count += extra_critical
                    damage_per_turn += extra_critical
                elif extra_option == "on hit":
                    damage_count += extra_critical
                    damage_per_turn += extra_critical
                elif extra_option == "on critical":
                    # Damage not affected by critical
                    damage_count += extra_damage
                    damage_per_turn += extra_damage
                damage_count += hit_critical
                damage_per_turn += hit_critical


    
            turn.append(damage_per_turn)
    average_damage = damage_count / total_rolls
    average_turn = sum(turn) / len(turn)
    return average_damage, average_turn
    
def get_success_rate(ac, attack_bonus, condition, player):
    """Get the average success rate for a given AC and attack bonus. Accepts different attacking conditions"""
    success_count = 0
    total_rolls = 100000  # Roll 100,000 times to get an accurate average
    for i in range(total_rolls):
        if test_attack_roll(ac, attack_bonus, condition, player):
            success_count += 1
    return success_count / total_rolls

def calculate_average_damage(num_dice, dice_size, modifier, critical_option=None):
    """Calculate the average damage for a given attack description, with an option for critical damage."""
    # Calculate the average damage based on the dice size
    if critical_option == "Extra roll":
        average_damage = ((2*num_dice)*((dice_size + 1) / 2))+modifier
    elif critical_option == "Maximum damage":
        average_damage = ((num_dice*((dice_size + 1) / 2))+modifier)+(num_dice*dice_size)
    else:
        average_damage = (num_dice*((dice_size + 1) / 2))+modifier

    return average_damage

def get_attack_description(attack_description):
    # Parse the attack description to get the number of dice and the dice size
    num_dice, dice_size, modifier = 0, 0, 0
    parts = attack_description.split("+")
    if len(parts) > 1:
        modifier = int(parts[1])
    dice_parts = parts[0].split("d")
    if len(dice_parts) > 1:
        num_dice = int(dice_parts[0])
        dice_size = int(dice_parts[1])
        
    return num_dice, dice_size, modifier


def calculate_estimated_damage():
    """Calculate the estimated damage per turn based on the user's input."""
    
    condition = conditions_var.get()
    player = [checkbox_elven.get(), 
              checkbox_lucky.get()]
    
    ac_option = ac_option_var.get()
    if ac_option=="Input AC":
        ac = int(ac_entry.get())
    else:
        ac = get_enemy_ac(ac_option, cr_entry.get())
        
    attack_bonus = int(attack_bonus_entry.get())
    num_attacks = int(num_attacks_entry.get())
    attack_description = attack_description_entry.get()
    extra_description = extra_option_entry.get()
    extra_option = extra_option_var.get()
    
    num_dice, dice_size, modifier = get_attack_description(attack_description)
    ex_num_dice, ex_dice_size, ex_modifier = get_attack_description(extra_description)
    critical_option = critical_option_var.get()

    if ac is not None:
        success_rate = get_success_rate(ac, attack_bonus, condition, player)
        average_damage, estimated_damage = get_damage(num_attacks, 
                                                      ac, 
                                                      attack_bonus, 
                                                      condition,
                                                      player,
                                                      num_dice, 
                                                      dice_size, 
                                                      modifier, 
                                                      critical_option, 
                                                      extra_option,
                                                      ex_num_dice,
                                                      ex_dice_size,
                                                      ex_modifier)

        result_label.configure(text=f"Estimated damage per turn: {estimated_damage:.2f}")
        result_label2.configure(text=f"Attack success rate: {success_rate:.2f}")
        result_label3.configure(text=f"Enemy AC of {ac}")
    else:
        result_label3.configure(text="Enemy CR not understood")

        
if __name__ == '__main__':
        
    # Create the main window
    root = tk.Tk()
    root.title("d20 Damage Calculator")
    
    # Create the Notebook widget
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)
    
    # Create the first tab
    tab1 = tk.Frame(notebook)
    notebook.add(tab1, text="Turn Description")
    
    # Create the second tab
    tab2 = tk.Frame(notebook)
    notebook.add(tab2, text="Options")
       
    # Create the input fields  
    left_label = tk.Label(tab1, text="Player Attack")
    left_label.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
    
    num_attacks_label = tk.Label(tab1, text="Attacks per Turn:")
    num_attacks_entry = tk.Entry(tab1)
    num_attacks_label.grid(row=1, column=0, padx=5, pady=5)
    num_attacks_entry.grid(row=1, column=1, padx=5, pady=5)  
    
    attack_bonus_label = tk.Label(tab1, text="Attack Bonus:")
    attack_bonus_entry = tk.Entry(tab1)
    attack_bonus_label.grid(row=2, column=0, padx=5, pady=5)
    attack_bonus_entry.grid(row=2, column=1, padx=5, pady=5)
    
    attack_description_label = tk.Label(tab1, text="Attack Description:")
    attack_description_entry = tk.Entry(tab1)
    attack_description_label.grid(row=3, column=0, padx=5, pady=5)
    attack_description_entry.grid(row=3, column=1, padx=5, pady=5)
    
    right_label = tk.Label(tab1, text="Enemy AC or CR")
    right_label.grid(row=0, column=2, padx=5, pady=5, columnspan=2)
    
    ac_options = ["Input AC","Mean AC per CR", "Median AC per CR"]
    ac_option_var = tk.StringVar(value=ac_options[0])
    ac_option_menu = tk.OptionMenu(tab1, ac_option_var, *ac_options)
    ac_option_menu.grid(row=1, column=2, padx=5, pady=5, columnspan=2)
    # Calculate the maximum length of the options
    max_length = max(len(option) for option in ac_options)
    ac_option_menu.config(width=max_length)
    
    ac_label = tk.Label(tab1, text="Enemy AC:")
    ac_entry = tk.Entry(tab1)
    ac_label.grid(row=2, column=2, padx=5, pady=5)
    ac_entry.grid(row=2, column=3, padx=5, pady=5)
    
    cr_label = tk.Label(tab1, text="Enemy CR:")
    cr_entry = tk.Entry(tab1)
    cr_label.grid(row=3, column=2, padx=5, pady=5)
    cr_entry.grid(row=3, column=3, padx=5, pady=5)
    
    
    # Create the button to calculate the estimated damage
    calculate_button = tk.Button(tab1, text="CALCULATE", command=calculate_estimated_damage)
    calculate_button.grid(row=4, column=0, columnspan=4, padx=5, pady=5)
    
    # Create the label to display the result
    result_label = tk.Label(tab1, text="")
    result_label.grid(row=10, column=0, columnspan=5, padx=5, pady=5)
    result_label2 = tk.Label(tab1, text="")
    result_label2.grid(row=12, column=0, columnspan=5, padx=5, pady=5)
    result_label3 = tk.Label(tab1, text="")
    result_label3.grid(row=14, column=0, columnspan=5, padx=5, pady=5)
    
    ### TAB 2
        
    # Create the dropdown menu for selecting game edition
    edition_label = tk.Label(tab2, text="Attack Condition:")
    edition_label.grid(row=0, column=0, padx=5, pady=5)
    conditions_options = ["Normal", "Advantage", "Disadvantage", "Enemy paralyzed within 5 ft"]
    conditions_var = tk.StringVar(value=conditions_options[0])
    condition_menu = tk.OptionMenu(tab2, conditions_var, *conditions_options)
    condition_menu.grid(row=0, column=1, padx=5, pady=5)
    # Calculate the maximum length of the options
    max_length = max(len(option) for option in conditions_options)
    condition_menu.config(width=max_length)
    
    critical_option_label = tk.Label(tab2, text="Critical Option:")
    critical_options = ["Extra roll", "Maximum damage"]
    critical_option_var = tk.StringVar(value=critical_options[0])
    critical_option_menu = tk.OptionMenu(tab2, critical_option_var, *critical_options)
    critical_option_label.grid(row=1, column=0, padx=5, pady=5)
    critical_option_menu.grid(row=1, column=1, padx=5, pady=5)
    # Calculate the maximum length of the options
    max_length = max(len(option) for option in critical_options)
    critical_option_menu.config(width=max_length)
        
    extra_damage_label = tk.Label(tab2, text="Extra damage:")
    extra_damage_label.grid(row=2, column=0, padx=5, pady=5)
    
    extra_options = ["on hit","on hit once per turn", "on critical"]
    extra_option_var = tk.StringVar(value=extra_options[0])
    extra_option_menu = tk.OptionMenu(tab2, extra_option_var, *extra_options)
    extra_option_menu.grid(row=2, column=1, padx=5, pady=5)
    # Calculate the maximum length of the options
    max_length = max(len(option) for option in extra_options)
    extra_option_menu.config(width=max_length)
    
    extra_dmg_label = tk.Label(tab2, text="Damage description:")
    extra_dmg_label.grid(row=3, column=0, padx=5, pady=5)
    extra_option_entry = tk.Entry(tab2)
    extra_option_entry.grid(row=3, column=1, padx=5, pady=5) 
    
    tab2_label1 = tk.Label(tab2, text="Player feats")
    tab2_label1.grid(row=4, column=0, padx=5, pady=5, columnspan=2)
    
    # Create a variable to store the state of the checkbox
    checkbox_elven = tk.BooleanVar()
    # Create the checkbox widget and associate it with the variable
    checkbox1 = tk.Checkbutton(tab2, text="Elven Accuracy", variable=checkbox_elven)
    checkbox1.grid(row=5, column=0, padx=5, pady=5) 
    
    # Create a variable to store the state of the checkbox
    checkbox_lucky = tk.BooleanVar()
    checkbox2 = tk.Checkbutton(tab2, text="Halfling Lucky", variable=checkbox_lucky)
    checkbox2.grid(row=5, column=1, padx=5, pady=5) 
    

    
    # Start the main event loop
    root.mainloop()
