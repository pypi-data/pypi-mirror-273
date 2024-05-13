import os
import math
import boto3
import logging
from litellm import completion
from typing import Dict, Optional, List
from fmbench.scripts.fmbench_predictor import (FMBenchPredictor,
                                               FMBenchPredictionResponse)

# set a logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the global variables, including the embeddings model declaration
# and the service name
EMBEDDING_MODELS: List[str] = ["amazon.titan-embed-text-v1",
                               "cohere.embed-english-v3",
                               "cohere.embed-multilingual-v3"]
SERVICE_NAME: str = 'bedrock'


class BedrockPredictor(FMBenchPredictor):

    # initialize the service name
    _service_name: str = SERVICE_NAME

    # overriding abstract method
    def __init__(self,
                 endpoint_name: str,
                 inference_spec: Optional[Dict]):
        try:
            # initialize private member variables
            self._endpoint_name = endpoint_name
            self._pt_model_id = None
            self._inference_spec = inference_spec
            self._aws_region = boto3.Session().region_name

            # check if the endpoint name corresponded to a provisioned throughput
            # endpoint
            if ':provisioned-model/' in self._endpoint_name:
                logger.info(f"{self._endpoint_name} is a provisioned throughput endpoint")
                bedrock_client = boto3.client(SERVICE_NAME)
                response = bedrock_client.list_provisioned_model_throughputs()
                if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                    logger.error(f"error received while calling list_provisioned_model_throughputs, response=\"{response}\", "
                                 f"BedrockPredictor cannot be created")
                else:
                    fm_arn = [pt_summary['foundationModelArn'] for \
                                pt_summary in response['provisionedModelSummaries'] \
                                  if pt_summary['provisionedModelArn'] == self._endpoint_name]
                    if len(fm_arn) > 0:                        
                        # set the PT name which looks like arn:aws:bedrock:us-east-1:<account-id>:provisioned-model/<something>                        
                        self._pt_model_id = self._endpoint_name
                        # set the endpoint name which needs to look like the FM model id
                        # this can now be extracted from the fm_arn which looks like 
                        # 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0:28k',                        
                        self._endpoint_name = fm_arn[0].split("/")[1]
                        logger.info(f"a matching PT was found, self._pt_model_id={self._pt_model_id}, "
                                    f"self._endpoint_name={self._endpoint_name}")
                    else:
                        logger.error(f"no matching PT was found, BedrockPredictor cannot be created")
                    
                
            # model_id for the litellm API with the specific bedrock model of choice
            # endpoint_name in case of bedrock refers to the model_id such as 
            # cohere.command-text-v14 for example
            self._bedrock_model = f"{self._service_name}/{self._endpoint_name}"
            # litellm supports the following inference params as per
            # https://litellm.vercel.app/docs/completion/input
            self._temperature = 0.1
            self._max_tokens = 100
            self._top_p = 0.9
            # not used for now but kept as placeholders for future
            self._stream = None
            self._stop = None

            # no caching of responses since we want every inference
            # call to be independant
            self._caching = False

            # override these defaults if there is an inference spec provided
            if inference_spec:
                parameters: Optional[Dict] = inference_spec.get('parameters')
                if parameters:
                    self._temperature = parameters.get('temperature', self._temperature)
                    self._max_tokens = parameters.get('max_tokens', self._max_tokens)
                    self._top_p = parameters.get('top_p', self._top_p)
            self._response_json = {}
            logger.info(f"__init__, _bedrock_model={self._bedrock_model}, self._pt_model_id={self._pt_model_id},"
                        f"_temperature={self._temperature} "
                        f"_max_tokens={self._max_tokens}, _top_p={self._top_p} "
                        f"_stream={self._stream}, _stop={self._stop}, _caching={self._caching}")
        except Exception as e:
            exception_msg = f"""exception while creating predictor/initializing variables
                            for endpoint_name={self._endpoint_name}, exception=\"{e}\", 
                            BedrockPredictor cannot be created"""
            logger.error(exception_msg)
            raise ValueError(exception_msg)

    def get_prediction(self, payload: Dict) -> FMBenchPredictionResponse:
        # Represents the prompt payload
        prompt_input_data = payload['inputs']
        os.environ["AWS_REGION_NAME"] = self._aws_region
        latency: Optional[float] = None
        completion_tokens: Optional[int] = None
        prompt_tokens: Optional[int] = None

        try:
            # this response is for text generation models on bedrock: Claude, Llama, Mistral etc.
            logger.info(f"Invoking {self._bedrock_model} to get inference")
            # cohere does not support top_p and apprarently LiteLLM does not
            # know that?
            if 'cohere' not in self._endpoint_name:
                response = completion(model=self._bedrock_model,
                                      model_id=self._pt_model_id,
                                      messages=[{"content": prompt_input_data,
                                                 "role": "user"}],
                                      temperature=self._temperature,
                                      max_tokens=self._max_tokens,
                                      top_p=self._top_p,
                                      caching=self._caching,)
            else:
                response = completion(model=self._bedrock_model,
                                      model_id=self._pt_model_id,
                                      messages=[{"content": prompt_input_data,
                                                 "role": "user"}],
                                      temperature=self._temperature,
                                      max_tokens=self._max_tokens,
                                      caching=self._caching,)

            # iterate through the entire model response
            # since we are not sending bached request so we only expect
            # a single completion
            for choice in response.choices:
                # extract the message and the message's content from litellm
                if choice.message and choice.message.content:
                    # extract the response from the dict
                    self._response_json["generated_text"] = choice.message.content
                    break

            # Extract number of input and completion prompt tokens
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens

            # Extract latency in seconds
            latency = response._response_ms / 1000
        except Exception as e:
            logger.error(f"exception during prediction, endpoint_name={self._endpoint_name}, "
                         f"exception={e}")

        return FMBenchPredictionResponse(response_json=self._response_json,
                                         latency=latency,
                                         completion_tokens=completion_tokens,
                                         prompt_tokens=prompt_tokens)

    def calculate_cost(self,
                       instance_type: str,
                       pricing: Dict,
                       duration: float,
                       prompt_tokens: int,
                       completion_tokens: int) -> float:
        """Represents the function to calculate the cost for Bedrock experiments.
        instance_type represents the model name
        """

        # Initializing all cost variables
        experiment_cost: Optional[float] = None
        input_token_cost: Optional[float] = None
        output_token_cost: Optional[float] = None
        try:
            if self._pt_model_id is None:
                logger.info("calculate_cost, calculating cost with token based pricing")
                # Retrieve the pricing information for the instance type
                bedrock_pricing = pricing['pricing']['token_based']
                # Calculate cost based on the number of input and output tokens
                model_pricing = bedrock_pricing.get(instance_type, None)
                if model_pricing:
                    input_token_cost = (prompt_tokens / 1000.0) * model_pricing['input-per-1k-tokens']
                    output_token_cost = (completion_tokens / 1000.0) * model_pricing['output-per-1k-tokens']
                    experiment_cost = input_token_cost + output_token_cost
                    logger.info(f"instance_type={instance_type}, prompt_tokens={prompt_tokens}, "
                                f"input_token_cost={input_token_cost}, output_token_cost={completion_tokens}, "
                                f"output_token_cost={output_token_cost}, experiment_cost={experiment_cost}")
                else:
                    logger.error(f"model pricing for \"{instance_type}\" not found, "
                                 f"cannot calculate experiment cost")
            else:
                logger.info("calculate_cost, calculating cost with PT pricing")
                instance_based_pricing = pricing['pricing']['instance_based']
                hourly_rate = instance_based_pricing.get(instance_type, None)
                # calculating the experiment cost for instance based pricing
                duration_in_hours_ceil = math.ceil(duration/3600)
                experiment_cost = hourly_rate * duration_in_hours_ceil
                logger.info(f"instance_type={instance_type}, hourly_rate={hourly_rate}, "
                            f"duration_in_hours_ceil={duration_in_hours_ceil}, experiment_cost={experiment_cost}")

        except Exception as e:
            logger.error(f"exception occurred during experiment cost calculation, exception={e}")
        return experiment_cost

    @property
    def endpoint_name(self) -> str:
        """The endpoint name property."""
        return self._endpoint_name

    @property
    def inference_parameters(self) -> Dict:
        """The inference parameters property."""
        return dict(temperature=self._temperature,
                    max_tokens=self._max_tokens,
                    top_p=self._top_p)


def create_predictor(endpoint_name: str, inference_spec: Optional[Dict]):
    if endpoint_name in EMBEDDING_MODELS:
        logger.error(f"embeddings models not supported for now")
        return None
    else:
        return BedrockPredictor(endpoint_name, inference_spec)