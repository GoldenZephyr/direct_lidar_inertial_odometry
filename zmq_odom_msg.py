from pydantic import BaseModel, ConfigDict, ValidationError


class OdomMsg(BaseModel):
    model_config = ConfigDict(strict=True)

    epoch_ns: int

    x: float
    y: float
    z: float

    vx: float
    vy: float
    vz: float

    qx: float
    qy: float
    qz: float
    qw: float

    omegax: float
    omegay: float
    omegaz: float


def parse_odom_msg(string):
    try:
        msg = OdomMsg.model_validate_json(string)
    except ValidationError as e:
        print(e)
    return msg


if __name__ == "__main__":
    json_data = '{"epoch_ns": 101, "x": 0, "y": 1, "z": 2, "vx": 1, "vy": 2, "vz": 3, "qx": 0, "qy": 0, "qz": 0, "qw": 1, "omegax": 0, "omegay": 1, "omegaz": 0}'
    try:
        msg = OdomMsg.model_validate_json(json_data)
        print(msg)
    except ValidationError as e:
        print(e)
