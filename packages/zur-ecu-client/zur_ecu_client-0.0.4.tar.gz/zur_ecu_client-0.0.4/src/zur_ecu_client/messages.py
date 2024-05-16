from enum import Enum, IntEnum

from zur_ecu_client.senml.senml_pack import SenmlPack
from zur_ecu_client.senml.senml_record import SenmlRecord
from zur_ecu_client.senml.senml_unit import SenmlUnits
from zur_ecu_client.senml.senml_zur_names import SenmlNames


class Messages:
    class AmiState(Enum):
        ACCELERATION = "acceleration"
        SKIDPAD = "skidpad"
        TRACKDRIVE = "trackdrive"
        BRAKETEST = "braketest"
        INSPECTION = "inspection"
        AUTOCROSS = "autocross"

    class EbsState(IntEnum):
        UNAVAILABLE = 1
        ARMED = 2
        ACTIVATED = 3

    class AsState(IntEnum):
        OFF = 1
        READY = 2
        DRIVING = 3
        EMERGENCY_BREAK = 4
        FINISH = 5

    class Dv:

        class Cfg:
            def __init__(self, **kwargs) -> None:
                self.pack = SenmlPack("cfg")
                self.cfg_as = SenmlRecord(
                    SenmlNames.ZUR_SENML_AS,
                    value=kwargs["AS"],
                )
                self.ebs = SenmlRecord(
                    SenmlNames.ZUR_SENML_EBS,
                    value=kwargs["EBS"],
                )
                self.ami = SenmlRecord(
                    SenmlNames.ZUR_SENML_AMI,
                    value=kwargs["AMI"],
                )
                self.pack.add(self.cfg_as)
                self.pack.add(self.ebs)
                self.pack.add(self.ami)

            def get(self) -> str:
                return self.pack.to_json()

        class Ctrl:
            def __init__(self, **kwargs) -> None:
                self.pack: SenmlPack = SenmlPack("ctrl")
                self.brake: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_BRAKE.value,
                    unit=SenmlUnits.SENML_UNIT_PERCENTAGE.value,
                    value=kwargs["brake"],
                )
                self.steering = SenmlRecord(
                    SenmlNames.ZUR_SENML_STEERING.value,
                    unit=SenmlUnits.SENML_UNIT_PERCENTAGE.value,
                    value=kwargs["steering"],
                )
                self.throttle = SenmlRecord(
                    SenmlNames.ZUR_SENML_THROTTLE.value,
                    unit=SenmlUnits.SENML_UNIT_PERCENTAGE.value,
                    value=kwargs["throttle"],
                )
                self.status = SenmlRecord(
                    SenmlNames.ZUR_SENML_STATUS.value,
                    value=kwargs["status"],
                )
                self.pack.add(self.brake)
                self.pack.add(self.steering)
                self.pack.add(self.throttle)
                self.pack.add(self.status)

            def get(self) -> str:
                return self.pack.to_json()

        class Stat:
            def __init__(self, **kwargs) -> None:
                self.pack = SenmlPack("stat")
                self.laps = SenmlRecord(
                    SenmlNames.ZUR_SENML_LAPS,
                    value=kwargs["laps"],
                )
                self.conesAct = SenmlRecord(
                    SenmlNames.ZUR_SENML_CONESACT,
                    value=kwargs["conesAct"],
                )
                self.conesAll = SenmlRecord(
                    SenmlNames.ZUR_SENML_CONESALL,
                    value=kwargs["conesAll"],
                )
                self.pack.add(self.laps)
                self.pack.add(self.conesAct)
                self.pack.add(self.conesAll)

            def get(self) -> str:
                return self.pack.to_json()

        class Acc:
            def __init__(self, **kwargs) -> None:
                self.pack = SenmlPack("acc")
                self.x = SenmlRecord(
                    SenmlNames.ZUR_SENML_X,
                    unit=SenmlUnits.SENML_UNIT_CUBIC_METER_PER_SECOND,
                    value=kwargs["x"],
                )
                self.y = SenmlRecord(
                    SenmlNames.ZUR_SENML_Y,
                    unit=SenmlUnits.SENML_UNIT_CUBIC_METER_PER_SECOND,
                    value=kwargs["y"],
                )
                self.z = SenmlRecord(
                    SenmlNames.ZUR_SENML_Z,
                    unit=SenmlUnits.SENML_UNIT_CUBIC_METER_PER_SECOND,
                    value=kwargs["z"],
                )
                self.pack.add(self.x)
                self.pack.add(self.y)
                self.pack.add(self.z)

            def get(self) -> str:
                return self.pack.to_json()

        class Ping:
            def __init__(self, **kwargs) -> None:
                self.pack = SenmlPack("dv")
                self.ping = SenmlRecord(
                    SenmlNames.ZUR_SENML_REQUEST.value, value=kwargs["ping"]
                )
                self.pack.add(self.ping)

            def get(self) -> str:
                return self.pack.to_json()

    class ECU:

        class HVCB:
            def __init__(self, **kwargs) -> None:
                self.pack = SenmlPack(SenmlNames.ZUR_ECU_HVCB_BASENAME.value)
                self.hvcb: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_SENSOR.value,
                    value=SenmlNames.ZUR_SENML_RESPONSE.value,
                )
                self.LVAccu: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_LVACCU.value,
                    unit=SenmlUnits.SENML_UNIT_VOLT.value,
                    value=kwargs["LVAccu"],
                )
                self.V24: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_24V.value,
                    unit=SenmlUnits.SENML_UNIT_VOLT.value,
                    value=kwargs["V24"],
                )
                self.V12: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_12V.value,
                    unit=SenmlUnits.SENML_UNIT_VOLT.value,
                    value=kwargs["V12"],
                )
                self.LVShutdown: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_LVSHUTDOWN.value,
                    value=kwargs["LVShutdown"],
                )

                self.pack.add(self.hvcb)
                self.pack.add(self.LVAccu)
                self.pack.add(self.V24)
                self.pack.add(self.V12)
                self.pack.add(self.LVShutdown)

            def get(self) -> str:
                return self.pack.to_json()

        class Pedal:
            def __init__(self, **kwargs) -> None:
                self.pack = SenmlPack(SenmlNames.ZUR_ECU_PEDAL_BASENAME.value)
                self.pedal: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_SENSOR.value,
                    value=SenmlNames.ZUR_SENML_RESPONSE.value,
                )
                self.throttleLeft: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_THROTTLE_LEFT.value,
                    unit=SenmlUnits.SENML_UNIT_PERCENTAGE.value,
                    value=kwargs["throttleLeft"],
                )
                self.throttleRight: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_THROTTLE_RIGHT.value,
                    unit=SenmlUnits.SENML_UNIT_PERCENTAGE.value,
                    value=kwargs["throttleRight"],
                )
                self.brakeFront: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_BRAKE_FRONT.value,
                    unit=SenmlUnits.SENML_UNIT_PERCENTAGE.value,
                    value=kwargs["brakeFront"],
                )
                self.brakeBack: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_BRAKE_BACK.value,
                    unit=SenmlUnits.SENML_UNIT_PERCENTAGE.value,
                    value=kwargs["brakeBack"],
                )

                self.pack.add(self.pedal)
                self.pack.add(self.throttleLeft)
                self.pack.add(self.throttleRight)
                self.pack.add(self.brakeFront)
                self.pack.add(self.brakeBack)

            def get(self) -> str:
                return self.pack.to_json()

        class Accu:
            def __init__(self, **kwargs) -> None:
                self.pack = SenmlPack(SenmlNames.ZUR_ECU_ACCU_BASENAME.value)
                self.accu: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_SENSOR.value,
                    value=SenmlNames.ZUR_SENML_RESPONSE.value,
                )
                self.charge: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_CHARGE.value,
                    unit=SenmlUnits.SENML_UNIT_PERCENTAGE.value,
                    value=kwargs["charge"],
                )
                self.temp: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_TEMP.value,
                    unit=SenmlUnits.SENML_UNIT_DEGREES_CELSIUS.value,
                    value=kwargs["temp"],
                )
                self.AIRPos: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_AIRPOS.value,
                    unit=SenmlUnits.SENML_UNIT_VOLT.value,
                    value=kwargs["AIRPos"],
                )
                self.AIRNeg: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_AIRNEG.value,
                    unit=SenmlUnits.SENML_UNIT_VOLT.value,
                    value=kwargs["AIRNeg"],
                )
                self.preRelay: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_PRERELAY.value,
                    unit=SenmlUnits.SENML_UNIT_VOLT.value,
                    value=kwargs["preRelay"],
                )

                self.pack.add(self.accu)
                self.pack.add(self.charge)
                self.pack.add(self.temp)
                self.pack.add(self.AIRPos)
                self.pack.add(self.AIRNeg)
                self.pack.add(self.preRelay)

            def get(self) -> str:
                return self.pack.to_json()

        class Cockpit:
            def __init__(self, **kwargs) -> None:
                self.pack = SenmlPack(SenmlNames.ZUR_ECU_COCKPIT_BASENAME.value)
                self.cockpit: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_SENSOR.value,
                    value=SenmlNames.ZUR_SENML_RESPONSE.value,
                )
                self.x: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_X.value,
                    unit=SenmlUnits.SENML_UNIT_ACCELERATION.value,
                    value=kwargs["x"],
                )
                self.y: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_Y.value,
                    unit=SenmlUnits.SENML_UNIT_ACCELERATION.value,
                    value=kwargs["y"],
                )
                self.z: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_Z.value,
                    unit=SenmlUnits.SENML_UNIT_ACCELERATION.value,
                    value=kwargs["z"],
                )

                self.pack.add(self.cockpit)
                self.pack.add(self.x)
                self.pack.add(self.y)
                self.pack.add(self.z)

            def get(self) -> str:
                return self.pack.to_json()

        class Dv:
            def __init__(self, **kwargs) -> None:
                self.pack = SenmlPack(SenmlNames.ZUR_ECU_DV_BASENAME.value)
                self.dv: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_SENSOR.value,
                    value=SenmlNames.ZUR_SENML_RESPONSE.value,
                )
                self.modeSel: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_MODESEL.value,
                    value=kwargs["modeSel"],
                )
                self.modeACK: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_MODEACK.value,
                    value=kwargs["modeACK"],
                )
                self.reset: SenmlRecord = SenmlRecord(
                    SenmlNames.ZUR_SENML_RESET.value,
                    value=kwargs["reset"],
                )

                self.pack.add(self.dv)
                self.pack.add(self.modeSel)
                self.pack.add(self.modeACK)
                self.pack.add(self.reset)

            def get(self) -> str:
                return self.pack.to_json()

        class Ping:
            def __init__(self) -> None:
                self.pack = SenmlPack(SenmlNames.ZUR_ECU_PING_BASENAME)
                self.request = SenmlRecord(SenmlNames.ZUR_SENML_REQUEST)

            def get(self) -> str:
                return self.pack.to_json()

    @staticmethod
    def convert(value, min_value, max_value, min_mapped, max_mapped):
        value = max(min_value, min(max_value, value))
        value_range = abs(max_value - min_value)
        percentage = (value - min_value) / value_range
        return min_mapped + percentage * (max_mapped - min_mapped)
