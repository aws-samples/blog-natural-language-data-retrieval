import app_constants as app_consts
import identity_service_facade
import llm_facade
import pre_process_request
import prepare_request
import rdbms_facade

# configure logging
import logging
logging.basicConfig(format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# This class, TextToSQLFlow, orchestrates the overall control-flow of the service
# The run method, given a user request in natural language will process the request, generate SQL corresponding
# to the request, run that SQL against the appropriate RBDMS and database and return the result
class TextToSQLFlow:
    # constructor
    def __init__(self):
        self.identity_service_facade = identity_service_facade.IdentityServiceFacade()
        self.llm_facade = llm_facade.LlmFacade(app_consts.BEDROCK_MODEL_ID)
        self.rdbms_facade = rdbms_facade.RdbmsFacade()
        self.pre_process_request = pre_process_request.PreProcessRequest(self.llm_facade)
        self.prepare_request = prepare_request.PrepareRequest()

    # Run the primary control-flow of the service
    def run(self, user_request: str):

        # pre-process the request
        pre_processed_request = self.pre_process_request.run(user_request)
        intent = pre_processed_request[app_consts.INTENT]
        named_resources = pre_processed_request[app_consts.NAMED_RESOURCES]

        # convert any named resources to identifiers
        if len(named_resources) > 0:
            identifiers = self.identity_service_facade.resolve(named_resources)
            # add identifies to the pre_processed_request object
            pre_processed_request[app_consts.IDENTIFIERS] = identifiers
        else:
            pre_processed_request[app_consts.IDENTIFIERS] = []

        # prepare the request for the LLM
        prepared_request = self.prepare_request.run(pre_processed_request)
        logger.debug(f"TextToSQLFlow: prepared_request: {prepared_request}")

        # generate SQL
        llm_response = self.llm_facade.invoke(prepared_request[app_consts.LLM_PROMPT])
        generated_sql = llm_response[app_consts.LLM_OUTPUT]

        logger.debug(f"TextToSQLFlow: generated_sql: {generated_sql}")

        # Execute the SQL script
        sql_script = prepared_request[app_consts.SQL_PREAMBLE] + [generated_sql[app_consts.SQL]]
        database = app_consts.get_database_for_intent(intent)
        logger.info(f"TextToSQLFlow: sql_script: {sql_script}")

        results = self.rdbms_facade.execute_sql(database, sql_script)
        rdbms_results, rdbms_status = results[app_consts.RDBMS_OUTPUT], results[app_consts.PROCESSING_STATUS]
        # info message
        print(f"Main Flow: execute_sql_script: {rdbms_results}")
        # return the results and the processing status
        return rdbms_results, rdbms_status

