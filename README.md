Oncilla
=======

2d Platformer

TODO
=======
* Some mechanism for blend animations
* Floating point bug, entities vibrate on surfaces
    PinnedBlock(100, 230, 100, 25)
    PlayerBlock(100, 0, 200, 200)
* Weird falling into edge bug

Refactoring
=======
* Commands should live in the entity class, not in the state class
* Modify enum.py to handle assigning specific enum values
    - probably modify enum definition to take a dict, rather than *sequential
