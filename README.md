You need to provide 2 environment variables 
TOKEN and BASE_URL to be able to work with the project.

The project is not yet in stable state and far to be finished, it does not yet have a CLI.
Currently you must directly use the classes.

samples : 

```py
from character.character import Character
armion = Character('Armion')
armion.display_character(verbose = True)
armion.move(7, 6)
armion.farm_monster('flying_serpent')
```
