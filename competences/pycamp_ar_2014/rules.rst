Rules
=====

Teams
-----

* Each team must play with 6 bots.
* You may use bots of different classes if you desire but you are not forced
  to.
* The bots can be programmed by groups of people of any size (including 1).

Games and scores
----------------

* Each team will have to play 3 matches of extermination, 3 matches of 
  safehouse and 3 matches of evacuation.
* Each match will grant points to the team if won, and no points if lost. 
* Extermination matches won give you 3 points. Safehouse and evacuation 
  matches won give you 5 points each.
* We will use final alive players on each match and ticks elapsed, to break 
  ties, in that order of precedence.
* Extermination matches will be played in ``fort`` map, with 300 initial 
  zombies and no minimum zombies population to mantain.
* Safehouse matches will be played in ``city_for_safehouse`` map, with no
  initial zombies and a minimum zombies population to mantain of 100.
* Evacuation matches will be played in ``village_for_evacuation`` map, with no
  initial zombies and a minimum zombies population to mantain of 50.
* The commands to run the matches are these:

.. code-block:: bash

    python play.py extermination TEAM_BOTS -z 300 -m fort -i
    python play.py safehouse TEAM_BOTS -n 100 -m city_for_safehouse -i
    python play.py evacuation TEAM_BOTS -n 50 -m village_for_evacuation -i


Other rules
-----------

* Docker isolation will be used to prevent hacks.
* If you need extra dependencies for your bots, ask before! They may be 
  difficult to install inside the isolation container.
* If a match is stuck in an evident infinite loop, or something where an end
  is very unlikely in a timely fashion, the match will be stopped and 
  re-launched. After 3 tries, the match is considered lost.
