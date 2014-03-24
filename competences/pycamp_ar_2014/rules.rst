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

Results
=======

+--------------------+----------------+--------+------------+-------+
| Team               | Match rules    | Result | Survivors  | Ticks |
+====================+================+========+============+=======+
| Lucio              | extermination  | WIN    | 6          | 375   |
| (futurologist.py,  |                +--------+------------+-------+
| evacuation.map)    |                | WIN    | 6          | 385   |
|                    |                +--------+------------+-------+
|                    |                | WIN    | 6          | 392   |
|                    +----------------+--------+------------+-------+
|                    | safehouse      | LOST   |            | 337   |
|                    |                +--------+------------+-------+
|                    |                | LOST   |            | 319   |
|                    |                +--------+------------+-------+
|                    |                | LOST   |            | 303   |
|                    +----------------+--------+------------+-------+
|                    | evacuation     | WIN    | 4          | 270   |
|                    |                +--------+------------+-------+
|                    |                | WIN    | 4          | 449   |
|                    |                +--------+------------+-------+
|                    |                | WIN    | 5          | 345   |
+--------------------+----------------+--------+------------+-------+
| Team Famaf         | extermination  | LOST   |            | 781   |
| (teamfamaf.py)     |                +--------+------------+-------+
|                    |                | LOST   |            | 166   |
|                    |                +--------+------------+-------+
|                    |                | LOST   |            | 215   |
|                    +----------------+--------+------------+-------+
|                    | safehouse      | LOST   |            | 258   |
|                    |                +--------+------------+-------+
|                    |                | WIN    | 1          | 336   |
|                    |                +--------+------------+-------+
|                    |                | LOST   |            | 339   |
|                    +----------------+--------+------------+-------+
|                    | evacuation     | WIN    | 6          | 324   |
|                    |                +--------+------------+-------+
|                    |                | WIN    | 3          | 261   |
|                    |                +--------+------------+-------+
|                    |                | WIN    | 3          | 194   |
+--------------------+----------------+--------+------------+-------+
| Mati y Nico        | extermination  | WIN    | 6          | 179   |
| (perrito2.py,      |                +--------+------------+-------+
| minions.py)        |                | WIN    | 6          | 195   |
|                    |                +--------+------------+-------+
|                    |                | WIN    | 6          | 160   |
|                    +----------------+--------+------------+-------+
|                    | safehouse      | LOST (timeout)              |
|                    |                +--------+------------+-------+
|                    |                | LOST (timeout)              |
|                    |                +--------+------------+-------+
|                    |                | LOST (timeout)              |
|                    +----------------+--------+------------+-------+
|                    | evacuation     | WIN    | 3          | 27    |
|                    |                +--------+------------+-------+
|                    |                | WIN    | 3          | 23    |
|                    |                +--------+------------+-------+
|                    |                | LOST   |            | 41    |
+--------------------+----------------+--------+------------+-------+

Final scores
------------

* Lucio: 24
* Team famaf: 20
* Mati y Nico: 19
