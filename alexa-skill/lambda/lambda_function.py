# -*- coding: utf-8 -*-

import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from processing import get_prediction_info
import responses

from ask_sdk_dynamodb.adapter import DynamoDbAdapter, user_id_partition_keygen
import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = responses.welcome
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class PatientInfoIntentHandler(AbstractRequestHandler):
    """Handler for Patient Info Intent."""
    
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        
        return ask_utils.is_intent_name("PatientInfoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        patient_name = slots['name'].value
        gender = slots['gender'].value
        recent_height = slots['height'].value
        growth_type = slots['growth_type'].value
        skeletal_year = slots['skeletal_year'].value
        skeletal_month = slots['skeletal_month'].value
        
        prediction_info = get_prediction_info(gender, recent_height, growth_type, skeletal_year, skeletal_month)
        
        if prediction_info[0] == 'skeletal_low':
            speak_output = responses.skeletal_low
        elif prediction_info[0] == 'skeletal_high':
            speak_output = responses.skeletal_high
        elif prediction_info[0] == 'skeletal_index_young':
            speak_output = responses.skeletal_index_young
        elif prediction_info[0] == 'skeletal_index_old':
            speak_output = responses.skeletal_index_old
        elif prediction_info[0] == 'height_index_low':
            speak_output = responses.height_index_low
        elif prediction_info[0] == 'height_index_tall':
            speak_output = responses.height_index_tall
        else:
            predicted_height = prediction_info[0]
            percent_of_mature = prediction_info[1]
            
            output = "Based on their current height of {} inches and their skeletal age of {} years and {} months, {}'s predicted \
            height is about {}. ".format(recent_height, skeletal_year, skeletal_month, patient_name, predicted_height)
            output_cont = 'They have completed {}% of their growth!'.format(percent_of_mature)
            speak_output = output + output_cont
                                
            dynamodb = boto3.resource('dynamodb',
                          region_name = 'region',
                          aws_access_key_id = 'access-key',
                          aws_secret_access_key = 'secret-access-key')
                          
            dynamo_client = DynamoDbAdapter(table_name = 'table-name',
                                partition_key_name = 'user_id',  # the ID you choose while creating the table
                                partition_keygen = user_id_partition_keygen,
                                create_table = False,  # default
                                dynamodb_resource = dynamodb) 
                                
            # Store attributes for the user
            attr = {
            'patient_name': patient_name,
            'predicted_height_message': speak_output, 
            'gender': gender,
            'recent_height': recent_height,
            'growth_type': growth_type,
            'skeletal_age': str(skeletal_year) + '-' + str(skeletal_month)
            }
            
            dynamo_client.save_attributes(request_envelope = handler_input.request_envelope, attributes = attr)

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(PatientInfoIntentHandler())
#sb.add_request_handler(SavedInfoIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()