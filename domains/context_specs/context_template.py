#######################################################
# Template
# Static prompt elements for constructing a complete prompt

DOMAIN_DESC = "[[name of the domain]]"

SYSTEM_PROMPT_INSTRUCTIONS = \
    """You are a SQL expert. Given the following SQL tables defintions, generate SQL language to answer the user's question. 

[[replave this part with the domain-specific instructions for the LLM]].
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

TABLE_NAMES = [""]
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
