import json
import boto3
from botocore.exceptions import ClientError

import app_constants as app_consts

# This class provides an abstraction to LLM services that may be called
# For this implementation this is wrapping the Amazon Bedrock service


class LlmFacade:

    def __init__(self, bedrock_model_id: str):
        self.bedrock_model_id = bedrock_model_id
        self.llm_stop_sequences = app_consts.BEDROCK_STOP_SEQUENCES

    # The invoke method of this class invoke an LLM with the input LLM prompt
    # It will then return a dictionary that includes: the JSON output from the LLM, plus processing status
    # If the prompt/invocation does not result in a JSON output/completion, the output will be set on None,
    # and the processing status will be set to fail
    def invoke(self, llm_prompt: str):
        # create a dictionary to store the generated SQL
        generated_json = {}

        # call the Bedrock llm service with the llm_prompt
        llm_output = self.query_bedrock(llm_prompt)

        # add the SQL output to the dictionary
        generated_json[app_consts.LLM_OUTPUT] = llm_output

        if llm_output is not None:
            # add the processing status to the dictionary
            generated_json[app_consts.PROCESSING_STATUS] = app_consts.SUCCESS
        else:
            generated_json[app_consts.PROCESSING_STATUS] = app_consts.FAIL

        # return the generated SQL
        return generated_json

    @staticmethod
    def query_endpoint(payload, endpoint_name):
        client = boto3.client('runtime.sagemaker')
        response = client.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType='application/json',
            Body=json.dumps(payload).encode('utf-8'),
        )
        response = response["Body"].read().decode("utf8")
        response = json.loads(response)
        return response

    def query_bedrock(self, payload):
        bedrock_client = boto3.client(service_name='bedrock-runtime', region_name=app_consts.BEDROCK_AWS_REGION)
        result = None

        inference_config = {
            "temperature": 0.05,  # Set the temperature for generating diverse responses
            "maxTokens": 512,  # Set the maximum number of tokens to generate
            "stopSequences": self.llm_stop_sequences,  # Define the stop sequences for generation
        }
        # Define additional model fields
        additional_model_fields = {"top_p": 0.95}

        # Create the converse method parameters
        converse_api_params = {
            "modelId": self.bedrock_model_id,
            "messages": [{"role": "user", "content": [{"text": payload}]}],  # Provide the prompt
            "inferenceConfig": inference_config,  # Pass the inference configuration
            "additionalModelRequestFields": additional_model_fields  # Pass additional model fields
        }

        # Send a request to the Bedrock client to generate a response
        try:
            response = bedrock_client.converse(**converse_api_params)

            # Extract the generated text content from the response
            completion = response['output']['message']['content'][0]['text']

            result = completion.replace("\n", ' ')

            # Return the generated text content
            result = json.loads(result)

        except ClientError as err:
            message = err.response['Error']['Message']
            print(f"A client error occurred: {message}")
            result = None
        except ValueError:
            print("Note: Being non-deterministic, sometimes the LLM may not return a strict JSON format completion")
            print(f"Output completion: {result}")
            result = None

        return result

