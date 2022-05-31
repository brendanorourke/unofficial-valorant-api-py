# This code is licensed under MIT license (see LICENSE.txt for details)
import json
import requests

from . import enums
from . import logger as _logging
from .utils import encode_uri, is_valid_act_filter, is_valid_country_code, is_valid_puuid, is_valid_region, retries

from urllib.parse import urlencode

class ValorantAPIPaths(object):
    ACCOUNT_DATA           = '/valorant/v1/account/{name}/{tag}'
    MMR_DATA               = '/valorant/v2/mrr/{name}/{tag}'
    MMR_DATA_BY_PUUID      = '/valorant/v2/by-puuid/mmr/{region}/{puuid}'
    MMR_HISTORY            = '/valorant/v1/mmr-history/{region}/{name}/{tag}'
    MMR_HISTORY_BY_PUUID   = '/valorant/v1/by-puuid/mmr-history/{region}/{puuid}'
    MATCH_HISTORY          = '/valorant/v3/matches/{region}/{name}/{tag}'
    MATCH_HISTORY_BY_PUUID = '/valorant/v3/by-puuid/matches/{region}/{puuid}'
    MATCH_DATA             = '/valorant/v2/match/{match_id}'
    WEBSITE_ARTICLES       = '/valorant/v1/website/{country_code}'
    LEADERBOARD            = '/valorant/v1/leaderboard/{region}'
    SERVER_STATUS          = '/valorant/v1/status/{region}'
    CONTENT                = '/valorant/v1/content'
    STORE_OFFERS           = '/valorant/v1/store-offers'
    STORE_FEATURED         = '/valorant/v1/store-featured'


class UnofficialValorantAPI(object):
    def __init__(self, logger=None):
        self._base_url = 'https://api.henrikdev.xyz'
        self._logger   = _logging.adapt_logger(logger or _logging.NoOpLogger())
        
        self._session         = requests.Session() 
        self._session.headers = {'User-Agent': 'Mozilla/5.0'}

    @retries(3)
    def _get(self, path, params=None):
        self._logger.info(f'GET: {path}{"?" + urlencode(params) if params is not None else ""}')
        return self._session.get(path, params=params)
    
    @retries(3)
    def _post(self, path, data):
        self._logger.info(f'POST: {path}')
        return self._session.post(path, data=json.dumps(data))

    def get_account_data(self, name, tag):
        """ Get general account data like puuid and account level. """
        path = self._base_url + ValorantAPIPaths.ACCOUNT_DATA.format(name=encode_uri(name), tag=encode_uri(tag))
        return self._get(path)
    
    def get_mmr_data(self, name, tag):
        """ Get mmr data about an user like current tier and last mmr change. """
        path = self._base_url + ValorantAPIPaths.MMR_DATA.format(name=encode_uri(name), tag=encode_uri(tag))
        return self._get(path)
    
    def get_mmr_data_by_puuid(self, region, puuid, filter=None):
        """ Get mmr data about an user like current tier and last mmr change. """
        if not is_valid_region(region):
            self._logger.error(enums.Errors.INVALID_REGION.format(region))
            return None

        if not is_valid_puuid(puuid):
            self._logger.error(enums.Errors.INVALID_PUUID.format(puuid))
            return None

        if not is_valid_act_filter(filter):
            self._logger.error(enums.Errors.INVALID_FILTER.format(filter))
            return None

        path = self._base_url + ValorantAPIPaths.MMR_DATA_BY_PUUID.format(region=region, puuid=puuid)
        
        return self._get(path, {'filter': filter})
    
    def get_mmr_history(self, region, name, tag):
        """ Get MMR History of the last competitive matches. """
        if not is_valid_region(region):
            self._logger.error(enums.Errors.INVALID_REGION.format(region))
            return None
        
        path = self._base_url + ValorantAPIPaths.MMR_HISTORY.format(region=region,
                                                                    name=encode_uri(name),
                                                                    tag=encode_uri(tag))
        
        return self._get(path)
    
    def get_mmr_history_by_puuid(self, region, puuid):
        """ Get mmr data about an user like current tier and last mmr change. """
        if not is_valid_region(region):
            self._logger.error(enums.Errors.INVALID_REGION.format(region))
            return None

        if not is_valid_puuid(puuid):
            self._logger.error(enums.Errors.INVALID_PUUID.format(puuid))
            return None
        
        path = self._base_url + ValorantAPIPaths.MMR_HISTORY_BY_PUUID.format(region=region, puuid=puuid)
        return self._get(path)

    def get_match_history(self, region, name, tag):
        """ Returns the last 5 matches that where played by this user. """
        if not is_valid_region(region):
            self._logger.error(enums.Errors.INVALID_REGION.format(region))
            return None
        
        path = self._base_url + ValorantAPIPaths.MATCH_HISTORY.format(region=region,
                                                                        name=encode_uri(name),
                                                                        tag=encode_uri(tag))
        return self._get(path)

    def get_match_history_by_puuid(self, region, puuid):
        """ Returns the last 5 matches that where played by this user. """
        if not is_valid_region(region):
            self._logger.error(enums.Errors.INVALID_REGION.format(region))
            return None
        
        if not is_valid_puuid(puuid):
            self._logger.error(enums.Errors.INVALID_PUUID.format(puuid))
            return None

        path = self._base_url + ValorantAPIPaths.MATCH_HISTORY_BY_PUUID.format(region=region, puuid=puuid)
        return self._get(path)
    
    def get_match_data(self, match_id):
        """ Returns match data for a specific match. """
        path = self._base_url + ValorantAPIPaths.MATCH_DATA.format(match_id=match_id)
        return self._get(path)
    
    def get_website_articles(self, country_code, filter=None):
        """ Get website articles based on your country code. """
        if not is_valid_country_code(country_code):
            self._logger.error(enums.Errors.INVALID_COUNTRY_CODE.format(country_code))
            return None

        path = self._base_url + ValorantAPIPaths.WEBSITE_ARTICLES.format(country_code=country_code)
        
        if filter in ['game_updates', 'dev', 'esports', 'announcements']:
            params = {'filter': filter}
        elif filter is None:
            params = {}
        else:
            self._logger.warning(enums.Errors.INVALID_FILTER.format(filter))
            params = {}

        return self._get(path, params)

    def get_leaderboard(self, region, name=None, tag=None):
        """ Returns leaderboard data for the given region. """
        if not is_valid_region(region):
            self._logger.error(enums.Errors.INVALID_REGION.format(region))
            return None
        
        path = self._base_url + ValorantAPIPaths.LEADERBOARD.format(region=region)
        
        if name is not None and tag is not None:
            params = {'name': encode_uri(name), 'tag': encode_uri(tag)}
        else:
            params = {}

        return self._get(path, params)

    def get_server_status(self, region):
        """ Returns server status for the given region. """
        if not is_valid_region(region):
            self._logger.error(enums.Errors.INVALID_REGION.format(region))
            return None
        
        path = self._base_url + ValorantAPIPaths.SERVER_STATUS.format(region=region)
        return self._get(path)

    def get_content(self):
        """ Returns Ingame Content. """
        path = self._base_url + ValorantAPIPaths.CONTENT
        return self._get(path)

    def get_store_offers(self):
        """ Returns all available store offers. """
        path = self._base_url + ValorantAPIPaths.STORE_OFFERS
        return self._get(path)
    
    def get_store_featured(self):
        """ Returns the featured ingame shop offers. """
        path = self._base_url + ValorantAPIPaths.STORE_FEATURED
        return self._get(path)
