from django.http import HttpRequest

from .constants import CORP_ROLES


class IGBHeaders(object):
    def __init__(self, request):
        if not isinstance(request, HttpRequest):
            raise TypeError("Argument 'request' must be of type django.http.HttpRequest!")

        self._parse_igb_headers(request)

    def _get_corp_roles(self, corp_roles_bit_mask=0):
        """Returns the list of corp roles the player with the given
        'corp_roles_bit_mask' has. If the player does not have any corp roles
        an empty list will be returned.

        Keyword arguments:
        corp_roles_bit_mask -- the corp role bitmask from 'HTTP_EVE_CORPROLE' (default: 0)

        """
        roles = [role for role in CORP_ROLES if (role['id'] & corp_roles_bit_mask) > 0]

        return roles

    def _parse_igb_headers(self, request):
        """ Parses the HTTP_EVE_* headers from IGB and sets the header values as class attributes.

        Keyword arguments:
        request -- Django HttpRequest object
        """
        # More information on the headers can be found in CCPs documentation:
        # http://wiki.eveonline.com/en/wiki/IGB_Headers
        self.is_igb = True if 'HTTP_EVE_TRUSTED' in request.META else False

        # only do any further processing of it's the IGB
        if not self.is_igb:
            return

        self.trusted = True if request.META['HTTP_EVE_TRUSTED'] == 'Yes' else False

        # only if the user trusted the website the other HEADERS will be send by the IGB.
        if self.trusted:
            self.serverip = request.META['HTTP_EVE_SERVERIP']
            self.charname = request.META['HTTP_EVE_CHARNAME']
            self.charid = int(request.META['HTTP_EVE_CHARID'])
            self.corpname = request.META['HTTP_EVE_CORPNAME']
            self.corpid = int(request.META['HTTP_EVE_CORPID'])
            self.regionname = request.META['HTTP_EVE_REGIONNAME']
            self.constellationname = request.META['HTTP_EVE_CONSTELLATIONNAME']
            self.solarsystemid = int(request.META['HTTP_EVE_SOLARSYSTEMID'])
            self.solarsystemname = request.META['HTTP_EVE_SOLARSYSTEMNAME']
            self.shipid = int(request.META['HTTP_EVE_SHIPID'])
            self.shipname = request.META['HTTP_EVE_SHIPNAME']
            self.shiptypeid = int(request.META['HTTP_EVE_SHIPTYPEID'])
            self.shiptypename = request.META['HTTP_EVE_SHIPTYPENAME']

            # The following headers don't have to be set by the IGB.
            # That's why they are read from the request.META dict with get.
            # If the header is not set a sane default will be return.

            # Only set if the player has roles
            self.corprole = int(request.META.get('HTTP_EVE_CORPROLE', 0))
            self.corproles = self._get_corp_roles(self.corprole)
            
            # Only set if the players corporation is part of an alliance
            self.alliancename = request.META.get('HTTP_EVE_ALLIANCENAME', '')
            self.allianceid = int(request.META.get('HTTP_EVE_ALLIANCEID', 0))

            # Only set if the player is on a station
            self.stationname = request.META.get('HTTP_EVE_STATIONNAME', '')
            self.stationid = int(request.META.get('HTTP_EVE_STATIONID', 0))

            # Only set if the player is participating in factional warfare
            self.warfactionid = int(request.META.get('HTTP_EVE_WARFACTIONID', 0))

            # TODO: add additional attributes:
            # is_wormhole
            # is_on_station
            # is_factionwarfare
            # has_alliance
            # has_corproles