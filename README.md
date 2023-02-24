# Dungeons and Dragons Calculator - GUI Interface

This is a simple GUI interface for a Dungeons and Dragons (D&D) calculator that estimates the average attack damage per turn, based on the user's input. The calculator uses Python's `random` module and the `tkinter` library to create a graphical user interface.

I added an executable for windows.

## How to use

To use the D&D calculator, simply input the required parameters in the input fields, and click on the "Calculate" button to get the estimated damage output. 

The input fields are:
- `Enemy AC`: The armor class (AC) of the enemy, which is the value that a player must roll to hit them.
- `Attack Bonus`: The attack bonus is the bonus to the player's attack roll.
- `Attacks per Turn`: The number of attacks the player makes per turn.
- `Attack Description`: A description of the player's attack, which includes the number of dice, dice size, and modifier. For example, "2d6+3" means the player rolls 2 six-sided dice and adds 3 to the result.
- `Critical Option`: The option for handling critical hits, which can be set to "normal" or "full damage".

Once the user clicks on the "Calculate" button, the calculator estimates the average damage output per turn, and displays the result in the output field.


## Code documentation

The code contains several functions, including:

### `test_attack_roll(ac, attack_bonus)`

This function tests the attack roll for a given AC and attack bonus. It returns 0 for a critical miss, 1 for a hit, and 2 for a critical hit.

### `get_damage(attacks_per_turn, ac, attack_bonus, num_dice, dice_size, modifier, critical_option)`

This function estimates the average damage rate for a given AC and attack bonus, based on the user's input. It uses the `test_attack_roll()` function to test the attack roll, and the `calculate_average_damage()` function to calculate the average damage.

### `get_success_rate(ac, attack_bonus)`

This function estimates the average success rate for a given AC and attack bonus. It uses the `test_attack_roll()` function to test the attack roll.

### `calculate_average_damage(num_dice, dice_size, modifier, critical_option="soft")`

This function calculates the average damage for a given attack description, with an option for critical damage. The `critical_option` parameter can be set to "normal", "full damage", or "soft" (default).

### `get_attack_description(attack_description)`

This function parses the attack description to get the number of dice and the dice size.

### `calculate_estimated_damage()`

This function is called when the user clicks on the "Calculate" button. It gets the input values from the input fields, estimates the damage per turn using the `get_damage()` function, and displays the result in the output field.
