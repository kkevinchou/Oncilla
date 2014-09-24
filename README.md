Oncilla
=======

Animation:

request animation from resource loader
create animation component

render system calls update() on animation component
animation component updates and keeps track of which frame it's on internally
render system calls draw()
sprite is drawn onto the screen

need to implement component message manager for entities
event gets sent to the entity (e.g. "HIT_BY_EXPLOSION", "FROZEN")
entity passes event to each component to handle
 --- rather than iterate through each component, should the entity
     just keep track of which events are relevant and which
     component is interested in those events? (can this be exapnded
     to systems?)

animation component receives the event and knows which animation to play
    (this should probably be something that's configured from a data file)

the data file should convey
    the sprite sheet
    define an animation based on the starting/ending location of an
        animation based off of the sprite sheet
    the entity type / event pair that maps to that sheet
    (in the future - may want to have some scripting to add boolean
    checks for specific states before playing an animation)
    blend animations! (between one animation and another by animation id)

if multiple animation events come in, how do we know which one to play on top of another?
(in the data file, we can include a priority of animations)


GOT STARTED ON ENTITY MESSAGING SYSTEM, WORKED ON JUMP ANIMATION TRIGGERING
