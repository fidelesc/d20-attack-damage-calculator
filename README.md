# d20 Calculator - GUI Interface

This is a simple GUI interface for a d20 system calculator that estimates the average attack damage per turn, based on the user's input. There is an option for using monster's CR, which currently only supports D&D options (see database folder).

The calculator uses Python's `random` module and the `tkinter` library to create a graphical user interface.

## Contents

- Python script.
- Windows executable.
- Database of enemy AC per CR.

## How to use

To use the D&D calculator, simply input the required parameters in the input fields, and click on the "Calculate" button to get the estimated damage output. 

The input fields are:
- `Attacks per Turn`: The number of attacks the player makes per turn.
- `Attack Bonus`: The attack bonus is the bonus to the player's attack roll.
- `Attack Description`: A description of the player's attack, which includes the number of dice, dice size, and modifier. For example, "2d6+3" means the player rolls 2 six-sided dice and adds 3 to the result.

- `Enemy AC`: The armor class (AC) of the enemy, which is the value that a player must roll to hit them.
- `Enemy CR`: The enemy CR to get either the mean or median value for AC. Accepts 0,1/8,1/4,1/2,1,2,...,30.

- `Attack Condition`: Normal (No advantage or disadvantage), Advantage (Roll two d20s and take the higher result), Disadvantage (Roll two d20s and take the lower result), Enemy paralyzed within 5 ft (The attack roll has advantage and any hit is a critical hit).
- `Critical Option`: The option for handling critical hits, which can be set to "Extra roll" or "Maximum damage". While in "Extra roll", the critical hit doubles the number of attack dices (2d6+4 becomes 4d6+4). The "Maximum damage" options adds the maximum dice roll (2d6+4 becomes 2d6+4+12).
- `Extra Damage`: (OPTIONAL) Extra damage roll (for example "2d6+3"), and option to apply "on hit" (every hit), "on critical" (added average damage, NOT CRITICAL, on a critical hit), and "on hit once per turn" is a damage applied once per turn if a hit happens.

- `Player feats`: Feats that affect the attack roll not included in `Attack Condition`. Note that Elven Accuracy only works if Attack Condition is set to Advantage or Enemy paralyzed.

Once the user clicks on the "Calculate" button, the calculator estimates the average damage output per turn, and displays the result in the output field.

It will also display the enemy AC used for calculations.
