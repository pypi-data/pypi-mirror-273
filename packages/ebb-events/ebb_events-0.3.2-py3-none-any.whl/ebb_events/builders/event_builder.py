import json
import logging

from datetime import datetime, timezone
from marshmallow import ValidationError
from typing import Optional
from uuid import uuid4

from ebb_events.field_constants import (
    DATA,
    ID,
    METADATA,
    SOURCE,
    TIME,
    TYPE,
    SERIAL_NUMBER,
)
from ebb_events.event_schema import EventEnvelopeSchema, EventPayloadSchema
from ebb_events.exceptions import PayloadFormatException, TopicFormatException


class EventEnvelope:
    """
    EventEnvelope class used to build the event payload and topic
    """

    def __init__(
        self,
        organization: str,
        system_id: str,
        event_type: str,
        subsystem_id: str,
        device_id: str,
    ) -> None:
        """Initialize an EventEnvelope class object with required fields and validate those fields"""
        self.organization = organization
        self.system_id = system_id
        self.event_type = event_type
        self.subsystem_id = subsystem_id
        self.device_id = device_id
        # Fields must all be valid to initialize this class
        self._validate()

    def __eq__(self, other):
        """Write the __eq__ method to evaluate EventEnvelopes with equivalent fields"""
        if not isinstance(other, EventEnvelope):
            return False
        return (
            self.organization == other.organization
            and self.system_id == other.system_id
            and self.event_type == other.event_type
            and self.subsystem_id == other.subsystem_id
            and self.device_id == other.device_id
        )

    def _validate(self):
        """
        Validate that the fields passed to EventEnvelope follow expected format and rules.

        Return: None if valid fields
        Raises: TopicFormatException for invalid fields
        """
        envelope_schema = EventEnvelopeSchema()
        errors = envelope_schema.validate(envelope_schema.dump(self))
        if errors:
            # errors will be a dictionary of validation errors
            logging.error("Invalid EventEnvelope", extra={"errors": errors})
            raise TopicFormatException(errors)

    def _format_time(self, datetime_raw: Optional[datetime] = None) -> str:
        """
        Helper takes in datetime object or None and returns the string datetime in RFC3339 format UTC.
        If None - timestamp is datetime.now().

        Format: YYYY-MM-DDThh:mm:ss.ssssss+/-hh:mm
        """
        datetime_raw = (
            datetime_raw if datetime_raw is not None else datetime.now(timezone.utc)
        )
        if (
            datetime_raw.tzinfo is None
            or datetime_raw.tzinfo.utcoffset(datetime_raw) is None
        ):
            datetime_raw = datetime_raw.replace(tzinfo=timezone.utc)
        return datetime_raw.isoformat()

    def build_event_topic(self) -> str:
        """
        Joins the EventEnvelope fields to form a valid topic string.
        Note: Fields are validated in __init__ so no need to re-validate here.
        Returns:
            str: _description_
        """
        topic = f"{self.organization}/{self.system_id}/{self.event_type}/{self.subsystem_id}/{self.device_id}"
        # This should be enforced by the ._validate() call and the EventEnvelopeSchema too
        if len(topic) > 256:
            logging.error(f"Invalid Topic. Topic too long: {topic}.")
            raise TopicFormatException("Topic length cannot exceed 256 characters.")
        return topic

    def build_event_payload_dict(
        self,
        message: dict,
        serial_number: str = None,
        metadata: dict = {},
        datetime_obj: Optional[datetime] = None,
        remove_nones: bool = False,
    ) -> dict:
        """
        Method validates the message structure, builds and returns the expected
        event payload to be used in the MQTT payload as a json serializable dictionary.
        NOTE: Returned object is a python dictionary, not a json object. In order to publish this,
        one must either `json.dumps()` this result or use `build_event_payload_json()` method.

        Args:
            message (dict): Dictionary containing the message information that is being published.
            serial_number (str): String serial number of the sensor publishing this event
                    This will be added to metadata dict and will overwrite any metadata field
                    named "serial_number".
            metadata (dict): Dictionary containing extra metadata information to be included in the data.
            datetime_obj (Optional[datetime]): datetime obj to use as event time.
            remove_nones (bool): If set to True, all key:value pairs where value=None will
                                    be removed/omitted from the resulting payload dict

        Returns:
            dict: Dictionary of the expected MQTT event message format.

        Exceptions:
            Raises 'PayloadFormatException' if the topic or message does not meet the expected format.
        """
        if serial_number is not None:
            metadata[SERIAL_NUMBER] = str(serial_number)
        payload_schema = EventPayloadSchema(context={"remove_nones": remove_nones})
        if datetime_obj is not None and type(datetime_obj) is not datetime:
            logging.error(
                f"Invalid datetime_obj: {datetime_obj} must be of type datetime."
            )
            raise PayloadFormatException(
                "datetime_obj must be a valid datetime object."
            )
        try:
            event_payload = {
                ID: uuid4(),
                TIME: self._format_time(datetime_raw=datetime_obj),
                SOURCE: self.build_event_topic(),
                TYPE: self.event_type,
                DATA: {METADATA: metadata, **message},
            }
            # validate that data and metadata are JSON serializable
            json.dumps(message)
            json.dumps(metadata)
            deserialized_payload = payload_schema.load(
                data=event_payload
            )  # validates event_payload against schema
        except TopicFormatException:
            # Exception raised by build_event_topic() if too long
            # logging.error called at source of the TopicFormatException raised
            raise PayloadFormatException(
                "Source and topic must be less than 256 characters."
            )
        except ValidationError as error:
            # Exception raised by schema.load() if not valid marshmallow schema
            logging.error(
                f"Invalid payload. Does not match marshmallow schema: {str(error)}"
            )
            raise PayloadFormatException(
                f"Payload does not match required format: {str(error)}"
            )
        except TypeError as error:
            # Exception raised by json.dumps() if not valid json serializable object
            logging.error(f"Invalid payload, not JSON serializable: {str(error)}")
            raise PayloadFormatException(
                "Payload message and metadata must be JSON serializable dictionaries."
            )
        return payload_schema.dump(deserialized_payload)

    def build_event_payload_json(
        self,
        message: dict,
        serial_number: str = None,
        metadata: dict = {},
        datetime_obj: Optional[datetime] = None,
        remove_nones: bool = False,
    ):
        """
        Method validates the message structure, builds and returns the expected
        event payload to be used in the MQTT payload as a JSON formatted str.

        This returned value can be immediately placed in an MQTT publish call as it's a json string.

        Args:
            message (dict): Dictionary containing the message information that is being published.
            serial_number (str): String serial number of the sensor publishing this event
                    This will be added to metadata dict and will overwrite any metadata field
                    named "serial_number".
            metadata (dict): Dictionary containing extra metadata information to be included in the data
            datetime_obj (Optional[datetime]): datetime obj to use as event time.
            remove_nones (bool): If set to True, all key:value pairs where value=None will
                                    be removed/omitted from the resulting payload json.

        Returns:
            dict: Dictionary of the expected MQTT event message format.

        Exceptions:
            Raises 'PayloadFormatException' if the topic or message does not meet the expected format.
        """
        payload_dict = self.build_event_payload_dict(
            message=message,
            serial_number=serial_number,
            metadata=metadata,
            datetime_obj=datetime_obj,
            remove_nones=remove_nones,
        )
        return json.dumps(payload_dict)
