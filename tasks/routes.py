import re
import requests
import json
from flask import (Blueprint, render_template, current_app)
from geopy import distance as geopy_distance

from tasks.exceptions import (GeoTaskException, NoLocationFoundException, RemoteResponseException,
                              LocationBoundsUnavailable, LocationPositionNotSpecified,
                              InvalidAddressFormatException, EmptyAddressException)

task = Blueprint('task', __name__, template_folder='templates')

MKAD = 'mkad'


@task.get('/')
def index():
    address = 'Tverskaya+6'
    # address = 'lagos'
    log_address_distance_from_mkad(address)
    return render_template('task_index.html')


@task.errorhandler(GeoTaskException)
def handle_exceptions(err):
    return f'Error Processing your request -> {str(err)}'


def log_address_distance_from_mkad(address: str) -> None:
    """Logs distance of supplied address against MKAD."""
    mkad_info = get_address_members(MKAD)[0]
    params = _get_geocode_params(address)
    mkad_bounds = _extract_location_bounds(mkad_info)
    mkad_title = _get_location_info_title(mkad_info)
    # No need calculating address it within MKAD
    if not _address_is_within_mkad_bounds(address, mkad_bounds, params=params):
        address_members = get_address_members(address)
        for member in address_members:  # Multiple distances will be logged for multiple results
            member_title = _get_location_info_title(member)
            distance = _calculate_distance_between(mkad_info, member)
            distance = '{:,.2f}'.format(distance)
            message = f'Distance between "{mkad_title}" and "{member_title}" is approx {distance}km'
            current_app.logger.info(message)


def _calculate_distance_between(source: dict, destination: dict) -> int:
    source_point = source.get('GeoObject', {}).get('Point', {}).get('pos')
    destination_point = destination.get('GeoObject', {}).get('Point', {}).get('pos')
    if not source_point or not destination_point:
        raise LocationPositionNotSpecified()
    source_point = source_point.split()
    destination_point = destination_point.split()
    source_point = tuple([source_point[1], source_point[0]])
    destination_point = tuple([destination_point[1], destination_point[0]])
    # Distance calculated will be returned in kilometers
    return geopy_distance.distance(source_point, destination_point).km


def _extract_location_bounds(location_object: dict) -> dict:
    bounds = location_object.get('GeoObject', {}).get('boundedBy', {}).get('Envelope', {})
    if not any(['lowerCorner' in bounds.keys(), 'upperCorner' in bounds.keys()]):
        location_title = _get_location_info_title(location_object)
        raise LocationBoundsUnavailable(f'Unable to extract location bounds for address, "{location_title}"')
    return bounds


def _address_is_within_mkad_bounds(address: str, mkad_bounds: dict, params=None) -> bool:
    params = params or _get_geocode_params(address)
    lower_corner = ','.join(mkad_bounds.get('lowerCorner').split())
    upper_corner = ','.join(mkad_bounds.get('upperCorner').split())
    params.update({'bbox': f'{lower_corner}~{upper_corner}', 'rspn': 1})
    try:
        get_address_members(address, params=params)
        current_app.logger.warning(f'Address "{address}" is within MKAD, skipping distance calculation...')
        return True
    except NoLocationFoundException:
        return False


def get_address_members(address: str, params=None) -> list:
    """Fetch all locations from address supplied."""
    info = fetch_address_info(address, params=params)
    members = info.get('response', {}).get('GeoObjectCollection', {}).get('featureMember', [])
    if not members:
        raise NoLocationFoundException(f'No location found for address "{address}"')
    return members


def fetch_address_info(address: str, params=None) -> dict:
    """Retrieves address information from Yandex endpoint."""
    if not address:
        raise EmptyAddressException("Please enter a valid address")
    url = current_app.config.get('GEOCODE_API')
    if params is None:
        params = _get_geocode_params(address)
    response = requests.get(url, params=params,
                            timeout=current_app.config.get('GEOCODE_REQUEST_TIMEOUT', 5))
    if response.status_code != 200:
        raise RemoteResponseException(f'Invalid response from Geo endpoint -> {response.content}')
    return json.loads(response.content)


def _get_geocode_params(address: str) -> dict:
    params = {'apikey': current_app.config.get('GEOCODE_API_KEY'),
              'lang': 'en_US', 'format': 'json',
              'geocode': _clean_inputted_address(address)}
    return params


def _get_location_info_title(location_info: dict) -> str:
    return f'{location_info.get("GeoObject", {}).get("metaDataProperty", {}).get("GeocoderMetaData", {}).get("text")}'


def _clean_inputted_address(address: str) -> str:
    validate_address_is_not_coordinates(address)
    return address


def validate_address_is_not_coordinates(address: str) -> None:
    """Prevent Reverse Geocoding."""
    address = ','.join([i.strip() for i in address.strip().split(',')]).replace(';', ',')
    for coordinate_format in current_app.config.get('GEO_COORDINATE_FORMATS', []):
        pattern = re.compile(coordinate_format)
        if re.fullmatch(pattern, address):
            raise InvalidAddressFormatException("Coordinates not allowed at this time, "
                                                "please input a valid address")
