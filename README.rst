Zombsole
========

.. image:: ./demo.gif

Zombsole is a game in which you play **programming** simple bots, which will have 
to survive and fight against hordes of zombies.

The game is **cooperative**: the idea is to find some friends, each one program a 
different bot, and then put the bots to work together against the zombies.

There are three different game types:

* **Extermination**: you must kill all zombies, and at least 1 player must survive.
* **Evacuation**: all players start far away from each other, and must get togheter
  to be evacuated at any place by an helicopter. At least half of the team must
  survive.
* **Safe House**: all players must travel and get inside a single safe house. At 
  least 1 player must reach it, but to win, all the living players must be 
  inside.

And the best of all: is really **simple**.

Getting started
===============

The game isn't packaged for PyPI or anything, it's meant to be a playground, so just
clone the code, install its dependencies, and get inside the ``zombsole`` folder to
start messing around:


.. code-block:: bash

    git clone https://github.com/fisadev/zombsole.git
    cd zombsole
    sudo pip install -r requirements.txt


And now lets just run a simple demo game:


.. code-block:: bash

    ./play.py extermination 50x20 sniper,troll -n 50 -m to_the_closet

Depending on how lucky you are, this could either keep running forever, or quickly
end with a very un-gory massacre of the two players (sniper and troll). If you want
to stop the game, just press ``Ctrl-c``.

The parameters of the ``play.py`` script are very easy to understand, just run 
``./play.py --help``. In the example we just said "run an extermination game in
a world of 50x20 size using the to_the_closet map, with the players sniper and 
troll and a constant population of 50 zombies."


(More detailed docs to come in the following days)
==================================================
