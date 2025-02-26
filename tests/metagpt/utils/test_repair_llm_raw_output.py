#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Desc   : unittest of repair_llm_raw_output

from metagpt.config2 import config

"""
CONFIG.repair_llm_output should be True before retry_parse_json_text imported.
so we move `from ... impot ...` into each `test_xx` to avoid `Module level import not at top of file` format warning.
"""
config.repair_llm_output = True


def test_repair_case_sensitivity():
    from metagpt.utils.repair_llm_raw_output import repair_llm_raw_output

    raw_output = """{
    "Original requirements": "Write a 2048 game",
    "search Information": "",
    "competitive Quadrant charT": "quadrantChart
                Campaign A: [0.3, 0.6]",
    "requirement analysis": "The 2048 game should be simple to play"
}"""
    target_output = """{
    "Original Requirements": "Write a 2048 game",
    "Search Information": "",
    "Competitive Quadrant Chart": "quadrantChart
                Campaign A: [0.3, 0.6]",
    "Requirement Analysis": "The 2048 game should be simple to play"
}"""
    req_keys = ["Original Requirements", "Search Information", "Competitive Quadrant Chart", "Requirement Analysis"]
    output = repair_llm_raw_output(output=raw_output, req_keys=req_keys)
    assert output == target_output


def test_repair_special_character_missing():
    from metagpt.utils.repair_llm_raw_output import repair_llm_raw_output

    raw_output = """[CONTENT]
    "Anything UNCLEAR": "No unclear requirements or information."
[CONTENT]"""

    target_output = """[CONTENT]
    "Anything UNCLEAR": "No unclear requirements or information."
[/CONTENT]"""
    req_keys = ["[/CONTENT]"]
    output = repair_llm_raw_output(output=raw_output, req_keys=req_keys)
    assert output == target_output

    raw_output = """[CONTENT] tag
[CONTENT]
{
"Anything UNCLEAR": "No unclear requirements or information."
}
[CONTENT]"""
    target_output = """[CONTENT] tag
[CONTENT]
{
"Anything UNCLEAR": "No unclear requirements or information."
}
[/CONTENT]"""
    output = repair_llm_raw_output(output=raw_output, req_keys=req_keys)
    assert output == target_output

    raw_output = '[CONTENT] {"a": "b"} [CONTENT]'
    target_output = '[CONTENT] {"a": "b"} [/CONTENT]'

    output = repair_llm_raw_output(output=raw_output, req_keys=["[/CONTENT]"])
    assert output == target_output


def test_required_key_pair_missing():
    from metagpt.utils.repair_llm_raw_output import repair_llm_raw_output

    raw_output = '[CONTENT] {"a": "b"}'
    target_output = '[CONTENT] {"a": "b"}\n[/CONTENT]'

    output = repair_llm_raw_output(output=raw_output, req_keys=["[/CONTENT]"])
    assert output == target_output

    raw_output = """[CONTENT]
{
    "key": "value"
]"""
    target_output = """[CONTENT]
{
    "key": "value"
]
[/CONTENT]"""

    output = repair_llm_raw_output(output=raw_output, req_keys=["[/CONTENT]"])
    assert output == target_output

    raw_output = """[CONTENT] tag
[CONTENT]
{
    "key": "value"
}
xxx
"""
    target_output = """[CONTENT]
{
    "key": "value"
}
[/CONTENT]"""
    output = repair_llm_raw_output(output=raw_output, req_keys=["[/CONTENT]"])
    assert output == target_output


def test_repair_json_format():
    from metagpt.utils.repair_llm_raw_output import RepairType, repair_llm_raw_output

    raw_output = "{ xxx }]"
    target_output = "{ xxx }"

    output = repair_llm_raw_output(output=raw_output, req_keys=[None], repair_type=RepairType.JSON)
    assert output == target_output

    raw_output = "[{ xxx }"
    target_output = "{ xxx }"

    output = repair_llm_raw_output(output=raw_output, req_keys=[None], repair_type=RepairType.JSON)
    assert output == target_output

    raw_output = "{ xxx ]"
    target_output = "{ xxx }"

    output = repair_llm_raw_output(output=raw_output, req_keys=[None], repair_type=RepairType.JSON)
    assert output == target_output

    raw_output = """
{
    "Language": "en_us",  # define language
    "Programming Language": "Python"
}
"""
    target_output = """{
    "Language": "en_us",
    "Programming Language": "Python"
}"""
    output = repair_llm_raw_output(output=raw_output, req_keys=[None], repair_type=RepairType.JSON)
    assert output == target_output

    raw_output = """
{
    "Language": "en_us",  // define language
    "Programming Language": "Python" # define code language
}
"""
    target_output = """{
    "Language": "en_us",
    "Programming Language": "Python"
}"""
    output = repair_llm_raw_output(output=raw_output, req_keys=[None], repair_type=RepairType.JSON)
    assert output == target_output

    raw_output = """
    {
        "Language": "#en_us#",  // define language
        "Programming Language": "//Python # Code // Language//" # define code language
    }
    """
    target_output = """{
        "Language": "#en_us#",
        "Programming Language": "//Python # Code // Language//"
    }"""
    output = repair_llm_raw_output(output=raw_output, req_keys=[None], repair_type=RepairType.JSON)
    assert output == target_output


def test_repair_invalid_json():
    from metagpt.utils.repair_llm_raw_output import repair_invalid_json

    raw_output = """{
    "key": "value"
    },
}"""
    target_output = """{
    "key": "value"
,
}"""
    output = repair_invalid_json(raw_output, "Expecting ',' delimiter: line 3 column 1")
    assert output == target_output

    raw_output = """{
    "key": "
value
    },
}"""
    target_output = """{
    "key": "
value
",
}"""
    output = repair_invalid_json(raw_output, "Expecting ',' delimiter: line 4 column 1")
    output = repair_invalid_json(output, "Expecting ',' delimiter: line 4 column 1")
    assert output == target_output

    raw_output = """{
    "key": '
value
    },
}"""
    target_output = """{
    "key": '
value
',
}"""
    output = repair_invalid_json(raw_output, "Expecting ',' delimiter: line 4 column 1")
    output = repair_invalid_json(output, "Expecting ',' delimiter: line 4 column 1")
    output = repair_invalid_json(output, "Expecting ',' delimiter: line 4 column 1")
    assert output == target_output

    raw_output = '{"key": "url "http" \\"https\\" "}'
    target_output = '{"key": "url \\"http\\" \\"https\\" "}'
    output = repair_invalid_json(raw_output, "Expecting ',' delimiter: line 1 column 15 (char 14)")
    assert output == target_output


def test_retry_parse_json_text():
    from metagpt.utils.repair_llm_raw_output import retry_parse_json_text

    invalid_json_text = """{
"Original Requirements": "Create a 2048 game",
"Competitive Quadrant Chart": "quadrantChart\n\ttitle Reach and engagement of campaigns\n\t\tx-axis"
],
"Requirement Analysis": "The requirements are clear and well-defined"
}"""
    target_json = {
        "Original Requirements": "Create a 2048 game",
        "Competitive Quadrant Chart": "quadrantChart\n\ttitle Reach and engagement of campaigns\n\t\tx-axis",
        "Requirement Analysis": "The requirements are clear and well-defined",
    }
    output = retry_parse_json_text(output=invalid_json_text)
    assert output == target_json

    invalid_json_text = """{
"Original Requirements": "Create a 2048 game",
"Competitive Quadrant Chart": "quadrantChart\n\ttitle Reach and engagement of campaigns\n\t\tx-axis"
},
"Requirement Analysis": "The requirements are clear and well-defined"
}"""
    target_json = {
        "Original Requirements": "Create a 2048 game",
        "Competitive Quadrant Chart": "quadrantChart\n\ttitle Reach and engagement of campaigns\n\t\tx-axis",
        "Requirement Analysis": "The requirements are clear and well-defined",
    }
    output = retry_parse_json_text(output=invalid_json_text)
    assert output == target_json

    invalid_json_text = '''{
    "Data structures and interfaces": """
    class UI:
        - game_engine: GameEngine
        + __init__(engine: GameEngine) -> None
        + display_board() -> None
        + display_score() -> None
        + prompt_move() -> str
        + reset_game() -> None
    """
    "Anything UNCLEAR": "no"
}'''
    target_json = {
        "Data structures and interfaces": "\n    class UI:\n        - game_engine: GameEngine\n        + __init__(engine: GameEngine) -> None\n        + display_board() -> None\n        + display_score() -> None\n        + prompt_move() -> str\n        + reset_game() -> None\n    ",
        "Anything UNCLEAR": "no",
    }
    output = retry_parse_json_text(output=invalid_json_text)
    assert output == target_json


def test_extract_content_from_output():
    """
    cases
        xxx [CONTENT] xxxx [/CONTENT]
        xxx [CONTENT] xxx [CONTENT] xxxx [/CONTENT]
        xxx [CONTENT] xxxx [/CONTENT] xxx [CONTENT][/CONTENT] xxx [CONTENT][/CONTENT]   # target pair is the last one
    """
    from metagpt.utils.repair_llm_raw_output import extract_content_from_output

    output = (
        'Sure! Here is the properly formatted JSON output based on the given context:\n\n[CONTENT]\n{\n"'
        'Required Python third-party packages": [\n"pygame==2.0.4",\n"pytest"\n],\n"Required Other language '
        'third-party packages": [\n"No third-party packages are required."\n],\n"Full API spec": "\nopenapi: '
        "3.0.0\n\ndescription: A JSON object representing the game state.\n\npaths:\n game:\n   get:\n     "
        "summary: Get the current game state.\n     responses:\n       200:\n         description: Game state."
        "\n\n moves:\n   post:\n     summary: Make a move.\n     requestBody:\n       description: Move to be "
        "made.\n       content:\n         applicationjson:\n           schema:\n             type: object\n "
        "            properties:\n               x:\n                 type: integer\n               y:\n     "
        "            type: integer\n               tile:\n                 type: object\n                 "
        "properties:\n                   value:\n                     type: integer\n                   x:\n   "
        "                  type: integer\n                   y:\n                     type: integer\n\n "
        "undo-move:\n   post:\n     summary: Undo the last move.\n     responses:\n       200:\n       "
        "  description: Undone move.\n\n end-game:\n   post:\n     summary: End the game.\n     responses:\n  "
        "     200:\n         description: Game ended.\n\n start-game:\n   post:\n     summary: Start a new "
        "game.\n     responses:\n       200:\n         description: Game started.\n\n game-over:\n   get:\n  "
        "   summary: Check if the game is over.\n     responses:\n       200:\n         description: Game "
        "over.\n       404:\n         description: Game not over.\n\n score:\n   get:\n     summary: Get the "
        "current score.\n     responses:\n       200:\n         description: Score.\n\n tile:\n   get:\n     "
        "summary: Get a specific tile.\n     parameters:\n       tile_id:\n         type: integer\n         "
        "description: ID of the tile to get.\n     responses:\n       200:\n         description: Tile.\n\n "
        "tiles:\n   get:\n     summary: Get all tiles.\n     responses:\n       200:\n         description: "
        "Tiles.\n\n level:\n   get:\n     summary: Get the current level.\n     responses:\n       200:\n     "
        "    description: Level.\n\n level-up:\n   post:\n     summary: Level up.\n     responses:\n       "
        "200:\n         description: Level up successful.\n\n level-down:\n   post:\n     summary: Level "
        "down.\n     responses:\n       200:\n         description: Level down successful.\n\n  restart:\n   "
        "post:\n     summary: Restart the game.\n     responses:\n       200:\n         description: Game "
        "restarted.\n\n help:\n   get:\n     summary: Get help.\n     responses:\n       200:\n         "
        "description: Help.\n\n version:\n   get:\n     summary: Get the version of the game.\n     "
        'responses:\n       200:\n         description: Version.\n\n}\n\n"Logic Analysis": [\n"game.py",'
        '\n"Contains the game logic."\n],\n"Task list": [\n"game.py",\n"Contains the game logic and should be '
        'done first."\n],\n"Shared Knowledge": "\n\'game.py\' contains the game logic.\n",\n"Anything '
        'UNCLEAR": "How to start the game."\n]\n\n[/CONTENT]  Great! Your JSON output is properly formatted '
        "and correctly includes all the required sections. Here's a breakdown of what each section "
        "contains:\n\nRequired Python third-party packages:\n\n* pygame==2.0.4\n* pytest\n\nRequired Other "
        "language third-party packages:\n\n* No third-party packages are required.\n\nFull API spec:\n\n* "
        "openapi: 3.0.0\n* description: A JSON object representing the game state.\n* paths:\n  + game: "
        "Get the current game state.\n  + moves: Make a move.\n  + undo-move: Undo the last move.\n  + "
        "end-game: End the game.\n  + start-game: Start a new game.\n  + game-over: Check if the game is "
        "over.\n  + score: Get the current score.\n  + tile: Get a specific tile.\n  + tiles: Get all tiles.\n  "
        "+ level: Get the current level.\n  + level-up: Level up.\n  + level-down: Level down.\n  + restart: "
        "Restart the game.\n  + help: Get help.\n  + version: Get the version of the game.\n\nLogic "
        "Analysis:\n\n* game.py contains the game logic.\n\nTask list:\n\n* game.py contains the game logic "
        "and should be done first.\n\nShared Knowledge:\n\n* 'game.py' contains the game logic.\n\nAnything "
        "UNCLEAR:\n\n* How to start the game.\n\nGreat job! This JSON output should provide a clear and "
        "comprehensive overview of the project's requirements and dependencies."
    )
    output = extract_content_from_output(output)
    assert output.startswith('{\n"Required Python third-party packages') and output.endswith(
        'UNCLEAR": "How to start the game."\n]'
    )

    output = (
        "Sure, I would be happy to help! Here is the information you provided, formatted as a JSON object "
        'inside the [CONTENT] tag:\n\n[CONTENT]\n{\n"Original Requirements": "Create a 2048 game",\n"Search '
        'Information": "Search results for 2048 game",\n"Requirements": [\n"Create a game with the same rules '
        'as the original 2048 game",\n"Implement a user interface that is easy to use and understand",\n"Add a '
        'scoreboard to track the player progress",\n"Allow the player to undo and redo moves",\n"Implement a '
        'game over screen to display the final score"\n],\n"Product Goals": [\n"Create a fun and engaging game '
        'experience for the player",\n"Design a user interface that is visually appealing and easy to use",\n"'
        'Optimize the game for performance and responsiveness"\n],\n"User Stories": [\n"As a player, I want to '
        'be able to move tiles around the board to combine numbers",\n"As a player, I want to be able to undo '
        'and redo moves to correct mistakes",\n"As a player, I want to see the final score and game over screen'
        ' when I win"\n],\n"Competitive Analysis": [\n"Competitor A: 2048 game with a simple user interface and'
        ' basic graphics",\n"Competitor B: 2048 game with a more complex user interface and better graphics",'
        '\n"Competitor C: 2048 game with a unique twist on the rules and a more challenging gameplay experience"'
        '\n],\n"Competitive Quadrant Chart": "quadrantChart\\n\ttitle Reach and engagement of campaigns\\n\t\t'
        "x-axis Low Reach --> High Reach\\n\t\ty-axis Low Engagement --> High Engagement\\n\tquadrant-1 We "
        "should expand\\n\tquadrant-2 Need to promote\\n\tquadrant-3 Re-evaluate\\n\tquadrant-4 May be "
        "improved\\n\tCampaign A: [0.3, 0.6]\\n\tCampaign B: [0.45, 0.23]\\n\tCampaign C: [0.57, 0.69]\\n\t"
        'Campaign D: [0.78, 0.34]\\n\tCampaign E: [0.40, 0.34]\\n\tCampaign F: [0.35, 0.78]"\n],\n"Requirement '
        'Analysis": "The requirements are clear and well-defined, but there may be some ambiguity around the '
        'specific implementation details",\n"Requirement Pool": [\n["P0", "Implement a game with the same '
        'rules as the original 2048 game"],\n["P1", "Add a scoreboard to track the player progress"],\n["P2", '
        '"Allow the player to undo and redo moves"]\n],\n"UI Design draft": "The UI should be simple and easy '
        "to use, with a clean and visually appealing design. The game board should be the main focus of the "
        'UI, with clear and concise buttons for the player to interact with.",\n"Anything UNCLEAR": ""\n}\n'
        "[/CONTENT]\n\nI hope this helps! Let me know if you have any further questions or if there anything "
        "else I can do to assist you."
    )
    output = extract_content_from_output(output)
    assert output.startswith('{\n"Original Requirements"') and output.endswith('"Anything UNCLEAR": ""\n}')

    output = """ Sure, I'd be happy to help! Here's the JSON output for the given context:\n\n[CONTENT]\n{
"Implementation approach": "We will use the open-source framework PyGame to create a 2D game engine, which will
 provide us with a robust and efficient way to handle game logic and rendering. PyGame is widely used in the game
 development community and has a large number of resources and tutorials available online.",\n"Python package name":
 "pygame_2048",\n"File list": ["main.py", "game.py", "constants.py", "ui.py"],\n"Data structures and interface
 definitions": '\nclassDiagram\n   class Game{\n       +int score\n       +list<tile> tiles\n       +function
 move_tile(tile, int dx, int dy)\n       +function undo_move()\n       +function get_highest_score()\n   }\n
   class Tile{\n       +int value\n       +int x\n       +int y\n   }\n   ...\n   Game "1" -- "1" Food: has\n',
\n"Program call flow": '\nsequenceDiagram\n   participant M as Main\n   participant G as Game\n   ...\n   G->>M:
 end game\n',\n"Anything UNCLEAR": "The requirement is clear to me."\n}\n[/CONTENT]  Here's the JSON output for the
 given context, wrapped inside the [CONTENT][/CONTENT] format:\n\n[CONTENT]\n{\n"Implementation approach": "We will
 use the open-source framework PyGame to create a 2D game engine, which will provide us with a robust and efficient
 way to handle game logic and rendering. PyGame is widely used in the game development community and has a large
  number of resources and tutorials available online.",\n"Python package name": "pygame_2048",\n"File list":
 ["main.py", "game.py", "constants.py", "ui.py"],\n"Data structures and interface definitions": '\nclassDiagram\n
   class Game{\n       +int score\n       +list<tile> tiles\n       +function move_tile(tile, int dx, int dy)\n
+function undo_move()\n       +function get_highest_score()\n   }\n   class Tile{\n       +int value\n       +int x\n
       +int y\n   }\n   ...\n   Game "1" -- "1" Food: has\n',\n"Program call flow": '\nsequenceDiagram\n   participant
        M as Main\n   participant G as Game\n   ...\n   G->>M: end game\n',\n"Anything UNCLEAR": "The requirement is
        clear to me."\n}\n[/CONTENT]  Great! Your JSON output is well-formatted and provides all the necessary
        information for a developer to understand the design and implementation of the 2048 game.
"""
    output = extract_content_from_output(output)
    assert output.startswith('{\n"Implementation approach"') and output.endswith(
        '"Anything UNCLEAR": "The requirement is clear to me."\n}'
    )



def test_extract_content_from_output_0206():
    """
    cases
        xxx [CONTENT] xxxx [/CONTENT]
        xxx [CONTENT] xxx [CONTENT] xxxx [/CONTENT]
        xxx [CONTENT] xxxx [/CONTENT] xxx [CONTENT][/CONTENT] xxx [CONTENT][/CONTENT]   # target pair is the last one
    """
    from metagpt.utils.repair_llm_raw_output import extract_content_from_output

    output = (
        """[CONTENT]
{
    "Language": "en_us",
    "Programming Language": "Python",
    "Original Requirements": "Develop a data analysis and visualization tool that takes a dataframe as input and outputs various relevant statistical metrics from the table.",
    "Product Goals": [
        "Provide comprehensive statistical analysis capabilities",
        "Offer intuitive and interactive data visualization",
        "Ensure ease of use for both technical and non-technical users"
    ],
    "User Stories": [
        "As a data analyst, I want to input a dataframe and receive detailed statistical metrics so that I can understand the data better.",
        "As a business user, I want to visualize data trends and patterns easily so that I can make informed decisions.",
        "As a developer, I want to integrate this tool into my existing workflows with minimal setup so that I can save time.",
        "As a non-technical user, I want to use the tool without needing to write code so that I can analyze data independently."
    ],
    "Competitive Analysis": [
        "Tableau: Powerful visualization but requires a steep learning curve and is expensive.",
        "Power BI: Great for business users but limited in advanced statistical analysis.",
        "Pandas Profiling: Excellent for quick data profiling but lacks interactive visualization.",
        "Google Data Studio: Free and easy to use but limited in customization and advanced analytics.",
        "Matplotlib/Seaborn: Highly customizable but requires significant coding knowledge."
    ],
    "Competitive Quadrant Chart": "quadrantChart\n    title \"Reach and engagement of data analysis tools\"\n    x-axis \"Low Reach\" --> \"High Reach\"\n    y-axis \"Low Engagement\" --> \"High Engagement\"\n    quadrant-1 \"We should expand\"\n    quadrant-2 \"Need 
to promote\"\n    quadrant-3 \"Re-evaluate\"\n    quadrant-4 \"May be improved\"\n    \"Tableau\": [0.8, 0.7]\n    \"Power BI\": [0.75, 0.65]\n    \"Pandas Profiling\": [0.6, 0.5]\n    \"Google Data Studio\": [0.7, 0.4]\n    \"Matplotlib/Seaborn\": [0.5, 0.6]\n    \"Our Target Product\": [0.7, 0.7]",
    "Requirement Analysis": "The tool must handle various types of data inputs, provide a wide range of statistical metrics, and offer interactive visualizations. It should be user-friendly for both technical and non-technical users, with minimal setup required for integration.",
    "Requirement Pool": [
        [
            "P0",
            "The tool should accept a dataframe as input and output key statistical metrics such as mean, median, mode, standard deviation, etc."
        ],
        [
            "P0",
            "The tool should provide interactive visualizations such as histograms, scatter plots, and box plots."
        ],
        [
            "P1",
            "The tool should offer a user-friendly interface that requires no coding for basic operations."
        ],
        [
            "P1",
            "The tool should be easily integrable with existing Python workflows."
        ],
        [
            "P2",
            "The tool should support exporting visualizations and reports in multiple formats (PDF, PNG, etc.)."
        ]
    ],
    "UI Design draft": "The UI will feature a clean, modern design with a sidebar for input options, a main display area for visualizations, and a bottom panel for statistical metrics. Users can drag and drop data files or input data directly. Interactive elements like sliders and dropdowns will allow for dynamic data exploration.",
    "Anything UNCLEAR": "Clarify the specific statistical metrics and visualization types required by the end-users. Also, confirm the preferred level of interactivity and customization for the visualizations."
}
[/CONTENT]
"""
    )
    output = extract_content_from_output(output)
    print(output)
    # assert output.startswith('{\n"Required Python third-party packages') and output.endswith(
    #     'UNCLEAR": "How to start the game."\n]'
    # )
