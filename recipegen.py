"""
recipegen.py - Recipe generator using a genetic algorithm.

Jack Beckitt-Marshall, Kevin Li and Yvonne Fang - CSCI 3725 - PQ1
14 September 2019
"""
import random
import argparse
import glob
import os
import shutil
import parse # Parsing library defined by parse.py (found on GitHub), allows us to parse using
             # format strings.


class Recipe:
    """
    This class defines a recipe: all in all, it is really just a simple dictionary consisting of
    pairs of {Ingredient: Amount} classes.
    """
    def __init__(self, recipe_dict=None):
        """
        Initialises a new recipe - this time utilizing an empty dictionary or recipe_dict if this is
        passed to it.

        Keyword arguments:
        recipe_dict -- Dictionary that we pass containing pairs of Ingredient: Amount objects to
        create a new recipe object.
        """
        if not recipe_dict:
            self.recipe_dict = dict()
        else:
            self.recipe_dict = recipe_dict


    def add_ingredient(self, ingredient, amount):
        """
        This function is pretty self-explanatory - we're just adding a new ingredient and amount
        to our list of ingredients.

        Keyword arguments:
        ingredient -- Ingredient to add.
        amount -- Amount of that ingredient to add.
        """
        for key, value in self.recipe_dict.items():
            if str(key) == str(ingredient):
                del self.recipe_dict[key]
                break

        self.recipe_dict[ingredient] = amount

    def remove_ingredient(self, ingredient):
        """
        This function is again pretty self-explanatory - we're just removing an ingredient
        from our list of ingredients.

        Keyword arguments:
        ingredient -- Ingredient to remove.
        """

        for key, value in self.recipe_dict.items():
            if str(key) == str(ingredient):
                del self.recipe_dict[key]
                break

    def change_ingredient_name(self, old_name, new_name):
        """
        This function is again pretty self-explanatory - we're just changing the name of an
        ingredient in our list of ingredients.

        Keyword arguments:
        ingredient -- Ingredient to remove.
        """
        old_amount = self.get_ingredient_amount(old_name)
        if old_amount:
            self.remove_ingredient(old_name)
            self.add_ingredient(new_name, old_amount)
        else:
            print("Error: old ingredient not found in the recipe.")

    def split_recipe(self):
        """
        This function splits the recipe into two "sub-recipes" using a random pivot. It returns two
        recipes as a tuple.
        """
        # Find a random pivot to split the ingredients list with, from 0 to the length of the list.
        pivot = random.randint(1, len(self.recipe_dict)-1) # Ensures we don't get empty sublists.

        left_sublist = list(self.recipe_dict.items())[0:pivot]
        right_sublist = list(self.recipe_dict.items())[pivot:len(self.recipe_dict)]
        return Recipe(recipe_dict=dict(left_sublist)), Recipe(recipe_dict=dict(right_sublist))

    def get_ingredient_tuples(self):
        """
        Gets us all of the tuples of ingredients and their amounts.
        """
        return self.recipe_dict.items()

    def get_ingredient_amount(self, ingredient):
        """
        Given an ingredient, returns the amount associated with that ingredient. if ingredient
        does not exist, return None.

        Keyword arguments:
        ingredient -- The ingredient for which we want to retrieve the amount.
        """
        for key, value in self.recipe_dict.items():
            if str(key) == str(ingredient):
                return value
        return None

    def fitness_level(self):
        """
        This function represents the fitness of the recipe. The fitness of the recipe is
        represented by the degree of ingredient diversity.
        """
        return len(self.recipe_dict)

    def combine_with_other(self, other_recipe):
        """
        This function will combine the recipe with another recipe given as an argument, adding
        ingredient amounts if necessary.

        Keyword arguments:
        other_recipe -- The other recipe to combine with this one.
        """
        for ingredient, amount in other_recipe.get_recipe_dict().items():
            existing_amount = self.get_ingredient_amount(ingredient)
            if existing_amount:
                self.remove_ingredient(ingredient)
                self.add_ingredient(ingredient, existing_amount + amount)
            else:
                self.add_ingredient(ingredient, amount)


    def get_recipe_dict(self):
        """
        Returns dictionary representation of the recipe.
        """
        return self.recipe_dict

    def normalization(self):
        """
        Normalises the recipe so that all amounts add up to 100 ounces.
        """
        # If the recipe is not empty.
        # Converting "magic numbers" to Amounts because we are performing operations on Amount
        # objects.
        if self.recipe_dict:
            total_amount = Amount(0)
            for ingredient, amount in self.get_recipe_dict().items():
                total_amount += amount

            if total_amount.get_num() != 100:
                coefficient = Amount(100)/total_amount
                for ingredient, amount in self.recipe_dict.items():
                    self.recipe_dict[ingredient] = amount * coefficient

    def __str__(self):
        """
        Returns string representation of the recipe.
        """
        output = ""
        if not self.recipe_dict:
            return "Blank recipe"
        else:
            for ingredient, amount in self.recipe_dict.items():
                output += "{0} {1}\n".format(str(amount), str(ingredient))
            return output

    def __repr__(self):
        """
        Returns the "official" string representation of the recipe.
        """
        output = ""
        for ingredient, amount in self.recipe_dict.items():
            output += "({0}: {1}),".format(repr(amount), repr(ingredient))
        return "Recipe({0})".format(output)


class Ingredient:
    """
    Ingredient class - again, this is a simple wrapper around a string.
    """

    def __init__(self, ingredient_name):
        """
        Initialises a recipe based upon a given ingredient name.
        """
        self.ingredient_name = ingredient_name

    def __str__(self):
        """
        Returns a string representation of the ingredient name - i.e. gets the ingredient name
        """
        return str(self.ingredient_name)

    def __repr__(self):
        """
        Returns a string representation that can be used to create a new instance of the Ingredient
        class.
        """
        return "Ingredient({0})".format(self.ingredient_name)

class Amount:
    """
    Amount class - again, this is a simple wrapper around a integer.
    """

    def __init__(self, amount):
        """
        Initialises a amount based upon a given amount (as an integer)
        """
        self.amount = float(amount)

    def get_num(self):
        """
        Gets the integer of the amount
        """
        return self.amount

    def __str__(self):
        """
        Returns a string representation of the ingredient name - i.e. gets the ingredient name
        """
        return str(self.amount) + " oz"

    def __repr__(self):
        """
        Returns a string representation that can be used to create a new instance of the Ingredient
        class.
        """
        return "Amount({0})".format(self.amount)

    def __add__(self, amount):
        """
        Overrides addition so that we can do simple math on amounts.

        Keyword arguments:
        amount -- The amount to use in operation.
        """
        return Amount(self.get_num() + amount.get_num())

    def __sub__(self, amount):
        """
        Overrides subtraction so that we can do simple math on amounts.

        Keyword arguments:
        amount -- The amount to use in operation.
        """
        return Amount(self.get_num() - amount.get_num())

    def __mul__(self, amount):
        """
        Overrides multiplication so that we can do simple math on amounts.

        Keyword arguments:
        amount -- The amount to use in operation.
        """
        return Amount(self.get_num() * amount.get_num())

    def __truediv__(self, amount):
        """
        Overrides division so that we can do simple math on amounts.

        Keyword arguments:
        amount -- The amount to use in operation.
        """
        return Amount(self.get_num() / amount.get_num())

def select_recipe_pairs(recipe_list):
    """
    For each recipe in the original recipe list, we select two recipes with probablity proportional
    to their fitness for genetic crossover.

    Keyword arguments:
    recipe_list -- List of recipes to use.
    """
    original_recipe_list_fitness = []
    sum_of_original_fitnesses = 0
    for recipe in recipe_list:
        original_recipe_list_fitness.append((recipe, recipe.fitness_level()))
        sum_of_original_fitnesses += recipe.fitness_level()

    recipe_pairs = []

    # Picks two recipes, ensuring we don't pick same recipe twice.
    while len(recipe_pairs) < len(recipe_list):
        recipe1 = None
        recipe2 = None
        while not recipe1 or not recipe2 or recipe1 is recipe2:

            pick1 = random.randint(0, sum_of_original_fitnesses)
            pick2 = random.randint(0, sum_of_original_fitnesses)

            current = 0

            for recipe, fitness in original_recipe_list_fitness:
                current += fitness
                if current > pick1:
                    recipe1 = recipe
                    break

            current = 0

            for recipe, fitness in original_recipe_list_fitness:
                current += fitness
                if current > pick2:
                    recipe2 = recipe
                    break

        recipe_pairs.append((recipe1, recipe2))

    return recipe_pairs

def natural_selection(offspring_list):
    """
    This function takes in the list of potential offspring and selects the fittest 50% for
    the next generation of recipes. This function returns the selected offspring as a list

    Keyword arguments:
    offspring-list -- The list of offspring to select from
    """
    offspring_fitness = []
    selected_offspring = []
    for recipe in offspring_list:
        recipe_fitness = recipe.fitness_level()
        offspring_fitness.append((recipe, recipe_fitness))
    sorted_fitness = sorted(offspring_fitness, key=lambda x: x[1])
    selected_offspring = sorted_fitness[int(len(offspring_fitness)/2):]
    return selected_offspring

def genetic_iteration(recipe_list, inspiring_set):
    """
    Performs an iteration of our genetic algorithm (simpler version of PIERRE). Returns next
    generation of recipes based upon 50% highest fitness of the previous generation and the top 50%
    of the newly generated recipes.

    Keyword arguments:
    recipe_list -- List of recipes that we would carry out the iteration on.
    """
    # Step 1: Generate a number of new recipes equal to the number of recipes in the population
    # For each new recipe, select two recipes with probability proportional to their fitness for
    # genetic crossover
    recipe_pairs = select_recipe_pairs(recipe_list)

    new_recipes = []
    # Step 2: Crossover
    for recipe1, recipe2 in recipe_pairs:
        new_recipe = recipe1.split_recipe()[0]
        combine_recipe = recipe2.split_recipe()[1]
        new_recipe.combine_with_other(combine_recipe)
        new_recipes.append(new_recipe)
    # Step 3:
    for recipe in new_recipes:
        mutation = random.random()
        if mutation > 0.5: # 50/50 chance of a mutation occurring.
            mutation_choice = random.randint(0, 3)
            if mutation_choice == 0:
                # Change of ingredient amount
                random_ingredient_amount = random.uniform(0, 100)
                random_choice = random.choice(list(recipe.get_recipe_dict().keys()))
                recipe.remove_ingredient(random_choice)
                recipe.add_ingredient(random_choice, Amount(random_ingredient_amount))
            elif mutation_choice == 1:
                # Change of one ingredient to another from our inspiring set.
                recipe.change_ingredient_name(random.choice(list(recipe.get_recipe_dict().keys())),
                                              random.choice(inspiring_set)[0])

            elif mutation_choice == 2:
                # Add an ingredient uniformly at random from the inspiring set and add it to the
                # recipe.
                random_choice = random.choice(inspiring_set)
                recipe.add_ingredient(random_choice[0], random_choice[1])
            elif mutation_choice == 3:
                # Delete an ingredient at random from the recipe.
                if recipe.get_recipe_dict(): # If the recipe isn't empty.
                    recipe.remove_ingredient(random.choice(list(recipe.get_recipe_dict().keys())))
        # Re-normalise all evolved recipes.
        recipe.normalization()

    # Return list consisting of top 50% of original recipes and top 50% of new recipes, and strip
    # their fitness levels away from them.
    return [pair[0] for pair in natural_selection(recipe_list)] + \
        [pair[0] for pair in natural_selection(new_recipes)]

def main():
    """
    Main function - loads recipe files and runs iterations of the genetic algorithm.
    """

    # Start off by parsing arguments from the command line.
    parser = argparse.ArgumentParser(description="Genetic algorithm-based recipe maker!")
    parser.add_argument("recipe_directory", type=str, help="Directory where recipes are stored.")
    parser.add_argument("iterations", type=int, help="Number of iterations to run.")

    args = parser.parse_args()

    # Load all of the recipes from the directory to create both our inspiring set and lists of each
    # recipe.
    recipes_list = []
    inspiring_set = []
    for filename in glob.glob(args.recipe_directory + "/*.txt"):
        with open(filename, 'r') as file:
            recipe = Recipe()
            file_lines = file.readlines()
            for file_line in file_lines:
                parsed = parse.parse("{0} oz {1}", file_line)
                recipe.add_ingredient(Ingredient(parsed[1]), Amount(float(parsed[0])))
                inspiring_set.append((Ingredient(parsed[1]), Amount(float(parsed[0]))))

        recipes_list.append(recipe)
    # Remove existing iterations directory if it exists.
    if os.path.exists("iterations"):
        shutil.rmtree("iterations")
    os.mkdir("iterations")

    for i in range(0, args.iterations):
        print("Running iteration {0}!".format(i+1))
        recipes_list = genetic_iteration(recipes_list, inspiring_set)
        os.mkdir("iterations/{0}".format(i))
        used_filenames = []
        count = 0
        for recipe in recipes_list:
            recipe_string = str(recipe)
            recipe_sorted = sorted(recipe.get_ingredient_tuples(), key=lambda x: x[1].get_num(),
                                   reverse=True)
            dish_names = ["soup", "broth", "stew", "ramen"]
            chef_names = ["Gordon Ramsay's ", "Salt Bae's ", "Bowdoin's ", "Thorne's ",
                            "Moulton's "]

            filename = "{0} star {1} and {2} {3}".format(i+1, recipe_sorted[0][0],
                                                         recipe_sorted[1][0],
                                                         random.choice(dish_names))
            # If the filename is used already, add a chef's name to the front of it!
            if filename in used_filenames:
                filename = random.choice(chef_names) + filename
            used_filenames.append(filename)
            with open("iterations/{0}/{1}".format(i, filename), "w") as file:
                file.write(recipe_string)
            count += 1

if __name__ == "__main__":
    main()
