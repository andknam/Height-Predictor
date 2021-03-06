# -*- coding: utf-8 -*-

import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from processing import get_prediction_info, get_brush_growth_type, get_one_year_growth_type
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
        
        # retrieving all slot values 
        slots = handler_input.request_envelope.request.intent.slots
        patient_name = slots['name'].value
        recent_height = slots['height'].value
        chronological_year = int(slots['chronological_year'].value)
        chronological_month = int(slots['chronological_month'].value)
        skeletal_year = slots['skeletal_year'].value
        skeletal_month = slots['skeletal_month'].value
        gender = slots['gender'].value
        selected_growth_type = slots['growth_type'].value

        # getting the growth type 
        if selected_growth_type == 'brush':
            growth_type = get_brush_growth_type(chronological_year, chronological_month, skeletal_year, skeletal_month, gender)
        else:
            growth_type = get_one_year_growth_type(chronological_year, chronological_month, skeletal_year, skeletal_month)

        prediction_info = get_prediction_info(recent_height, skeletal_year, skeletal_month, gender, growth_type[0])

        # error responses
        if prediction_info[0] == 'skeletal_low':
            response = responses.skeletal_low
        elif prediction_info[0] == 'skeletal_high':
            response = responses.skeletal_high
        elif prediction_info[0] == 'skeletal_index_young':
            response = responses.skeletal_index_young
        elif prediction_info[0] == 'skeletal_index_old':
            response = responses.skeletal_index_old
        elif prediction_info[0] == 'height_index_low':
            response = responses.height_index_low
        elif prediction_info[0] == 'height_index_tall':
            response = responses.height_index_tall
        elif prediction_info[0] == 'chronological_young':
            response = responses.chronological_young
        elif prediction_info[0] == 'chronological_old':
            response = responses.chronological_old
        else:
            ph = prediction_info[0]
            pm = prediction_info[1]
            
            gt = growth_type[0]

            rh = recent_height
            cy = str(chronological_year)
            cm = str(chronological_month)
            sy = skeletal_year
            sm = skeletal_month
            p = patient_name
            
            # speak output based on gender and growth type 
            if gender == 'male':
                if selected_growth_type == 'brush':
                    sd = growth_type[1]
                    speak_output = responses.male_brush.format(sy, sm, gt, cy, cm, sd, ph, pm)
                else:
                    speak_output = responses.male_one_year.format(sy, sm, gt, cy, cm, ph, pm)
            else:
                if selected_growth_type == 'brush':
                    sd = growth_type[1]
                    speak_output = responses.female_brush.format(sy, sm, gt, cy, cm, sd, ph, pm)
                else:
                    speak_output = responses.female_one_year.format(sy, sm, gt, cy, cm, ph, pm)
                    
            # usage of dynamodb table commented out for now 
            #dynamodb = boto3.resource('dynamodb',
            #              region_name = 'us-east-1',
            #              aws_access_key_id = 'access-key',
            #              aws_secret_access_key = 'secret-access-key')
            #              
            #dynamo_client = DynamoDbAdapter(table_name = 'Patient_Information',
            #                    partition_key_name = 'user_id',  # the ID you choose while creating the table
            #                    partition_keygen = user_id_partition_keygen,
            #                    create_table = False,  # default
            #                    dynamodb_resource = dynamodb) 
                                
            # Store attributes for the user
            #attr = {
            #'patient_name': patient_name,
            #'predicted_height_message': speak_output, 
            #'gender': gender,
            #'recent_height': recent_height,
            #'growth_type': growth_type,
            #'skeletal_age': str(skeletal_year) + '-' + str(skeletal_month)
            #'chronological_age': str(chronological_year) + '-' + str(chronological_month)
            #}
            
            #dynamo_client.save_attributes(request_envelope = handler_input.request_envelope, attributes = attr)

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
