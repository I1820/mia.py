from ..domain.message import AoLabThingMessage


class HashtProtocol():
    thing_sensors = {
        't': 'temperature',
        'l': 'light',
        'h': 'humidity',
        'm': 'motion',
        'g': 'gas'
    }

    thing_actuators = {
        'alarm': 'A',
        'lamp': 'l',
        'cooler': 'c',
        'curtain': 'p',
        'projector': 'p',
        'tv': 't',
        'valve': 'v'
    }

    @classmethod
    def marshal(cls, type: str, device_id: str, node_id: str, command: str) -> str:
        if type == 'lamp' or type == 'curtain' or type == 'alarm' \
                or type == 'valve':
            return f'@{node_id},{cls.thing_actuators[type]}{device_id}{command}.'
        if type != 'lamp':
            return f'@{node_id},{cls.thing_actuators[type]}{command}.'
        return ''

    @classmethod
    def unmarshal(cls, message: str) -> AoLabThingMessage:
        if len(message) == 0 or message[0] != '@':
            raise ValueError('message is not valid')
        parts = message.split(',')
        node = parts[0][1:]
        if parts[-1][0].isalpha():
            battery = 0
            parts[-1] = parts[-1][:-2]
        else:
            battery = parts[-1][:-2]
            parts.pop()
            try:
                battery = (int(battery) - 2900) // 13
            except (KeyError, ValueError):
                battery = 0
        things = []
        for thing in parts[1:]:
            things.append({
                'type': cls.thing_sensors[thing[0]],
                'value': thing[2:],
                'device': thing[1]
            })
        return AoLabThingMessage(int(node), battery, things)
