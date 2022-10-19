import json
import logging
from typing import Any, List, Union
import requests
import xml.etree.cElementTree as et


class IrishRailStation:
    """Python class representing Irish rail station taken from their API

    Attributes:
        stationDesc:        Station description.
        stationAlias:       Alias of the station, is optional.
        stationLatitude:    Latitude of the station.
        stationLongitude:   Longitude of the station.
        stationCode:        Station code.
        stationId:          Station Id.
    """
    stationDesc: str
    stationAlias: Union[str, None]
    stationLatitude: float
    stationLongitude: float
    stationCode: str
    stationId: str

    def __init__(self, stationDesc: str,
                 stationAlias: Union[str, None],
                 stationLatitude: float,
                 stationLongitude: float,
                 stationCode: str,
                 stationId: str) -> None:
        self.stationDesc = stationDesc
        self.stationAlias = stationAlias
        self.stationLatitude = stationLatitude
        self.stationLongitude = stationLongitude
        self.stationCode = stationCode
        self.stationId = stationId


def as_rail_station(dct):
    return IrishRailStation(dct['stationDesc'],
                 dct['stationAlias'],
                 dct['stationLatitude'],
                 dct['stationLongitude'],
                 dct['stationCode'],
                 dct['stationId']) 


def get_irish_rail_stations(base_url: str = "https://api.irishrail.ie/",  api_endpoint: str = "realtime/realtime.asmx/getAllStationsXML") -> List[Any]:
    """Get all Irish rail stations from the api
    Note api is in process of being deprecated so this will need to be changed at some point.
    """
    result = requests.get(base_url + api_endpoint)
    if not result.ok:
        logging.debug("Unable to get data from endpoint")
        return []

    elements = et.fromstring(result.content)
    stations: List[IrishRailStation] = []
    for el in elements:
        longitude = el.find('{http://api.irishrail.ie/realtime/}StationLongitude')
        latitude = el.find('{http://api.irishrail.ie/realtime/}StationLatitude')
        stationCode = el.find('{http://api.irishrail.ie/realtime/}StationCode')
        stationId = el.find('{http://api.irishrail.ie/realtime/}StationId')
        stationDesc = el.find('{http://api.irishrail.ie/realtime/}StationDesc')
        stationAlias = el.find('{http://api.irishrail.ie/realtime/}StationAlias')
        try:
            station = IrishRailStation(stationDesc.text, stationAlias.text or "", float(latitude.text),
            float(longitude.text), stationCode.text, stationId.text)
            stations.append(station)
        except Exception as err:
            logging.error(
                f"unable to convert element to irish rail station failed with error: {err}" )
    return stations


def main():
    stations = get_irish_rail_stations()
    json.dump([ x.__dict__ for x in stations], open( "./stations.json", 'w'))


if __name__ == "__main__":
    main()
