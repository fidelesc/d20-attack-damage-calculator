import random
import tkinter as tk
from tkinter import ttk
from numpy import array, savetxt
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.ticker as ticker

FIG_GWMSS = Figure(figsize=(8, 4), dpi=100)
ax_FIG_GWMSS = FIG_GWMSS.add_subplot(111)
FIG_TRACK = Figure(figsize=(8, 4), dpi=100)
ax_FIG_TRACK = FIG_TRACK.add_subplot(111)
FIG_PLOT = Figure(figsize=(8, 4), dpi=100)
ax_FIG_PLOT = FIG_PLOT.add_subplot(111)

### INPUTS
TRACK = None
ATTACK_BONUS = None
WEAPON_DAMAGE_COUNT = None
WEAPON_DAMAGE_DICE = None
DAMAGE_BONUS = None
NUM_ATTACKS = None
CONDITION = None
CRITICAL_OPTION = None
EXTRA = {}
ENEMY_CR = None
ENEMY_AC = None
PLAYER_EFFECTS = None
BARDIC_CONDITION = None

CRIT_RANGE = 20

NUMBER_OF_ROLLS = 100000
ROLL_MULTIPLIER = 1

MULTIPLIERS = ["1", "2", "3", "5", "10"]

GWM_SS_CALCULATIONS = []

TURN_TRACKING = []

PLOT_CALCULATIONS = []

DICES = ["d4","d6","d8","d10","d12"]
EXTRA_DAMAGE_OPTIONS = ["On hit","On hit once per turn", "On critical"]
ATTACK_CONDITIONS = ["Normal", "Advantage", "Disadvantage", "Enemy paralyzed"]


AC_OPTIONS = ["Input AC","Mean AC per CR", "Median AC per CR"]

ENEMY_CR = ["0", "1/8", "1/4", "1/2", "1", "2","3","4","5","6","7","8","9","10",
            "11","12","13","14","15","16","17","18","19","20","21","22","23",
            "24","25","26","27","28","29","30"]

BARDIC_INSPIRATION_DICE = ["No", "1d6", "1d8", "1d10", "1d12"]

SAVAGE_APPLIED_THIS_TURN = False

EXTRA_TOOLTIP = """
Use this format for tooltips.
Use this format for tooltips.
Use this format for tooltips.
Use this format for tooltips.
"""

ENEMY_TOOLTIP = """
Use this format for tooltips.
Use this format for tooltips.
Use this format for tooltips.
Use this format for tooltips.
"""

class WatermarkEntry(tk.Entry):
    def __init__(self, master=None, watermark='', **kw):
        super().__init__(master, **kw)
        self.watermark = watermark
        self.insert(0, self.watermark)
        self.bind('<FocusIn>', self._clear_watermark)
        self.bind('<FocusOut>', self._set_watermark)

    def _clear_watermark(self, event):
        if self.get() == self.watermark:
            self.delete(0, tk.END)

    def _set_watermark(self, event):
        if not self.get():
            self.insert(0, self.watermark)
            
def toggle_tracking():
    if tracking_var.get():
        tracking_var.set(False)
        tracking_button.configure(text="OFF")
    else:
        tracking_var.set(True)
        tracking_button.configure(text="ON")

def clear_tracking():
    global TURN_TRACKING
    TURN_TRACKING = []
    turns_saved_count.configure(text="0")
    
def see_tracking():
    if len(TURN_TRACKING) <= 1:    
        feedback_tracking.configure(text="Insuficient data points saved!")
        return 1
    # Create a new tkinter window to display the plot
    plot_window2 = tk.Toplevel(root)
    plot_window2.title("Turn tracking")
    
    damage_values = [d["damage"] for d in TURN_TRACKING]
    damage_array = array(damage_values)
    
    max_values = [d["max"] for d in TURN_TRACKING]
    max_array = array(max_values)
    
    turns = range(len(TURN_TRACKING))
    
    cumulative_damage = 0
    cumulative_array = []
    for i in range(len(damage_array)):
        cumulative_damage += damage_array[i]
        cumulative_array.append(cumulative_damage)
        
    cumulative_array = array(cumulative_array)

    # global FIG_TRACK
    global ax_FIG_TRACK
    ax_FIG_TRACK.cla()
    ax = ax_FIG_TRACK
    # plt.figure("GWM/SS")
    ax.plot(turns, damage_array, color = "blue", marker="o", label="Average damage")
    ax.plot(turns, max_array, color = "red", marker="o", label="Highest damage")
    ax.plot(turns, cumulative_array, color = "green", marker="o", label="Cumulative damage")
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    ax.set_title("Average damage per turn")
    ax.set_xlabel("Turn")
    ax.set_ylabel("Turn damage")
    ax.grid(axis='y', color='0.90')
    ax.legend()
    
    # Create a canvas to display the plot
    canvas = FigureCanvasTkAgg(FIG_TRACK, master=plot_window2)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, columnspan=10, rowspan=10)
    
    save_button2 = tk.Button(plot_window2, text="SAVE CHART", command=save_tracking_chart)
    save_button2.grid(row=0, column=0, columnspan=1, padx=0, pady=0)
    
    save_button3 = tk.Button(plot_window2, text="SAVE DATA", command=save_tracking_data)
    save_button3.grid(row=0, column=1, columnspan=1, padx=0, pady=0)

def save_tracking_data():
    save_path = filedialog.asksaveasfilename(defaultextension=".csv")
    if save_path:
        output = []
        cumulative_damage = 0
        h = "Enemy AC, Hit chance [%], Critical chance [%], Average damage, Highest damage, Cumulative damage"
        for d in TURN_TRACKING:
            cumulative_damage += d["damage"]
            output.append([d["AC"], d["hit"], d["critical"], d["damage"], d["max"], cumulative_damage])

        savetxt(save_path, output, fmt="%s", delimiter=",", comments="", header=h)

def save_tracking_chart():
    save_path = filedialog.asksaveasfilename(defaultextension=".png")
    if save_path:
        global FIG_TRACK
        FIG_TRACK.savefig(save_path, dpi = 300)

def get_enemy_ac(cr, option):
    """ Get the enemy AC by mean or median from multiple source books"""
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

    if option==AC_OPTIONS[1]:
        return mean_ac[cr]
    elif option==AC_OPTIONS[2]:
        return median_ac[cr]
    else:
        return None

def run_calculation(enemy_ac: int):
    hits = 0
    criticals = 0
    total_damage = 0
    peace = False
    bardic_available = False
    max_damage = 0
    global SAVAGE_AVAILABLE
    
    for _ in range(NUMBER_OF_ROLLS*ROLL_MULTIPLIER):
        once_per_turn = True
        turn_damage = 0
        if PLAYER_EFFECTS["Peace"]: # effect activated once per turn
            peace = True
        if PLAYER_EFFECTS["Bardic"] != "No": # effect activated once per turn
            bardic_available = True
        if PLAYER_EFFECTS["Savage"]:
            SAVAGE_AVAILABLE = True
        else:
            SAVAGE_AVAILABLE = False
            
        for _ in range(NUM_ATTACKS):
            damage = 0
            attack_roll = roll_attack()
            if attack_roll == 1: # Critical Miss!
                peace = False # Apply once per turn
                continue # stop here
            elif attack_roll >= CRIT_RANGE: # Critical Hit!
                peace = False # Apply once per turn
                damage = roll_damage(weapon_damage=True) + roll_damage(weapon_damage=True, critical=True) + roll_damage(on_hit=True) + roll_damage(on_hit=True, critical=True) + roll_damage(on_critical=True)
                if once_per_turn:
                    damage += roll_damage(once_turn=True) + roll_damage(once_turn=True, critical=True)
                    once_per_turn = False
                criticals += 1 # count critical
                turn_damage += damage
                continue
            
            else: # Test for hit
                attack_roll += ATTACK_BONUS
                if PLAYER_EFFECTS["Bless"]: #adds Bless
                    attack_roll += random.randint(1, 4)  # add a d4
                if peace: # adds Emboldening Bond on first attack
                    attack_roll += random.randint(1, 4)  # add a d4
                    peace = False # Apply once per turn
                if bardic_available and attack_roll < BARDIC_CONDITION:
                    attack_roll += random.randint(1, int(PLAYER_EFFECTS["Bardic"][2:]))
                    
                if attack_roll >= enemy_ac: # Hits!
                    hits += 1
                    if CONDITION=="Enemy paralyzed":
                        damage = roll_damage(weapon_damage=True) + roll_damage(weapon_damage=True, critical=True) + roll_damage(on_hit=True) + roll_damage(on_hit=True, critical=True) + roll_damage(on_critical=True)
                        if once_per_turn:
                            damage += roll_damage(once_turn=True) + roll_damage(once_turn=True, critical=True)
                            once_per_turn = False
                    else:
                        damage = roll_damage(weapon_damage=True) + roll_damage(on_hit=True)
                        if once_per_turn:
                            damage += roll_damage(once_turn=True)
                            once_per_turn = False
                    turn_damage += damage
                    
        total_damage += turn_damage
        if max_damage < turn_damage:
            max_damage = turn_damage
        
        
    average_damage = total_damage / (NUMBER_OF_ROLLS*ROLL_MULTIPLIER)
    hit_chance = (hits+criticals) /(NUMBER_OF_ROLLS*ROLL_MULTIPLIER*NUM_ATTACKS)
    critical_chance = criticals / (NUMBER_OF_ROLLS*ROLL_MULTIPLIER*NUM_ATTACKS)
    
    return average_damage, (100*hit_chance), (100*critical_chance), max_damage

def roll_attack():
    
    if CONDITION=="Normal":
        d20_roll = random.randint(1, 20)  # Roll a d20
        if PLAYER_EFFECTS["Halfling Luck"] and d20_roll==1:
            d20_roll = random.randint(1, 20)  # Reroll a d20 for halfing luck
            return d20_roll
        
    elif CONDITION == "Advantage"  or CONDITION=="Enemy paralyzed":
        d20_roll = [random.randint(1, 20), random.randint(1, 20)]  # Roll two d20s and take the higher result
        if PLAYER_EFFECTS["Elven accuracy"]: # Elven Accuracy
            d20_roll.append(random.randint(1, 20))
        if PLAYER_EFFECTS["Halfling Luck"] and 1 in d20_roll:
            d20_roll.append(random.randint(1, 20))  # Reroll a d20 for halfing luck
        
        return max(d20_roll)
    
    elif CONDITION == "Disadvantage":
        d20_roll = min(random.randint(1, 20), random.randint(1, 20))  # Roll two d20s and take the lower result
        if PLAYER_EFFECTS["Halfling Luck"] and d20_roll==1:
            d20_roll = random.randint(1, 20)  # Reroll a d20 for halfing luck
        
    return d20_roll


def roll_damage(weapon_damage=False, on_hit=False, once_turn=False, on_critical=False, critical = False):

    if weapon_damage:
        if critical:
            if CRITICAL_OPTION == "Extra roll":
                return weapon_roll(damage = 0) # Does not apply weapon damage bonus, just roll dice
            elif CRITICAL_OPTION == "Maximum damage": # For maximum damage
                return WEAPON_DAMAGE_COUNT * WEAPON_DAMAGE_DICE
        else:
            return weapon_roll(damage = DAMAGE_BONUS)

    if on_hit:
        if critical:
            if CRITICAL_OPTION == "Extra roll":
                return on_hit_roll(condition="On hit", count_multiplier=2)
            elif CRITICAL_OPTION == "Maximum damage": # For maximum damage
                return on_hit_roll(condition="On hit", maximum=True)
        else:
            return on_hit_roll(condition="On hit")
        
    if once_turn:
        if critical:
            if CRITICAL_OPTION == "Extra roll":
                return on_hit_roll(condition="On hit once per turn", count_multiplier=2)
            elif CRITICAL_OPTION == "Maximum damage": # For maximum damage
                return on_hit_roll(condition="On hit once per turn", maximum=True)
        else:
            return on_hit_roll(condition="On hit once per turn")
        
    if on_critical:
        return on_hit_roll(condition="On critical")
            
def on_hit_roll(condition: str, count_multiplier=1, maximum=False):
    damage = 0
    for d in EXTRA[condition]:
        for _ in range(count_multiplier*d[0]):
            if maximum:
                damage += int(d[1][1:])
            else:
                damage +=  random.randint(1, int(d[1][1:]))
                
    return damage


def weapon_roll(damage):
    global SAVAGE_AVAILABLE
    for _ in range(WEAPON_DAMAGE_COUNT):
        d = random.randint(1, WEAPON_DAMAGE_DICE)
        if d <= 2 and PLAYER_EFFECTS["GWF"]:
            d = random.randint(1, WEAPON_DAMAGE_DICE)
        if d<((WEAPON_DAMAGE_DICE+1)/2) and SAVAGE_AVAILABLE: # If savage is available and the roll is less than the average dice roll
            d = max(d, random.randint(1, WEAPON_DAMAGE_DICE))
            SAVAGE_AVAILABLE = False
        damage += d
    return damage



def plot_range():
    ## Tab 5
    global PLOT_CALCULATIONS
    
    plot_feedback.configure(text="")
    
    feedback_inputs = get_inputs(get_ac=False)
    
    if feedback_inputs is not None:
        plot_feedback.configure(text=feedback_inputs)
        return 1

    try:
        ac0 = int(start_ac_entry.get())
        if ac0 < 0:
            plot_feedback.configure(text="Start AC input not allowed")
    except:
        plot_feedback.configure(text="Start AC input not allowed")
        
    try:
        ac1 = int(end_ac_entry.get())
        if ac1 <= ac0:
            plot_feedback.configure(text="End AC must be higher than start AC")
    except:
        plot_feedback.configure(text="End AC input not allowed")
        
    PLOT_CALCULATIONS = []
    for ac in range(ac0,ac1+1):
        average_damage, hit_chance, critical_chance, max_damage = run_calculation(ac)
        PLOT_CALCULATIONS.append([ac, hit_chance, average_damage])
        
    PLOT_CALCULATIONS = array(PLOT_CALCULATIONS)
    
    plot_feedback.configure(text=f"Finished calculations from AC of {ac0} to {ac1}")
        
    # PLOT CHART
    plot_button5.grid(row=6, column=0, columnspan=10, padx=5, pady=5)
    
def see_plot():
    # global FIG_PLOT
    global PLOT_CALCULATIONS

    # Create a new tkinter window to display the plot
    plot_window3 = tk.Toplevel(root)
    plot_window3.title("Turn plot")
    ax_FIG_PLOT.cla()
    # ax = FIG_PLOT.add_subplot(111)
    ax = ax_FIG_PLOT
    ax.plot(PLOT_CALCULATIONS[:,0], PLOT_CALCULATIONS[:,2], color = "blue", marker="o") #with gwm
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    ax.set_title("Average turn damage per AC")
    ax.set_xlabel("Enemy AC")
    ax.set_ylabel("Turn damage")
    ax.grid(axis='y', color='0.90')
    
    # Create a canvas to display the plot
    canvas = FigureCanvasTkAgg(FIG_PLOT, master=plot_window3)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, columnspan=10, rowspan=10)
    
    save_button8 = tk.Button(plot_window3, text="SAVE CHART", command=save_plot_chart)
    save_button8.grid(row=0, column=0, columnspan=1, padx=0, pady=0)
    
    save_button9 = tk.Button(plot_window3, text="SAVE DATA", command=save_plot_data)
    save_button9.grid(row=0, column=1, columnspan=1, padx=0, pady=0)

def save_plot_data():
    save_path = filedialog.asksaveasfilename(defaultextension=".csv")
    if save_path:
        h = "Enemy AC, Hit chance [%], Average damage"

        savetxt(save_path, PLOT_CALCULATIONS, fmt="%s", delimiter=",", comments="", header=h)
        
def save_plot_chart():
    save_path = filedialog.asksaveasfilename(defaultextension=".png")
    if save_path:
        global FIG_PLOT
        FIG_PLOT.savefig(save_path, dpi = 300)
        
def calculate_damage():
    feedback.configure(text="")
    result_label1.configure(text="")
    result_label2.configure(text="")
    result_label3.configure(text="")
    result_label4.configure(text="")
    result_label5.configure(text="")
    
    feedback_inputs = get_inputs()
    
    if feedback_inputs is not None:
        feedback.configure(text=feedback_inputs)
        return 1
    
    average_damage, hit_chance, critical_chance, max_damage = run_calculation(ENEMY_AC)
    
    if TRACK:
        feedback.configure(text="Turn calculation saved")
        
    result_label1.configure(text=f"Using enemy AC of {ENEMY_AC}")
    result_label2.configure(text=f"Attack success rate: {hit_chance:.2f} %")
    result_label3.configure(text=f"Attack critical chance: {critical_chance:.2f} %")
    result_label4.configure(text=f"Estimated damage per turn: {average_damage:.2f}")
    result_label5.configure(text=f"Highest damage per turn: {max_damage:.2f}")
    
    if TRACK:
        global TURN_TRACKING
        TURN_TRACKING.append({"damage": average_damage,
                              "hit": hit_chance,
                              "critical": critical_chance,
                              "AC": ENEMY_AC,
                              "max": max_damage})
        
        turns_saved_count.configure(text=str(len(TURN_TRACKING)))
    
def check_GWM_SS():
    
    global ATTACK_BONUS
    global DAMAGE_BONUS
    global GWM_SS_CALCULATIONS

    feedback7.configure(text="")
    feedback7b.configure(text="")
    
    feedback_inputs = get_inputs(get_ac=False)
    
    if feedback_inputs is not None:
        feedback7.configure(text=feedback_inputs)
        return 1
        
    try:
        ac0 = int(start_ac_entry7.get())
    except:
        feedback7.configure(text="Incorrect Start AC input")
        return 1
    if ac0 <= 0:
        feedback7.configure(text="Incorrect Start AC input")
        return 1
    try:
        ac1 = int(end_ac_entry7.get())
    except:
        feedback7.configure(text="Incorrect End AC input")
        return 1
    if ac1 <= 0:
        feedback7.configure(text="Incorrect End AC input")
        return 1
    if ac0 >= ac1:
        feedback7.configure(text="Start AC cannot be higher than End AC!")
        return 1
    
    if checkbox_gwmss.get():   # if GWM and SS is already true, remove it here
        ATTACK_BONUS += +5
        DAMAGE_BONUS += -10

    calculations_without = []
    for ac in range(ac0,ac1+1):
        average_damage, hit_chance, critical_chance, max_damage = run_calculation(ac)
        calculations_without.append([average_damage, hit_chance])

    # turn ON GWM and SS
    ATTACK_BONUS += -5
    DAMAGE_BONUS += 10

    calculations_with = []
    for ac in range(ac0,ac1+1):
        average_damage, hit_chance, critical_chance, max_damage = run_calculation(ac)
        calculations_with.append([average_damage, hit_chance, ac])
       
    stop = None
    for i in range(len(calculations_with)):
        if calculations_with[i][0] > calculations_without[i][0]:
            stop = calculations_with[i][2]
        else:
            break

    GWM_SS_CALCULATIONS = []
    for i in range(len(calculations_with)):
        GWM_SS_CALCULATIONS.append([calculations_with[i][2],calculations_with[i][0], calculations_without[i][0]])
    
    GWM_SS_CALCULATIONS = array(GWM_SS_CALCULATIONS, dtype=object)
        
    feedback7.configure(text=f"Finished calculations from AC of {ac0} to {ac1}")
    if stop == None:
        feedback7b.configure(text="Great Weapon Master / Sharpshooter should not be used in this AC range")
    else:
        feedback7b.configure(text=f"Great Weapon Master / Sharpshooter is optimum for enemy AC < {stop}")
        
    # PLOT CHART
    chart_button8.grid(row=6, column=0, columnspan=10, padx=5, pady=5)



def see_gwmss_chart():
    # Create a new tkinter window to display the plot
    plot_window = tk.Toplevel(root)
    plot_window.title("GWM / SS plot")

    # global FIG_GWMSS
    ax_FIG_GWMSS.cla()
    ax = ax_FIG_GWMSS
    ax.plot(GWM_SS_CALCULATIONS[:,0], GWM_SS_CALCULATIONS[:,1], color = "blue", marker="o", label="With GWM/SS") #with gwm
    ax.plot(GWM_SS_CALCULATIONS[:,0], GWM_SS_CALCULATIONS[:,2], color = "red", marker="o", label="Without GWM/SS")
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    ax.set_title("Average turn damage per AC")
    ax.set_xlabel("Enemy AC")
    ax.set_ylabel("Turn damage")
    ax.grid(axis='y', color='0.90')
    ax.legend()
    
    # Create a canvas to display the plot
    canvas = FigureCanvasTkAgg(FIG_GWMSS, master=plot_window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, columnspan=10, rowspan=10)
    
    save_button = tk.Button(plot_window, text="SAVE CHART", command=save_gwmss_chart)
    save_button.grid(row=0, column=0, columnspan=1, padx=0, pady=0)
    
    save_button4 = tk.Button(plot_window, text="SAVE DATA", command=save_gwmss_data)
    save_button4.grid(row=0, column=1, columnspan=1, padx=0, pady=0)

def save_gwmss_data():
    save_path = filedialog.asksaveasfilename(defaultextension=".csv")
    if save_path:
        h = "Enemy AC, Damage with GWM/SS, Damage without GWM/SS"

        savetxt(save_path, GWM_SS_CALCULATIONS, fmt="%s", delimiter=",", comments="", header=h)
        
def save_gwmss_chart():
    save_path = filedialog.asksaveasfilename(defaultextension=".png")
    if save_path:
        global FIG_GWMSS
        FIG_GWMSS.savefig(save_path, dpi = 300)
    


def get_inputs(get_ac=True):
    global TRACK
    global ATTACK_BONUS
    global WEAPON_DAMAGE_COUNT
    global WEAPON_DAMAGE_DICE
    global DAMAGE_BONUS
    global NUM_ATTACKS
    global CONDITION
    global CRITICAL_OPTION
    global EXTRA
    global ENEMY_CR
    global ENEMY_AC
    global PLAYER_EFFECTS
    global BARDIC_CONDITION
    global CRIT_RANGE


## Tab 1
    try:
        ATTACK_BONUS = int(attack_bonus_entry.get())
    except:
        return "Incorrect Attack bonus entry"
    
    try:
        WEAPON_DAMAGE_COUNT = int(weapon_damage_count.get())
    except:
        return "Incorrect Weapon damage entry"
    
    WEAPON_DAMAGE_DICE = int(weapon_damage_dice.get()[1:])
    
    try:
        DAMAGE_BONUS = int(damage_bonus_entry.get())
    except:
        return "Incorrect Damage bonus entry"
    
    try:
        NUM_ATTACKS = int(num_attacks_entry.get())
    except:
        return "Incorrect Attacks per turn entry"
    
    CONDITION = conditions_var.get()
    CRITICAL_OPTION = critical_option_var.get()

## Tab 2
    EXTRA = {"On hit": [],
             "On hit once per turn": [],
             "On critical": []
             }
    
    for i in range(len(dice_counts)):
        try:
            dice_count = int(dice_counts[i].get())
            dice = damage_dices[i].get()
            condition = extra_options[i].get()

        except:
            return f"Incorrect Extra damage entry: {i+1}"
        if dice_count >= 0:
            if dice_count > 0:
                EXTRA[condition].append([dice_count, dice])
        else:
            return f"Incorrect Extra damage entry: {i+1}"

## Tab 3
    if get_ac:
        ac_option = ac_option_var.get()
        if ac_option == AC_OPTIONS[0]: # Use input AC
            try:
                ac = int(ac_entry.get())
                if ac < 0:
                    return "Incorrect Enemy AC entry"
            except:
                return "Incorrect Enemy AC entry"
        else:
            cr = enemy_cr_input.get()
            ENEMY_CR = cr
            ac = get_enemy_ac(cr, ac_option)
            
            try:
                debuff = int(enemy_effect_entry.get())
                ac = ac+debuff
            except:
                if enemy_effect_entry.get() == '-2,-1,0,1,2,...':
                    pass
                else:
                    return "Incorrect Enemy AC changes entry"
        ENEMY_AC = ac
    
## Tab 4

    PLAYER_EFFECTS = {
              "Elven accuracy": checkbox_elven.get(),
              "Halfling Luck": checkbox_lucky.get(),
              "GWF": checkbox_gwf.get(),
              "Savage": checkbox_savage.get(),
              "Bless": checkbox_bless.get(),
              "Peace": checkbox_bond.get(),
              "Bardic": bardic_var.get()             
             }
    
    try:
        CRIT_RANGE = int(crit_entry.get())
    except:
        return "Critical range not accepted"
    if CRIT_RANGE <= 1 or CRIT_RANGE > 20:
        return "Critical range not accepted"

    if checkbox_gwmss.get():   # if GWM and SS is true, do -5/+10
        ATTACK_BONUS += -5
        DAMAGE_BONUS += 10
        
    if bardic_var.get() != "No":
        try:
            BARDIC_CONDITION = int(bardic_entry.get())
        except:
            return "Incorrect Bardic Inspiration condition entry"
        if BARDIC_CONDITION <= 0:
            return "Incorrect Bardic Inspiration condition entry"
## Tab 6

    TRACK = tracking_var.get()
   

def save_config():
    global ROLL_MULTIPLIER
    
    ROLL_MULTIPLIER = int(multiplier_var.get())
    
    tab8_feedback.configure(text=f"Roll multiplier changed to {ROLL_MULTIPLIER}")

if __name__ == '__main__':
        
    # Create the main window
    root = tk.Tk()
    root.title("d20 Damage Calculator")
    
    # Create the Notebook widget
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)
    
    # Create tab 1
    tab1 = tk.Frame(notebook)
    notebook.add(tab1, text="Attack")
    
    # Create tab 2
    tab2 = tk.Frame(notebook)
    notebook.add(tab2, text="Extras")
    
    # Create tab 3
    tab3 = tk.Frame(notebook)
    notebook.add(tab3, text="Enemy")
    
    # Create tab 4
    tab4 = tk.Frame(notebook)
    notebook.add(tab4, text="Player")
    
    # Create tab 6
    tab6 = tk.Frame(notebook)
    notebook.add(tab6, text="Datapoints")
    
    # Create tab 5
    tab5 = tk.Frame(notebook)
    notebook.add(tab5, text="Plot")
       
    # Create tab 7
    tab7 = tk.Frame(notebook)
    notebook.add(tab7, text="GWM/SS")
    
    # Create tab 8
    tab8 = tk.Frame(notebook)
    notebook.add(tab8, text="Config")
    
###############################################################################
    ## TAB 1
    
    # Create the input fields  
    left_label = tk.Label(tab1, text="Player attack")
    left_label.grid(row=0, column=0, padx=5, pady=5, columnspan=4)
       
    attack_bonus_label = tk.Label(tab1, text="Attack bonus:")
    attack_bonus_entry = WatermarkEntry(tab1, watermark='-1,+1,+2,...')
    attack_bonus_label.grid(row=1, column=0, padx=5, pady=5)
    attack_bonus_entry.grid(row=1, column=1, padx=5, pady=5)
    
    weapon_damage_label = tk.Label(tab1, text="Weapon damage:")
    weapon_damage_label.grid(row=2, column=0, padx=5, pady=5)
    weapon_damage_count = WatermarkEntry(tab1, watermark='1,2,...')
    weapon_damage_count.grid(row=2, column=1, padx=5, pady=5, sticky='w')
    weapon_damage_count.config(width = 6)
    weapon_damage_dice = tk.StringVar(value=DICES[0])
    menu = tk.OptionMenu(tab1, weapon_damage_dice, *DICES)
    menu.grid(row=2, column=1, padx=0, pady=5, sticky='e')
    # Calculate the maximum length of the options
    max_length = max(len(option) for option in DICES)
    menu.config(width=max_length+1)
    
    damage_bonus_label = tk.Label(tab1, text="Damage bonus:")
    damage_bonus_entry = WatermarkEntry(tab1, watermark='-1,+1,+2,...')
    damage_bonus_label.grid(row=3, column=0, padx=5, pady=5)
    damage_bonus_entry.grid(row=3, column=1, padx=5, pady=5)  
    
    num_attacks_label = tk.Label(tab1, text="Attacks per turn:")
    num_attacks_entry = WatermarkEntry(tab1, watermark='1,2,3,...')
    num_attacks_label.grid(row=1, column=2, padx=5, pady=5)
    num_attacks_entry.grid(row=1, column=3, padx=5, pady=5) 
    num_attacks_entry.config(width=18)
    
    # Create the dropdown menu for selecting game edition
    edition_label = tk.Label(tab1, text="Attack condition:")
    edition_label.grid(row=2, column=2, padx=5, pady=5)
    conditions_var = tk.StringVar(value=ATTACK_CONDITIONS[0])
    condition_menu = tk.OptionMenu(tab1, conditions_var, *ATTACK_CONDITIONS)
    condition_menu.grid(row=2, column=3, padx=5, pady=5)
    # Calculate the maximum length of the options
    max_length = max(len(option) for option in ATTACK_CONDITIONS)
    condition_menu.config(width=max_length)
    
    critical_option_label = tk.Label(tab1, text="Critical option:")
    critical_options = ["Extra roll", "Maximum damage"]
    critical_option_var = tk.StringVar(value=critical_options[0])
    critical_option_menu = tk.OptionMenu(tab1, critical_option_var, *critical_options)
    critical_option_label.grid(row=3, column=2, padx=5, pady=5)
    critical_option_menu.grid(row=3, column=3, padx=5, pady=5)
    # Calculate the maximum length of the options
    max_length = max(len(option) for option in critical_options)
    critical_option_menu.config(width=max_length+2)
    
    # Create the button to calculate the estimated damage
    calculate_button = tk.Button(tab1, text="CALCULATE", command=calculate_damage)
    calculate_button.grid(row=4, column=0, columnspan=4, padx=5, pady=5)
    feedback = tk.Label(tab1, text="")
    feedback.grid(row=5, column=0, columnspan=5, padx=5, pady=5)
    
    # Create the label to display the result
    result_label1 = tk.Label(tab1, text="")
    result_label1.grid(row=7, column=0, columnspan=5, padx=5, pady=5)
    result_label2 = tk.Label(tab1, text="")
    result_label2.grid(row=8, column=0, columnspan=5, padx=5, pady=5)
    result_label3 = tk.Label(tab1, text="")
    result_label3.grid(row=9, column=0, columnspan=5, padx=5, pady=5)
    result_label4 = tk.Label(tab1, text="")
    result_label4.grid(row=10, column=0, columnspan=5, padx=5, pady=5)
    result_label5 = tk.Label(tab1, text="")
    result_label5.grid(row=11, column=0, columnspan=5, padx=5, pady=5)
    
###############################################################################
    ### TAB 2  
    extra_damage_label = tk.Label(tab2, text="Extra damage:")
    extra_damage_label.grid(row=0, column=0, padx=5, pady=5, columnspan=4)
    
    extra_damage_help = tk.Label(tab2, text=EXTRA_TOOLTIP)
    extra_damage_help.grid(row=0, column=4, padx=5, pady=5, rowspan=5)
    
    extra_dmg_labels = []
    dice_counts = []
    damage_dices = []
    extra_options = []
    
    for i in range(0,5):
    
        extra_dmg_labels.append(tk.Label(tab2, text="Damage:"))
        extra_dmg_labels[i].grid(row=i+1, column=0, padx=5, pady=5)
        
        
        entry = WatermarkEntry(tab2, watermark='0')
        entry.config(width=4)
        dice_counts.append(entry)
        dice_counts[i].grid(row=i+1, column=1, pady=5, sticky='e')
         
        damage_dices.append(tk.StringVar(value=DICES[0]))
        menu = tk.OptionMenu(tab2, damage_dices[i], *DICES)
        menu.grid(row=i+1, column=2, padx=5, pady=5)
        # Calculate the maximum length of the options
        max_length = max(len(option) for option in DICES)
        menu.config(width=max_length)
        
        extra_options.append(tk.StringVar(value=EXTRA_DAMAGE_OPTIONS[0]))
        menu = tk.OptionMenu(tab2, extra_options[i], *EXTRA_DAMAGE_OPTIONS)
        menu.grid(row=i+1, column=3, padx=0, pady=5)
        # Calculate the maximum length of the options
        max_length = max(len(option) for option in EXTRA_DAMAGE_OPTIONS)
        menu.config(width=max_length)
       
###############################################################################
    ## Tab 3
        
    tab3_label = tk.Label(tab3, text="Enemy information")
    tab3_label.grid(row=0, column=0, padx=5, pady=5, columnspan=4)
    
    ac_option_var = tk.StringVar(value=AC_OPTIONS[0])
    ac_option_menu = tk.OptionMenu(tab3, ac_option_var, *AC_OPTIONS)
    ac_option_menu.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
    # Calculate the maximum length of the options
    max_length = max(len(option) for option in AC_OPTIONS)
    ac_option_menu.config(width=max_length)
    
    enemy_ac_label = tk.Label(tab3, text="Enemy AC:")
    enemy_ac_label.grid(row=2, column=0, padx=5, pady=5)
    
    ac_entry = WatermarkEntry(tab3, watermark='0,1,2,...')
    ac_entry.grid(row=2, column=1, padx=5, pady=5)
    
    cr_label = tk.Label(tab3, text="Enemy CR:")
    cr_label.grid(row=3, column=0, padx=5, pady=5)
    
    enemy_cr_input = tk.StringVar(value=ENEMY_CR[0])
    enemy_cr_menu = tk.OptionMenu(tab3, enemy_cr_input, *ENEMY_CR)
    enemy_cr_menu.grid(row=3, column=1, padx=5, pady=5)
    # Calculate the maximum length of the options
    max_length = max(len(option) for option in ENEMY_CR)
    enemy_cr_menu.config(width=14)
    
    enemy_debuff_label = tk.Label(tab3, text="Enemy AC changes:")
    enemy_debuff_label.grid(row=4, column=0, padx=5, pady=5)
    
    enemy_effect_entry = WatermarkEntry(tab3, watermark='-2,-1,0,1,2,...')
    enemy_effect_entry.grid(row=4, column=1, padx=5, pady=5)
    
    enemy_help = tk.Label(tab3, text=ENEMY_TOOLTIP)
    enemy_help.grid(row=0, column=3, padx=5, pady=5, rowspan=5, columnspan=3)
    
###############################################################################
    ## Tab 4

    tab4_label1 = tk.Label(tab4, text="Player feats")
    tab4_label1.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
    
    # Create a variable to store the state of the checkbox
    checkbox_elven = tk.BooleanVar()
    # Create the checkbox widget and associate it with the variable
    checkbox1 = tk.Checkbutton(tab4, text=" Elven Accuracy", variable=checkbox_elven)
    checkbox1.grid(row=1, column=0, padx=5, pady=5, sticky="w") 
    
    # Create a variable to store the state of the checkbox
    checkbox_lucky = tk.BooleanVar()
    checkbox2 = tk.Checkbutton(tab4, text=" Halfling Luck", variable=checkbox_lucky)
    checkbox2.grid(row=1, column=1, padx=5, pady=5, sticky="w") 
    
    # Create a variable to store the state of the checkbox
    checkbox_gwf = tk.BooleanVar()
    checkbox3 = tk.Checkbutton(tab4, text=" Great Weapon Fighting", variable=checkbox_gwf)
    checkbox3.grid(row=2, column=0, padx=5, pady=5, sticky="w") 
    
    # Create a variable to store the state of the checkbox
    checkbox_savage = tk.BooleanVar()
    checkbox4 = tk.Checkbutton(tab4, text=" Savage Attacker", variable=checkbox_savage)
    checkbox4.grid(row=2, column=1, padx=5, pady=5, sticky="w") 
    
    # Create a variable to store the state of the checkbox
    checkbox_gwmss = tk.BooleanVar()
    checkbox7 = tk.Checkbutton(tab4, text=" Great Weapon Master \n Sharpshooter", variable=checkbox_gwmss)
    checkbox7.grid(row=3, column=0, padx=5, pady=5, sticky="w") 
    
    tab4_label3 = tk.Label(tab4, text="Improved critical:\n(critical hit when roll\nequals or higher than)")
    tab4_label3.grid(row=4, column=0, padx=5, pady=5, sticky="e")
    
    crit_entry = WatermarkEntry(tab4, watermark='20')
    crit_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
    crit_entry.configure(width=8)
    
    tab4_label2 = tk.Label(tab4, text="Player buffs")
    tab4_label2.grid(row=5, column=0, padx=5, pady=5, columnspan=2)
    
    tab4_label3 = tk.Label(tab4, text="Bardic Inspiration")
    tab4_label3.grid(row=6, column=0, padx=5, pady=5)
    
    bardic_var = tk.StringVar(value=BARDIC_INSPIRATION_DICE[0])
    bardic_dice_menu = tk.OptionMenu(tab4, bardic_var, *BARDIC_INSPIRATION_DICE)
    bardic_dice_menu.grid(row=6, column=1, padx=5, pady=5)
    # Calculate the maximum length of the options
    max_length = max(len(option) for option in BARDIC_INSPIRATION_DICE)
    bardic_dice_menu.config(width=max_length)
    
    
    tab4_label4 = tk.Label(tab4, text="Use Bardic Inspiration \nwhen total attack roll less than:")
    tab4_label4.grid(row=7, column=0, padx=5, pady=5)
    
    bardic_entry = WatermarkEntry(tab4, watermark='5,6,7...')
    bardic_entry.grid(row=7, column=1, padx=5, pady=5)
    
    # Create a variable to store the state of the checkbox
    checkbox_bless = tk.BooleanVar()
    # Create the checkbox widget and associate it with the variable
    checkbox5 = tk.Checkbutton(tab4, text=" Bless", variable=checkbox_bless)
    checkbox5.grid(row=8, column=0, padx=5, pady=5, sticky="w") 
    
    # Create a variable to store the state of the checkbox
    checkbox_bond = tk.BooleanVar()
    checkbox6 = tk.Checkbutton(tab4, text=" Emboldening Bond", variable=checkbox_bond)
    checkbox6.grid(row=8, column=1, padx=5, pady=5, sticky="w") 
    
###############################################################################
    ## Tab 5
    
    tab5_label1 = tk.Label(tab5, text="Plot calculations for a range of AC values")
    tab5_label1.grid(row=0, column=0, padx=5, pady=5, columnspan=4)
    
    tab5_label2 = tk.Label(tab5, text="Start AC: ")
    tab5_label2.grid(row=1, column=0, padx=5, pady=5)
    
    start_ac_entry = WatermarkEntry(tab5, watermark='0')
    start_ac_entry.grid(row=1, column=1, padx=5, pady=5)
    start_ac_entry.configure(width=8)
    
    tab5_label3 = tk.Label(tab5, text="End AC: ")
    tab5_label3.grid(row=1, column=2, padx=5, pady=5)
    
    end_ac_entry = WatermarkEntry(tab5, watermark='30')
    end_ac_entry.grid(row=1, column=3, padx=5, pady=5)
    end_ac_entry.configure(width=8)
    
    # Create the button to calculate the estimated damage
    plot_button = tk.Button(tab5, text="PLOT", command=plot_range)
    plot_button.grid(row=2, column=0, columnspan=4, padx=5, pady=5)
    
    # Create the label to display the result
    plot_feedback = tk.Label(tab5, text="")
    plot_feedback.grid(row=4, column=0, columnspan=5, padx=5, pady=5)
    
    plot_button5 = tk.Button(tab5, text="SEE PLOT", command=see_plot)
    
###############################################################################
    ## Tab 6
    
    tab6_label1 = tk.Label(tab6, text="Save turn calculations for plotting")
    tab6_label1.grid(row=0, column=0, padx=5, pady=5, columnspan=4)
    
    tab6_label2 = tk.Label(tab6, text="Track calculations")
    tab6_label2.grid(row=1, column=0, padx=5, pady=5)
    
    # Create a variable to store the state of the switch
    tracking_var = tk.BooleanVar(value=False)
    # Create the switch button widget and associate it with the variable
    tracking_button = tk.Button(tab6, text="OFF", command=toggle_tracking)
    tracking_button.grid(row=1, column=1, padx=5, pady=5)
    tracking_button.configure(width=6)
    
    tab6_label3 = tk.Label(tab6, text="Turns saved:")
    tab6_label3.grid(row=1, column=2, padx=0, pady=5)
    
    turns_saved_count = tk.Label(tab6, text="0")
    turns_saved_count.grid(row=1, column=3, padx=0, pady=5, sticky="w")
    
    # Create the switch button widget and associate it with the variable
    clear_tracking_button = tk.Button(tab6, text="CLEAR TRACKED TURNS", command=clear_tracking)
    clear_tracking_button.grid(row=2, column=0, padx=5, pady=5, columnspan=4)
    
    # Create the switch button widget and associate it with the variable
    see_tracking_button = tk.Button(tab6, text="SEE TRACKED TURNS", command=see_tracking)
    see_tracking_button.grid(row=3, column=0, padx=5, pady=5, columnspan=4)
    
    feedback_tracking = tk.Label(tab6, text="")
    feedback_tracking.grid(row=4, column=0, padx=5, pady=5, columnspan=4)
    
###############################################################################
    ## Tab 7
    
    tab7_label1 = tk.Label(tab7, text="Check effectiveness of Great Weapon Master or Sharpshooter")
    tab7_label1.grid(row=0, column=0, padx=5, pady=5, columnspan=10)
    
    tab7_label2 = tk.Label(tab7, text="Start AC:")
    tab7_label2.grid(row=1, column=0, padx=5, pady=5)
    
    start_ac_entry7 = WatermarkEntry(tab7, watermark='5')
    start_ac_entry7.grid(row=1, column=1, padx=5, pady=5)
    start_ac_entry7.configure(width=8)
    
    tab7_label3 = tk.Label(tab7, text="End AC:")
    tab7_label3.grid(row=1, column=3, padx=5, pady=5)
    
    end_ac_entry7 = WatermarkEntry(tab7, watermark='30')
    end_ac_entry7.grid(row=1, column=4, padx=5, pady=5)
    end_ac_entry7.configure(width=8)
    
    tab7_label2 = tk.Label(tab7, text="Note: this will turn ON the Great Weapon Master / Sharpshooter feat option \n for these calculations")
    tab7_label2.grid(row=2, column=0, padx=5, pady=5, columnspan=10)
    
    # Create the button to calculate the estimated damage
    calculate_button7 = tk.Button(tab7, text="CALCULATE", command=check_GWM_SS)
    calculate_button7.grid(row=3, column=0, columnspan=10, padx=5, pady=5)
    feedback7 = tk.Label(tab7, text="")
    feedback7.grid(row=4, column=0, columnspan=10, padx=5, pady=5)
    feedback7b = tk.Label(tab7, text="")
    feedback7b.grid(row=5, column=0, columnspan=10, padx=5, pady=5)
    
    chart_button8 = tk.Button(tab7, text="SEE CHART", command=see_gwmss_chart)
    # calculate_button7.grid(row=6, column=0, columnspan=10, padx=5, pady=5)
    
###############################################################################
## Tab 8
    tab8_label1 = tk.Label(tab8, text="Configurations")
    tab8_label1.grid(row=0, column=0, padx=5, pady=5, columnspan=10)
    
    tab8_label2 = tk.Label(tab8, text="Roll multiplier")
    tab8_label2.grid(row=1, column=0, padx=5, pady=5)
    
    multiplier_var = tk.StringVar(value=MULTIPLIERS[0])
    multiplier_menu = tk.OptionMenu(tab8, multiplier_var, *MULTIPLIERS)
    multiplier_menu.grid(row=1, column=1, padx=5, pady=5)
    # Calculate the maximum length of the options
    max_length = max(len(option) for option in MULTIPLIERS)
    multiplier_menu.config(width=max_length)
    
    config_button = tk.Button(tab8, text="SAVE", command=save_config)
    config_button.grid(row=4, column=0, columnspan=10, padx=5, pady=5)
    
    tab8_feedback = tk.Label(tab8, text="")
    tab8_feedback.grid(row=5, column=0, padx=5, pady=5, columnspan=10)
    
    
###############################################################################
    
    # Start the main event loop
    root.mainloop()
