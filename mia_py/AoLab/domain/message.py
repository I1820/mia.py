import dataclasses


@dataclasses.dataclass()
class AoLabThingMessage:
    node_id: int
    battery: int
    things: list[dict[str, str]]
