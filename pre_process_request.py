import app_constants as app_consts
import llm_facade
import identify_service_facade
import intents

# A class called pre-process-request
# The primary function on this class is to pre-process a user request such that it is ready for down-stream processing.
# The run function an input user request (as a string) and returns a dictionary that includes:
# The input user request, the intent class of the request and identifiers found in the request
# This is a simple implementation that will be replaced with a more sophisticated AI in the full implementation.


class PreProcessRequest:

    def __init__(self, llm_inference: llm_facade.LlmFacade):
        self.llm_inference = llm_inference

    # A method to pre-process a request
    def run(self, user_request: str):
        # create a dictionary to store the pre-processed request
        # the input, the intent-class of the input and identifiers found in the input
        pre_processed_request = {app_consts.USER_QUERY: user_request,
                                 app_consts.INTENT: self.determine_intent(user_request),
                                 app_consts.NAMED_RESOURCES: self.get_named_resources_from_user_request(user_request)}

        return pre_processed_request

    def determine_intent(self, user_request: str):
        prompt = app_consts.INTENT_CLASSIFICATION_PROMPT + user_request + "\n"
        intent_inference = self.llm_inference.invoke(prompt)

        if intent_inference[app_consts.PROCESSING_STATUS] == "FAILURE":
            return intents.INTENT_UNKNOWN
        else:
            llm_output = intent_inference[app_consts.LLM_OUTPUT]
            determined_intent = llm_output[app_consts.INTENT]

        if determined_intent in intents.contexts.keys():
            return determined_intent
        else:
            return intents.INTENT_UNKNOWN

    @staticmethod
    def get_named_resources_from_user_request(user_request: str):
        """
        For this use case named resources should be: firstname<space>lastname
        These will looked up in the database
        :param user_request:
        :return:
        """
        # create a set to store the identifiers
        named_resources = set()

        # remove special characters from the user_request
        user_request = user_request.replace(",", " ").replace(".", " ").replace("?", " ").replace("!", " ")
        # lower case the user_request
        user_request = user_request.lower()
        # iterate through each word in the user_request
        first_name, last_name = None, None
        for word in user_request.split():
            if first_name is None:      # first word
                first_name = word
                continue
            elif last_name is None:     # second word
                last_name = word
            else:                       # iterating normally
                first_name = last_name
                last_name = word
            if identify_service_facade.IdentityServiceFacade.is_named_resource(f"{first_name} {last_name}"):
                # add the named resource to the set
                named_resources.add(f"{first_name} {last_name}")

        # return the set of named resources
        return named_resources
