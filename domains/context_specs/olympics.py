#######################################################
# DOMAIN_VACATION_MANAGEMENT context specs

DOMAIN_DESC = "olympics"

SYSTEM_PROMPT_INSTRUCTIONS = \
    """You are a SQL expert. Given the following SQL tables definitions, generate SQL language to answer the user's question. 

Each user question is about the Olympic Games.
Produce SQL ready for use with a SQLITE database.
Output the result in a JSON format with one key "sql".
Answer the question immediately without preamble.
*important* Strictly follow the rules in the <rule> tags for generating the SQL 

"""

USER_PROMPT = "question: "

ANNOTATED_SQL_DEFINITIONS = \
    """-- The athletes_in_focus is a temporary table that is pre-populated with the exact set of 'id' values for the athletes to be included in any queries about athletes.
CREATE temp TABLE athletes_in_focus (
  id INTEGER PRIMARY KEY,   -- the unique id for each athlete to be included in the query
);

-- The games table holds information on the when and where the games were held
CREATE TABLE games (
  id INTEGER PRIMARY KEY,   -- the unique id for each olympic games
  games_year INTEGER DEFAULT NULL,  -- the year the specific olympic games being described
  games_name TEXT DEFAULT NULL,     -- the name of the specific olympic game (e.g. '1992 Summer')
  season TEXT DEFAULT NULL          -- the season of the olympic game (either 'Summer' or 'Winter')
);

-- The games_city table enables bi-directional relationships between the games and the city where the games were held.
CREATE TABLE games_city (
  games_id INTEGER DEFAULT NULL,    -- the unique id for each olympic games
  city_id INTEGER DEFAULT NULL,     -- the unique id for each city where the games were held
  CONSTRAINT fk_gci_city FOREIGN KEY (city_id) REFERENCES city (id),
  CONSTRAINT fk_gci_gam FOREIGN KEY (games_id) REFERENCES games (id)
);

-- The city table holds the names of cities that have hosted the olympic games
CREATE TABLE city (
  id INTEGER DEFAULT NULL,      -- the unique id the city where the games were held
  city_name TEXT DEFAULT NULL   -- the name of the city
);

-- the games_competitor enables bi-derectional relationships between specific competitors and specific Olympic games.
CREATE TABLE games_competitor (
  id INTEGER PRIMARY KEY,       -- unique id for the record
  games_id INTEGER DEFAULT NULL,    -- the id of the specific olympic game
  person_id INTEGER DEFAULT NULL,   -- the unique id for the athlete)
  age INTEGER DEFAULT NULL,         -- the athlete's age in years at the time of the specific olympic game
  CONSTRAINT fk_gc_gam FOREIGN KEY (games_id) REFERENCES games (id),
  CONSTRAINT fk_gc_per FOREIGN KEY (person_id) REFERENCES athletes_in_focus (id)
);

-- the event tables holds essential information about each event held at the games
CREATE TABLE event (
  id INTEGER PRIMARY KEY, -- the unique id for the event
  sport_id INTEGER DEFAULT NULL,
  event_name TEXT DEFAULT NULL, -- the name of the event
  CONSTRAINT fk_ev_sp FOREIGN KEY (sport_id) REFERENCES sport (id)
);

-- the competitor_event table has the list of athletes for each event and a medal-id for a competitors who won a medal
CREATE TABLE competitor_event (
  event_id INTEGER DEFAULT NULL,
  competitor_id INTEGER DEFAULT NULL,
  medal_id INTEGER DEFAULT NULL,
  CONSTRAINT fk_ce_com FOREIGN KEY (competitor_id) REFERENCES games_competitor (id),
  CONSTRAINT fk_ce_ev FOREIGN KEY (event_id) REFERENCES event (id),
  CONSTRAINT fk_ce_med FOREIGN KEY (medal_id) REFERENCES medal (id)
);

-- The medal table holds the names of cities that have hosted the olympic games
CREATE TABLE medal (
  id INTEGER DEFAULT NULL,      -- the unique id the medal for the event
  medal_name TEXT DEFAULT NULL   -- the name of the medal
);

 -- The athlete_training_locations_tv table holds data on where the athlete does thier training
CREATE TABLE athlete_training_locations_tv (
  competitor_id INTEGER,    -- the unique id for the athlete
  location TEXT DEFAULT NULL   -- the name of the athlete's training location
  CONSTRAINT fk_at_com FOREIGN KEY (competitor_id) REFERENCES games_competitor (id),
);
"""

JOIN_HINTS = """
<rule>
The athletes_in_focus is a temporary table that has been pre-populated with the specific set of 'id' values of the athletes applicable for this query.
</rule>
<rule>
No filters need to be applied to the athletes_in_focus to get the correct set of athlete identifiers for queries  about specific athletes. 
</rule>
<rule> 
Even when the user's question is about specific athletes, these athletes, and only these athletes, are in the athletes_in_focus table
</rule>
<rule>
Only use tables and columns explicitly described with the <SQL> tags
</rule>
"""

TABLE_NAMES = ["athletes_in_focus"]
SQL_PREAMBLE_PT1 = ["""
CREATE temp TABLE athletes_in_focus (
  row_id INTEGER PRIMARY KEY,
  id INTEGER,
  full_name TEXT DEFAULT NULL);
"""]

SQL_PREAMBLE_PT2 = ["""
    CREATE TEMP VIEW athlete_training_locations_tv (competitor_id, location) as
      select ab.ID as 'id', json_tree.value AS 'training_locations' 
      from athlete_background as ab, json_tree(ab.background, '$.training_locations') 
      where json_tree.type NOT IN ('object','array');
    """]

FEW_SHOT_EXAMPLES = \
    """<example>
question: What is the last games that the is in the database
answer:
```{"sql": "SELECT id, games_name, games_year, max(games_year) FROM games"
}
```
</example>

<example>
question: Which games did Rudolf Krpti compete?
answer:
```{"sql": "SELECT g.games_name, g.games_year 
FROM athletes_in_focus a
JOIN games_competitor gc ON gc.person_id = a.id
JOIN games g ON gc.games_id = g.id;" 
}
```
</example>

<example>
question: How many gold medals has Yukio Endo won?
answer:
```{"sql": "SELECT a.id, count(m.medal_name) as "count"
FROM athletes_in_focus a
INNER JOIN games_competitor gc ON gc.person_id = a.id
INNER JOIN competitor_event ce ON gc.id = ce.competitor_id
INNER JOIN medal m ON ce.medal_id = m.id
WHERE m.medal_name = 'Gold' 
GROUP BY a.id;"
}
```
</example>

<example>
question: Which events has Chris Hoy taken part in?
answer:
```{"sql": "SELECT distinct a.id, e.event_name
FROM athletes_in_focus a
INNER JOIN games_competitor gc ON a.id = gc.person_id
INNER JOIN competitor_event ce ON gc.id = ce.competitor_id
INNER JOIN event e ON ce.event_id = e.id;"
}
```
</example>

<example>
question: Which games did Tams Darnyi, Viktor An and Kathrin Boron compete?
answer:
```{"sql": "SELECT g.games_name, g.games_year 
FROM athletes_in_focus a
JOIN games_competitor gc ON gc.person_id = a.id
JOIN games g ON gc.games_id = g.id;"
}
```
</example>

<example>
question: How many gold medals have Danuta Kozk and Michael Johnson won?
answer:
```{"sql": "SELECT a.id, count(m.medal_name) as "count"
FROM athletes_in_focus a
INNER JOIN games_competitor gc ON gc.person_id = a.id
INNER JOIN competitor_event ce ON gc.id = ce.competitor_id
INNER JOIN medal m ON ce.medal_id = m.id
WHERE m.medal_name = 'Gold' 
GROUP BY a.id;"
}
```
</example>

<example>
question: Which events has Sawao Kato, Reiner Klimke, Janica Kosteli and Danuta Kozk taken part in?
answer:
```{"sql": "SELECT distinct a.id, e.event_name
FROM athletes_in_focus a
INNER JOIN games_competitor gc ON a.id = gc.person_id
INNER JOIN competitor_event ce ON gc.id = ce.competitor_id
INNER JOIN event e ON ce.event_id = e.id;"
}
```
</example>

<example>
question: Where does Danuta Kozk do his training for the games?
answer:
```{"sql": "SELECT atl.competitor_id, atl.location
FROM athletes_in_focus a
JOIN athlete_training_locations_tv atl ON a.id = atl.competitor_id;"
}
```
</example>
"""

SYSTEM_PROMPT = \
    SYSTEM_PROMPT_INSTRUCTIONS + JOIN_HINTS + "\n<SQL>\n" + \
    ANNOTATED_SQL_DEFINITIONS + "</SQL>\n" + \
    FEW_SHOT_EXAMPLES
