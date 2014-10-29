Oncilla
=======

2d Platformer

TODO
=======
* ReaperSystem
* Some mechanism for blend animations

Refactoring
=======
* Commands should live in the entity class, not in the state class

Optimizations
=======
* Could probably cut down on the number of collision checks by only handling one side of the collision,
    then handling the other side of the collision without doing all the redundant calculations
* Rather than have all systems receive all messages, let systems specify which messages they're interested in

Bugs
=======

* Floating point bug, entities vibrate on surfaces
    PinnedBlock(100, 230, 100, 25)
    PlayerBlock(100, 0, 200, 200)
* Weird falling into edge bug
    Jump off a platform and slide against the vertical edge of the platform
* Firing Ice Shard right next to block (work around is to send all messages as 'immediate')
