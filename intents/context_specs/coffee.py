#######################################################
# For INTENT_VACATION_MANAGEMENT
# Static prompt elements for constructing a complete prompt

INTENT_DESC = "coffee"

SYSTEM_PROMPT_INSTRUCTIONS = \
    """You are a SQL expert. Given the following SQL tables defintions, generate SQL language to answer the user's question. 

Each user question is about employee vacation: days available, requesting time off, etc. 
If the year for a query on vacation totals is not provided, assume the year is 2024.
Produce SQL ready for use with a SQLITE database.
Output the result in a JSON format with one key "sql".
Answer the question immediately without preamble.

"""

USER_PROMPT = "question: "

ANNOTATED_SQL_DEFINITIONS = \
    """
"""

JOIN_HINTS = """
"""

SQL_PREAMBLE_PT1 = [""]
SQL_PREAMBLE_PT2 = [""]


FEW_SHOT_EXAMPLES = """
<example>
</example>
"""

SYSTEM_PROMPT = \
    SYSTEM_PROMPT_INSTRUCTIONS + "<SQL>" + \
    ANNOTATED_SQL_DEFINITIONS + \
    JOIN_HINTS + "</SQL>" + \
    FEW_SHOT_EXAMPLES
