import random
import tkinter as tk


def test_attack_roll(ac, attack_bonus):
    """Test the attack roll for a given AC and attack bonus."""
    d20_roll = random.randint(1, 20)  # Roll a d20
    if d20_roll == 20:
        return 2  # Critical hit!
    elif d20_roll == 1:
        return 0  # Critical miss :(
    else:
        if d20_roll + attack_bonus >= ac:
            return 1
        else:
            return 0


def get_damage(attacks_per_turn, ac, attack_bonus, num_dice, dice_size, modifier, critical_option):
    """Get the average damage rate for a given AC and attack bonus."""
    damage_count = 0
    turn = []
    total_rolls = 100000  # Roll 100,000 times to get an accurate average
    for i in range(total_rolls):
        damage_per_turn = 0
        for j in range(attacks_per_turn):
            test = test_attack_roll(ac, attack_bonus)
            if test==0:
                damage_count += 0
                damage_per_turn += 0
            elif test==1:
                damage_count += calculate_average_damage(num_dice, dice_size, modifier)
                damage_per_turn += calculate_average_damage(num_dice, dice_size, modifier)
            elif test==2:
                damage_count += calculate_average_damage(num_dice, dice_size, modifier, critical_option)
                damage_per_turn += calculate_average_damage(num_dice, dice_size, modifier, critical_option)
    
            turn.append(damage_per_turn)
    average_damage = damage_count / total_rolls
    average_turn = sum(turn) / len(turn)
    return average_damage, average_turn
    
def get_success_rate(ac, attack_bonus):
    """Get the average success rate for a given AC and attack bonus."""
    success_count = 0
    total_rolls = 200000  # Roll 100,000 times to get an accurate average
    for i in range(total_rolls):
        if test_attack_roll(ac, attack_bonus):
            success_count += 1
    return success_count / total_rolls

def calculate_average_damage(num_dice, dice_size, modifier, critical_option="soft"):
    """Calculate the average damage for a given attack description, with an option for critical damage."""

    # Calculate the average damage based on the dice size
    if critical_option == "normal":
        average_damage = ((2*num_dice)*((dice_size + 1) / 2))+modifier
    elif critical_option == "full damage":
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
    ac = int(ac_entry.get())
    attack_bonus = int(attack_bonus_entry.get())
    num_attacks = int(num_attacks_entry.get())
    attack_description = attack_description_entry.get()
    num_dice, dice_size, modifier = get_attack_description(attack_description)
    critical_option = critical_option_var.get()

    success_rate = get_success_rate(ac, attack_bonus)
    average_damage, estimated_damage = get_damage(num_attacks, ac, attack_bonus, num_dice, dice_size, modifier, critical_option)

    result_label.configure(text=f"Estimated damage per turn: {estimated_damage:.2f}")
    result_label2.configure(text=f"Attack success rate: {success_rate:.2f}")
        
if __name__ == '__main__':
    
    # Create the main window
    root = tk.Tk()
    root.title("D&D Damage Calculator")
    
    # Create the input fields
    ac_label = tk.Label(root, text="Enemy AC:")
    ac_entry = tk.Entry(root)
    ac_label.grid(row=0, column=0, padx=5, pady=5)
    ac_entry.grid(row=0, column=1, padx=5, pady=5)
    
    attack_bonus_label = tk.Label(root, text="Attack Bonus:")
    attack_bonus_entry = tk.Entry(root)
    attack_bonus_label.grid(row=1, column=0, padx=5, pady=5)
    attack_bonus_entry.grid(row=1, column=1, padx=5, pady=5)
    
    num_attacks_label = tk.Label(root, text="Attacks per Turn:")
    num_attacks_entry = tk.Entry(root)
    num_attacks_label.grid(row=2, column=0, padx=5, pady=5)
    num_attacks_entry.grid(row=2, column=1, padx=5, pady=5)
    
    attack_description_label = tk.Label(root, text="Attack Description:")
    attack_description_entry = tk.Entry(root)
    attack_description_label.grid(row=3, column=0, padx=5, pady=5)
    attack_description_entry.grid(row=3, column=1, padx=5, pady=5)
    
    critical_option_label = tk.Label(root, text="Critical Option:")
    critical_option_var = tk.StringVar(value="normal")
    critical_option_menu = tk.OptionMenu(root, critical_option_var, "normal", "full damage")
    critical_option_label.grid(row=4, column=0, padx=5, pady=5)
    critical_option_menu.grid(row=4, column=1, padx=5, pady=5)
    
    # Create the button to calculate the estimated damage
    calculate_button = tk.Button(root, text="Calculate", command=calculate_estimated_damage)
    calculate_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
    
    # Create the label to display the result
    result_label = tk.Label(root, text="")
    result_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
    result_label2 = tk.Label(root, text="")
    result_label2.grid(row=8, column=0, columnspan=2, padx=5, pady=5)
    
    # Start the main event loop
    root.mainloop()
