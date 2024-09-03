# The values that are represented here are constants that are declared here for simplicity

BEDROCK_MODEL_ID = 'anthropic.claude-3-haiku-20240307-v1:0'
BEDROCK_AWS_REGION = 'us-east-1'
BEDROCK_PREFILL = ["```{"]
BEDROCK_STOP_SEQUENCES = ["```"]

# Mapping of Intent to database server
# In a Production system this data would be stored/retrieved from a database of some form
INTENT_TO_DATABASE = {
    'vacation': 'db_employee.db',
    'olympics': 'db_olympics.db',
}

FAIL = "fail"
INPUT = "input"
INTENT = "intent"
IDENTIFIERS = "identifiers"
LLM_PROMPT = "llm_prompt"
LLM_OUTPUT = "llm_output"
NAMED_RESOURCES = "named_resources"
PROCESSING_STATUS = "processing_status"
RDBMS_OUTPUT = "rdbms_output"
SQL = "sql"
SQL_PREAMBLE = "sql_preamble"
SQL_QUERY = "sql_query"
SUCCESS = "success"
USER_QUERY = "user_query"


# Prompt constants
STANDARD_USER_PROMPT = "question: "
INTENT_CLASSIFICATION_PROMPT = """
You are an expert at understanding short requests and classifying the request to a one of a given set of classes.
The set of target classes are <classes>vacation, coffee, olympics<classes>
If the request does not correspond to one of these classes, set the class as "other"
Output the result in a JSON format with one key "intent".
Answer the question immediately without preamble.

request: """


def get_database_for_intent(intent: str):
    return INTENT_TO_DATABASE[intent]
