# ebb-events:
EbbCarbon package to standardize event message structures. For environmental and industrial automation montioring, we are using many physical sensors to read/gather data about our systems and the environment. In order to communicate this information across systems, we are utilizing the MQTT messaging protocol to publish and subscribe to various messages and topics (however, this structure can be used to publish events across various other protocols as well). In an attempt to standardize the event message structure, this package works to define a standard topic hierarchy, standard event types to use, and a standard payload structure that can be replicated and re-used throughout the industry. This structure will be consistent with the CloudEvent structure defined [here] (https://cloudevents.io/) while implementing some additional standards and best practices so that these events can be consumed and used by CloudEvent users as well.

# Use:
Install the ebb-events package from pip installer via: `pip install ebb-events`.
Use ebb-events to format your event messages and topics.
```python
from ebb_events.builders.event_builder import EventEnvelope

event_envelope = EventEnvelope(
    organization="test-org",
    system_id="test-system",
    event_type="data",
    subsystem_id="test-subsystem",
    device_id="test-device-01",
)

event_topic = event_envelope.build_event_topic()
# Builds a JSON payload of the expected ebb-events structure
event_payload = event_envelope.build_event_payload_json(
    message={...},
    serial_number="ABC123",
    metadata={...},
    datetime_obj=my_datetime
)
```

Use ebb-events package to consume events published with this expected ebb-events structure
```python
from ebb_events.consumers.event_consumer import EventConsumer

my_event_payload = {...}
event_consumer = EventConsumer(payload=my_event_payload)

event_consumer.get_event_message()  # Retrieves the dict message found in the payload's `data` field
event_consumer.get_event_time()
event_conumser.get_event_system_id()
event_consumer.get_device_serial_number()
```

# Topic Structure:
One thing that this package enforces is a topic structure for publishing MQTT messages to a broker. Well defined topics help Our topic structure is as follows:
* _\<organization\>/\<system-id\>/\<event-type\>/\<subsystem-id\>/\<device-id\>_

### Topic Naming Rules:
* Lower case only (subscriptions are case sensitive)
* Dashes (not underscores)
* Alphanumeric topics only (Illegal characters: #, +, *, \<spaces\>)
* No leading “/”
* 50 character maximum per topic section (256 maximum total)

### Topic Hierarchy Explained:
1. **\<organization\>:** The highest level in the hierarchy representing the \<organization\> that is publishing and owning this event.
    * Example: `ebb`
2. **\<system-id\>:** The unique \<system-id\> from which this message is originating. The \<system-id\> should be unique and un-changing (e.g. don't rely on things like geographic location if the producer might move locations).
    * Example: `system-name`
3. **\<event-type\>:** The specific type of event being published. As of now, we support four event-types.
    * `data`: Sensor readings and measurements
    * `state`: Sensor current state (e.g. online status, battery life, memory, power, etc.)
    * `config`: Sensor setup (e.g. calibration coefficients, calibration date, physical location, configured outputs/fields, etc.)
    * `cmd`: Instructions for subscribing clients
4. **\<subsystem-id\>:** Systems are typically made up of several subsystems, each of which contains numberous sensors monitoring their own data and readings. This section of the topic hierarchy should define which subsystem the sensor data is coming from.
    * Example: `system-name` is made up of 4 subsystems, 3 of which are different "my-subsystem-name" subsystems -> the various "my-subsystem-name" subsystems could be labeled `my-subsystem-name-01`, `my-subsystem-name-02`, and `my-subsystem-name-03`
5. **\<device-id\>:** The unique identity of a device _as it relates to the subsystem_ on which it lives. This is _not_ the device's serial number or physical unique ID since the physical device might be replaced.
    * Example: `my-subsystem-name-01` has sensors ("my-sensor") in slots 01, 02, and 03. Therefore \<device-id\> could be `my-sensor-02`
        * If the physical "my-sensor" in slot 02 fails and is replaced with a new "my-sensor", even though the serial number is now different, the \<device-id\> in your topic would remain the same because this part of the topic refers to the \<device-id\> as it relates to the overall subsystem, not as it relates to the physical device itself.
        * The new "my-sensor" is still `my-sensor-02`.
### Topic Example:
For a data message being published by one of Ebb's edge-nodes with measurements from "my-sensor" in sensor slot 02 of subsystem 1, which makes up system-name:
* `ebb/system-name/data/subsystem-1/my-sensor-02`

# Event Payload Structure:
This package defines the event payload schema to follow for all event types. The schema includes relavant metadata in the EventEnvelope and the actual message information in the "data" field of the payload. Specific message structures of the "data" field differ based on event type and the context of the event. The envelope + data make up the overall event payload. All MQTT event messages that are published and consumed should subscribe to this general structure making it easier to share data across organizations and systems. Names of payload fields follow attribute names from [CloudEvents](https://cloudevents.io/) as well.

### Event Payload:
Structure shared by all event messages regardless of event type
```python
{
    "id": str(uuid),
    "time": str,  # [RFC3339](https://datatracker.ietf.org/doc/html/rfc3339) format
    "source": str,  # same as topic string
    "type": str,
    "data": {
        "metadata": {
            "serial_number": str,
            ...
        },
        ...  # unique nested JSON dependent on event-type
    }
}
```

### Suggested `data` Event Message Structure:
The ebb-events package allows users to publish payloads of any structure (as long as they are JSON serializable) so that it can be helpful for publishing all types of events.  However, we have a recommened message structure that we encourage all to adopt when publishing sensor data events that will allow consumers to process the readings smoothly and accurately. Each variable that is measured by a sensor should named following the convention outlined [here](https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html) whenever possible, and should have a corresponding `value` and `units` attached to it and should be formatted in the `message` argument of `build_event_payload_json/dict(message={})` like so:
```python
message = {
    "variable_name_1": {
        "value": ____,
        "units": str
    },
    "variable_name_2": {
        "value": ____,
        "units": str
    },
    ...
}
```

### EventEnvelope Class:
The EventEnvelope class is used to consolidate all of the pieces of aa event payload and build the expected structure for a user so that users don't have to worry about constructing the properly formatted topic or payload. The `EventEnvelope` class expects to be provided with certain fields that are then used to build the topic and payload via class methods. These methods handle all the validation and formatting needed to ensure that your events follow the ebb-events standards.

Required fields: `organization`, `system_id`, `event_type`, `subsystem_id`, `device_id`
Useful methods: `EventEnvelope().build_event_topic()`, `EventEnvelope().build_event_payload()`

# Event Consumer:
This package defines an event consumer that can be used to process incoming events that follow this ebb-events structure. To use this consumer, initialize the class with a given JSON payload: `EventConsumer(payload=my_payload)`. Then, you can use the various getters present on the class in order to retrieve different pieces of the payload depending on your needs (e.g. system_id, message, metadata, etc.). If you need all the parts of the payload that go into building it (e.g. an entire `EventEnvelope` wrapper for the payload) you may also use the `get_event_envelope()` method to do so.

### Exception Handling
If you attempt to consume an event that _DOES NOT_ match the ebb-events structure, you can still initialize an `EventConsumer(payload=my_payload)` object and the payload will live as `EventConsumer().raw_payload`. However, all of the getter methods will raise `PayloadFormatExceptions` because the payload does not match the expected format. Therefore, for a payload that does not match the ebb-events structure, you must process the payload as a raw JSON/dict object instead.
