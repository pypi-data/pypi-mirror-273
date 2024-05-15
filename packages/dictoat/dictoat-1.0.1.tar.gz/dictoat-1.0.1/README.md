# Dictoat

Dictoat is a Python utility designed to simplify accessing data stored in dictionaries. It converts dictionaries into Python objects, allowing for more intuitive access to data via attributes instead of dictionary keys. This is ideal for projects where readability and ease of access to complex data structures are essential.

## Installation

You can easily install `Dictoat` using pip:

```bash
pip install dictoat
```
or via git:

```bash
git clone https://github.com/niCodeLine/dictoat.git
```
or just copy-paste it into your code.
## Usage

To use Dictoat, simply import the `Dictoat` class in your Python project and pass a dictionary as an argument. For example:

```python
from dictoat import Dictoat

# Example of using Dictoat
apple_dict = {"flavor": "sweet", "colors": ["red", "green"],"dimentions": {"weigh": 185, "radius": 5}}
apple = Dictoat(apple_dict)

# Accessing the data
print(apple.flavor_)
print(apple.dimentions_.radius_)
print(apple.colors_)
```

The output would show:
```markdown
sweet
5
["red", "green"]
```

Or a more complete example:

```python
from dictoat import Dictoat

pokedex_dict = {
    "total_pokemons": 2,
    "region": "Kanto",
    "Pokemons": {
        "Pikachu": {
            "type": "Electric",
            "abilities": ["Static", "Lightning Rod"],
            "stats": {
                "hp": 35,
                "attack": 55,
                "defense": 40
            }
        },
        "Squirtle": {
            "type": "Water",
            "abilities": ["Torrent", "Rain Dish"],
            "stats": {
                "hp": 44,
                "attack": 48,
                "defense": 65
            },
            "evolutions": ["Wartortle", "Blastoise"]
        }
    }
}

pokedex = Dictoat(pokedex_dict)

# Accessing the data
print("Total Pokémon in Pokedex:", pokedex.total_pokemons_)
print("Pokedex Region:", pokedex.region_)

print("Pikachu Type:", pokedex.Pokemons_.Pikachu_.type_)
print("Pikachu Abilities:", pokedex.Pokemons_.Pikachu_.abilities_)
print("Pikachu HP:", pokedex.Pokemons_.Pikachu_.stats_.hp_)

print("Squirtle Type:", pokedex.Pokemons_.Squirtle_.type_)
print("Squirtle Abilities:", pokedex.Pokemons_.Squirtle_.abilities_)
print("Squirtle Defense:", pokedex.Pokemons_.Squirtle_.stats_.defense_)
print("Squirtle Evolutions:", pokedex.Pokemons_.Squirtle_.evolutions_)
```

With its output being:

```markdown
Total Pokémon in Pokedex: 2
Pokedex Region: Kanto

Pikachu Type: Electric
Pikachu Abilities: ['Static', 'Lightning Rod']
Pikachu HP: 35

Squirtle Type: Water
Squirtle Abilities: ['Torrent', 'Rain Dish']
Squirtle Defense: 65
Squirtle Evolutions: ['Wartortle', 'Blastoise']
```

## Features

- **Simple Conversion**: Converts any dictionary into an object for easier access.
- **Deep Nesting Support**: Supports nested dictionaries, creating sub-objects for each level.

## Contributions

Contributions are welcome! If you have improvements or fixes, please send a pull request or open an issue in the GitHub repository.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

Nico Spok - nicospok@hotmail.com
GitHub: niCodeLine
