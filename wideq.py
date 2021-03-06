import requests
from urllib.parse import urljoin, urlencode, urlparse, parse_qs
import uuid
import base64
import json
import hashlib
import hmac
import datetime
from collections import namedtuple
import enum
import time

GATEWAY_URL = 'https://kic.lgthinq.com:46030/api/common/gatewayUriList'
APP_KEY = 'wideq'
SECURITY_KEY = 'nuts_securitykey'
DATA_ROOT = 'lgedmRoot'
COUNTRY = 'US'
LANGUAGE = 'en-US'
SVC_CODE = 'SVC202'
CLIENT_ID = 'LGAO221A02'
OAUTH_SECRET_KEY = 'c053c2a6ddeb7ad97cb0eed0dcb31cf8'
OAUTH_CLIENT_KEY = 'LGAO221A02'
DATE_FORMAT = '%a, %d %b %Y %H:%M:%S +0000'

"""HVAC STATE"""
STATE_COOL = 'COOL'
STATE_DRY = 'DRY'
STATE_AIRCLEAN = 'ON'
STATE_AIRCLEAN_OFF = 'OFF'
STATE_SMARTCARE = 'ON'
STATE_SMARTCARE_OFF = 'OFF'
STATE_AUTODRY = 'ON'
STATE_AUTODRY_OFF = 'OFF'
STATE_POWERSAVE = 'ON'
STATE_POWERSAVE_OFF = 'OFF'
STATE_COOLPOWER = 'ON'
STATE_COOLPOWER_OFF = 'OFF'
STATE_LONGPOWER = 'ON'
STATE_LONGPOWER_OFF = 'OFF'

STATE_LOW = 'LOW'
STATE_MID = 'MEDIUM'
STATE_HIGH = 'HIGH'
STATE_RIGHT_LOW_LEFT_MID = 'LLM'
STATE_RIGHT_LOW_LEFT_HIGH = 'LLH'
STATE_RIGHT_MID_LEFT_LOW = 'MLL'
STATE_RIGHT_MID_LEFT_HIGH = 'MLH'
STATE_RIGHT_HIGH_LEFT_LOW = 'HLL'
STATE_RIGHT_HIGH_LEFT_MID = 'HLM'
STATE_RIGHT_ONLY_LOW = 'ROL'
STATE_RIGHT_ONLY_MID = 'ROM'
STATE_RIGHT_ONLY_HIGH = 'ROH'
STATE_LEFT_ONLY_LOW = 'LOL'
STATE_LEFT_ONLY_MID = 'LOM'
STATE_LEFT_ONLY_HIGH = 'LOH'

STATE_LEFT_RIGHT = 'L/R'
STATE_RIGHTSIDE_LEFT_RIGHT = 'R L/R'
STATE_LEFTSIDE_LEFT_RIGHT = 'L R/L'
STATE_LEFT_RIGHT_STOP = 'LRS'

STATE_UP_DOWN = 'ON'
STATE_UP_DOWN_STOP = 'OFF'

"""REFRIGERATOR STATE"""
STATE_ICE_PLUS = '켜짐'
STATE_ICE_PLUS_OFF = '꺼짐'

STATE_FRESH_AIR_FILTER_REPLACE_FILTER = '필터교체필요'
STATE_FRESH_AIR_FILTER_SMART_CARE_ON = '켜짐'
STATE_FRESH_AIR_FILTER_SMART_CARE_OFF = '꺼짐'
STATE_FRESH_AIR_FILTER_SMART_CARE_WAIT = '대기'
STATE_FRESH_AIR_FILTER_POWER = '파워'
STATE_FRESH_AIR_FILTER_AUTO = '자동'
STATE_FRESH_AIR_FILTER_OFF = '꺼짐'


STATE_SMART_SAVING_NIGHT = 'NIGHT'
STATE_SMART_SAVING_CUSTOM = 'CUSTOM'
STATE_SMART_SAVING_OFF = 'OFF'

STATE_REF_WATERFILTER_OK = '정상'
STATE_REF_WATERFILTER_REPLACE = '교체필요'
STATE_REF_WATERFILTER_NO_FILTER = '정수기없음'

STATE_REF_ACTIVESAVING_ZERO = '0'
STATE_REF_ACTIVESAVING_ONE = '1'
STATE_REF_ACTIVESAVING_TWO = '2'
STATE_REF_ACTIVESAVING_THREE = '3'

"""DRYER STATE"""
STATE_DRYER_POWER_OFF = '꺼짐'
STATE_DRYER_INITIAL = '코스선택'
STATE_DRYER_RUNNING = '가동중'
STATE_DRYER_PAUSE = '일시정지'
STATE_DRYER_END = '종료'
STATE_DRYER_ERROR = '에러'

STATE_DRYER_PROCESS_DETECTING = '세탁물감지중'
STATE_DRYER_PROCESS_STEAM = '스팀중'
STATE_DRYER_PROCESS_DRY = '건조중'
STATE_DRYER_PROCESS_COOLING = '송풍'
STATE_DRYER_PROCESS_ANTI_CREASE = '구김방지'
STATE_DRYER_PROCESS_END = '종료'

STATE_DRY_LEVEL_IRON = '약'
STATE_DRY_LEVEL_CUPBOARD = '표준'
STATE_DRY_LEVEL_EXTRA = '강력'

STATE_ECOHYBRID_ECO = '에너지'
STATE_ECOHYBRID_NORMAL = '표준'
STATE_ECOHYBRID_TURBO = '스피드'

STATE_COURSE_COTTON_SOFT = '타월'
STATE_COURSE_BULKY_ITEM = '이불'
STATE_COURSE_EASY_CARE = '셔츠'
STATE_COURSE_COTTON = '표준'
STATE_COURSE_SPORTS_WEAR = '기능성의류'
STATE_COURSE_QUICK_DRY = '소량급속'
STATE_COURSE_WOOL = '울/섬세'
STATE_COURSE_RACK_DRY = '선반건조'
STATE_COURSE_COOL_AIR = '송풍'
STATE_COURSE_WARM_AIR = '온풍'
STATE_COURSE_BEDDING_BRUSH = '침구털기'
STATE_COURSE_STERILIZATION = '살균'
STATE_COURSE_REFRESH = '리프레쉬'
STATE_COURSE_POWER = '강력'

STATE_SMARTCOURSE_GYM_CLOTHES = '운동복'
STATE_SMARTCOURSE_RAINY_SEASON = '장마철'
STATE_SMARTCOURSE_DEODORIZATION = '리프레쉬'
STATE_SMARTCOURSE_SMALL_LOAD = '소량 건조'
STATE_SMARTCOURSE_LINGERIE = '란제리'
STATE_SMARTCOURSE_EASY_IRON = '촉촉 건조'
STATE_SMARTCOURSE_SUPER_DRY = '강력 건조'
STATE_SMARTCOURSE_ECONOMIC_DRY = '절약 건조'
STATE_SMARTCOURSE_BIG_SIZE_ITEM = '큰 빨래 건조'
STATE_SMARTCOURSE_MINIMIZE_WRINKLES = '구김 완화 건조'
STATE_SMARTCOURSE_FULL_SIZE_LOAD = '다량건조'
STATE_SMARTCOURSE_JEAN = '청바지'

STATE_ERROR_DOOR = '문열림 에러 - 문이 닫혔는지 확인하세요'
STATE_ERROR_DRAINMOTOR = '배수펌프 에러 - 배수라인이 동결되었는지 확인하세요'
STATE_ERROR_LE1 = '과부하 에러 - 세탁물 양을 확인하세요'
STATE_ERROR_TE1 = '온도센서 에러 - 서비스 센터에 문의하세요'
STATE_ERROR_TE2 = '온도센서 에러 - 서비스 센터에 문의하세요'
STATE_ERROR_F1 = '과온 에러 - 서비스 센터에 문의하세요'
STATE_ERROR_LE2 = '컴프레서 에러 - 서비스 센터에 문의하세요'
STATE_ERROR_AE = '컴프레서 에러 - 서비스 센터에 문의하세요'
STATE_ERROR_dE4 = 'ERROR_dE4'
STATE_ERROR_NOFILTER = '필터 없음 - 필터를 삽입해 주세요'
STATE_ERROR_EMPTYWATER = '물통 가득참 - 물통을 비워주세요'
STATE_ERROR_CE1 = 'ERROR_CE1'
STATE_NO_ERROR = '정상'

STATE_OPTIONITEM_ON = '켜짐'
STATE_OPTIONITEM_OFF = '꺼짐'

"""WASHER STATE"""
STATE_WASHER_POWER_OFF = '꺼짐'
STATE_WASHER_INITIAL = '코스선택'
STATE_WASHER_PAUSE = '일시정지'
STATE_WASHER_ERROR_AUTO_OFF = '에러_자동종료'
STATE_WASHER_RESERVE = '예약중'
STATE_WASHER_DETECTING = '세탁물 감지 중'
STATE_WASHER_ADD_DRAIN = 'ADD_DRAIN'
STATE_WASHER_DETERGENT_AMOUT = '세제량'
STATE_WASHER_RUNNING = '세탁 중'
STATE_WASHER_PREWASH = '애벌세탁 중'
STATE_WASHER_RINSING = '헹굼 중'
STATE_WASHER_RINSE_HOLD = '헹굼 대기'
STATE_WASHER_SPINNING = '탈수 중'
STATE_WASHER_DRYING = '건조 중'
STATE_WASHER_END = '종료'
STATE_WASHER_FRESHCARE = 'FreshCare'
STATE_WASHER_TCL_ALARM_NORMAL = '통세척'
STATE_WASHER_FROZEN_PREVENT_INITIAL = '동파방지_초기화'
STATE_WASHER_FROZEN_PREVENT_RUNNING = '동파방지_동작중'
STATE_WASHER_FROZEN_PREVENT_PAUSE = '동파방지_일시정지'
STATE_WASHER_ERROR = '에러'

STATE_WASHER_SOILLEVEL_LIGHT = '적은때'
STATE_WASHER_SOILLEVEL_NORMAL = '표준'
STATE_WASHER_SOILLEVEL_HEAVY = '강력'
STATE_WASHER_SOILLEVEL_PRE_WASH = '애벌세탁'
STATE_WASHER_SOILLEVEL_SOAKING = '불림'

STATE_WASHER_WATERTEMP_COLD = '냉수'
STATE_WASHER_WATERTEMP_30 = '30℃'
STATE_WASHER_WATERTEMP_40 = '40℃'
STATE_WASHER_WATERTEMP_60 = '60℃'
STATE_WASHER_WATERTEMP_95 = '95℃'

STATE_WASHER_SPINSPEED_EXTRA_LOW = '섬세'
STATE_WASHER_SPINSPEED_LOW = '약'
STATE_WASHER_SPINSPEED_MEDIUM = '중'
STATE_WASHER_SPINSPEED_HIGH = '강'
STATE_WASHER_SPINSPEED_EXTRA_HIGH = '건조맞춤'

STATE_WASHER_RINSECOUNT_1 = '1회'
STATE_WASHER_RINSECOUNT_2 = '2회'
STATE_WASHER_RINSECOUNT_3 = '3회'
STATE_WASHER_RINSECOUNT_4 = '4회'
STATE_WASHER_RINSECOUNT_5 = '5회'

STATE_WASHER_DRYLEVEL_WIND = '바람건조'
STATE_WASHER_DRYLEVEL_TURBO = '터보건조'
STATE_WASHER_DRYLEVEL_TIME_30 = '시간건조_30분'
STATE_WASHER_DRYLEVEL_TIME_60 = '시간건조_60분'
STATE_WASHER_DRYLEVEL_TIME_90 = '시간건조_90분'
STATE_WASHER_DRYLEVEL_TIME_120 = '시간건조_120분'
STATE_WASHER_DRYLEVEL_TIME_150 = '시간건조_150분'

STATE_WASHER_NO_ERROR = '정상'
STATE_WASHER_ERROR_dE2 = '문열림 에러 - 문이 닫혔는지 확인하세요'
STATE_WASHER_ERROR_IE = '급수안됨'
STATE_WASHER_ERROR_OE = '배수안됨'
STATE_WASHER_ERROR_UE = '세탁물 치우침'
STATE_WASHER_ERROR_FE = 'FE - 서비스 센터에 문의하세요'
STATE_WASHER_ERROR_PE = 'PE - 서비스 센터에 문의하세요'
STATE_WASHER_ERROR_LE = 'LE - 서비스 센터에 문의하세요'
STATE_WASHER_ERROR_tE = 'tE - 서비스 센터에 문의하세요'
STATE_WASHER_ERROR_dHE = 'dHE - 서비스 센터에 문의하세요'
STATE_WASHER_ERROR_CE = 'CE - 서비스 센터에 문의하세요'
STATE_WASHER_ERROR_PF = 'PF - 서비스 센터에 문의하세요'
STATE_WASHER_ERROR_FF = '제품 얼음'
STATE_WASHER_ERROR_dCE = 'dCE - 서비스 센터에 문의하세요'
STATE_WASHER_ERROR_EE = 'EE - 서비스 센터에 문의하세요'
STATE_WASHER_ERROR_PS = 'PS - 서비스 센터에 문의하세요'
STATE_WASHER_ERROR_dE1 = '문열림 에러 - 문이 닫혔는지 확인하세요'
STATE_WASHER_ERROR_LOE = '세제통 문열림 에러 - 세제통 문이 닫혔는지 확인하세요'

STATE_WASHER_APCOURSE_COTTON = '표준세탁'
STATE_WASHER_APCOURSE_SPEEDWASH_DRY = '스피드워시+건조'
STATE_WASHER_APCOURSE_SPEEDWASH = '스피드워시'
STATE_WASHER_APCOURSE_SINGLE_SHIRT_DRY = '셔츠한벌건조'
STATE_WASHER_APCOURSE_RINSESPIN = '헹굼+탈수'
STATE_WASHER_APCOURSE_SPEEDBOIL = '알뜰삶음'
STATE_WASHER_APCOURSE_ALLERGYCARE = '알러지케어'
STATE_WASHER_APCOURSE_STEAMCLEANING = '스팀클리닝'
STATE_WASHER_APCOURSE_BABYWEAR = '아기옷'
STATE_WASHER_APCOURSE_BLANKET_ROB = '이불살균털기'
STATE_WASHER_APCOURSE_UTILITY = '기능성의류'
STATE_WASHER_APCOURSE_BLANKET = '이불'
STATE_WASHER_APCOURSE_LINGERIE_WOOL = '란제리/울'
STATE_WASHER_APCOURSE_COLDWASH = '찬물세탁'
STATE_WASHER_APCOURSE_TUBCLEAN_SANITARY = '통살균'
STATE_WASHER_APCOURSE_DOWNLOAD_COUSE = '다운로드코스'

STATE_WASHER_SMARTCOURSE_SILENT = '조용조용'
STATE_WASHER_SMARTCOURSE_SMALL_LOAD = '소량 세탁'
STATE_WASHER_SMARTCOURSE_SKIN_CARE = '스킨 케어'
STATE_WASHER_SMARTCOURSE_RAINY_SEASON = '장마철 세탁'
STATE_WASHER_SMARTCOURSE_SWEAT_STAIN = '땀얼룩 제거'
STATE_WASHER_SMARTCOURSE_SINGLE_GARMENT = '한벌 세탁'
STATE_WASHER_SMARTCOURSE_SCHOOL_UNIFORM = '교복'
STATE_WASHER_SMARTCOURSE_STATIC_REMOVAL = '정전기 제거'
STATE_WASHER_SMARTCOURSE_COLOR_CARE = '컬러 케어'
STATE_WASHER_SMARTCOURSE_SPIN_ONLY = '탈수 전용'
STATE_WASHER_SMARTCOURSE_DEODORIZATION = '냄새 제거'
STATE_WASHER_SMARTCOURSE_BEDDING_CARE = '침구 케어'
STATE_WASHER_SMARTCOURSE_CLOTH_CARE = '옷감 보호'
STATE_WASHER_SMARTCOURSE_SMART_RINSE = '안심 헹굼'
STATE_WASHER_SMARTCOURSE_ECO_WASH = '알뜰 세탁'

STATE_WASHER_TERM_NO_SELECT = '선택 안함'

STATE_WASHER_OPTIONITEM_ON = '켜짐'
STATE_WASHER_OPTIONITEM_OFF = '꺼짐'

"""DEHUMIDIFIER STATE"""
STATE_DEHUM_ON = '동작 중'
STATE_DEHUM_OFF = '꺼짐'

STATE_DEHUM_OPMODE_SMART_DEHUM = '스마트제습'
STATE_DEHUM_OPMODE_FAST_DEHUM = '쾌속제습'
STATE_DEHUM_OPMODE_SILENT_DEHUM = '저소음제습'
STATE_DEHUM_OPMODE_CONCENTRATION_DRY = '집중건조'
STATE_DEHUM_OPMODE_CLOTHING_DRY = '의류건조'
STATE_DEHUM_OPMODE_IONIZER = '공기제균'

STATE_DEHUM_WINDSTRENGTH_LOW = '약풍'
STATE_DEHUM_WIDESTRENGTH_HIGH = '강풍'

STATE_DEHUM_AIRREMOVAL_ON = '켜짐'
STATE_DEHUM_AIRREMOVAL_OFF = '꺼짐'


def gen_uuid():
    return str(uuid.uuid4())


def oauth2_signature(message, secret):
    """Get the base64-encoded SHA-1 HMAC digest of a string, as used in
    OAauth2 request signatures.

    Both the `secret` and `message` are given as text strings. We use
    their UTF-8 equivalents.
    """

    secret_bytes = secret.encode('utf8')
    hashed = hmac.new(secret_bytes, message.encode('utf8'), hashlib.sha1)
    digest = hashed.digest()
    return base64.b64encode(digest)


def as_list(obj):
    """Wrap non-lists in lists.

    If `obj` is a list, return it unchanged. Otherwise, return a
    single-element list containing it.
    """

    if isinstance(obj, list):
        return obj
    else:
        return [obj]


class APIError(Exception):
    """An error reported by the API."""

    def __init__(self, code, message):
        self.code = code
        self.message = message


class NotLoggedInError(APIError):
    """The session is not valid or expired."""

    def __init__(self):
        pass


class TokenError(APIError):
    """An authentication token was rejected."""

    def __init__(self):
        pass


class MonitorError(APIError):
    """Monitoring a device failed, possibly because the monitoring
    session failed and needs to be restarted.
    """

    def __init__(self, device_id, code):
        self.device_id = device_id
        self.code = code

class NotConnectError(APIError):
    """The session is not valid or expired."""

    def __init__(self):
        pass


def lgedm_post(url, data=None, access_token=None, session_id=None):
    """Make an HTTP request in the format used by the API servers.

    In this format, the request POST data sent as JSON under a special
    key; authentication sent in headers. Return the JSON data extracted
    from the response.

    The `access_token` and `session_id` are required for most normal,
    authenticated requests. They are not required, for example, to load
    the gateway server data or to start a session.
    """

    headers = {
        'x-thinq-application-key': APP_KEY,
        'x-thinq-security-key': SECURITY_KEY,
        'Accept': 'application/json',
    }
    if access_token:
        headers['x-thinq-token'] = access_token
    if session_id:
        headers['x-thinq-jsessionId'] = session_id

    res = requests.post(url, json={DATA_ROOT: data}, headers=headers)
    out = res.json()[DATA_ROOT]

    # Check for API errors.
    if 'returnCd' in out:
        code = out['returnCd']
        if code != '0000':
            message = out['returnMsg']
            if code == "0102":
                raise NotLoggedInError()
            elif code == "0106":
                raise NotConnectError()
            else:
                raise APIError(code, message)


    return out


def gateway_info():
    """Load information about the hosts to use for API interaction.
    """

    return lgedm_post(
        GATEWAY_URL,
        {'countryCode': COUNTRY, 'langCode': LANGUAGE},
    )


def oauth_url(auth_base):
    """Construct the URL for users to log in (in a browser) to start an
    authenticated session.
    """

    url = urljoin(auth_base, 'login/sign_in')
    query = urlencode({
        'country': COUNTRY,
        'language': LANGUAGE,
        'svcCode': SVC_CODE,
        'authSvr': 'oauth2',
        'client_id': CLIENT_ID,
        'division': 'ha',
        'grant_type': 'password',
    })
    return '{}?{}'.format(url, query)


def parse_oauth_callback(url):
    """Parse the URL to which an OAuth login redirected to obtain two
    tokens: an access token for API credentials, and a refresh token for
    getting updated access tokens.
    """

    params = parse_qs(urlparse(url).query)
    return params['access_token'][0], params['refresh_token'][0]


def login(api_root, access_token):
    """Use an access token to log into the API and obtain a session and
    return information about the session.
    """

    url = urljoin(api_root + '/', 'member/login')
    data = {
        'countryCode': COUNTRY,
        'langCode': LANGUAGE,
        'loginType': 'EMP',
        'token': access_token,
    }
    return lgedm_post(url, data)


def refresh_auth(oauth_root, refresh_token):
    """Get a new access_token using a refresh_token.

    May raise a `TokenError`.
    """

    token_url = urljoin(oauth_root, '/oauth2/token')
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }

    # The timestamp for labeling OAuth requests can be obtained
    # through a request to the date/time endpoint:
    # https://us.lgeapi.com/datetime
    # But we can also just generate a timestamp.
    timestamp = datetime.datetime.utcnow().strftime(DATE_FORMAT)

    # The signature for the requests is on a string consisting of two
    # parts: (1) a fake request URL containing the refresh token, and (2)
    # the timestamp.
    req_url = ('/oauth2/token?grant_type=refresh_token&refresh_token=' +
               refresh_token)
    sig = oauth2_signature('{}\n{}'.format(req_url, timestamp),
                           OAUTH_SECRET_KEY)

    headers = {
        'lgemp-x-app-key': OAUTH_CLIENT_KEY,
        'lgemp-x-signature': sig,
        'lgemp-x-date': timestamp,
        'Accept': 'application/json',
    }

    res = requests.post(token_url, data=data, headers=headers)
    res_data = res.json()

    if res_data['status'] != 1:
        raise TokenError()
    return res_data['access_token']


class Gateway(object):
    def __init__(self, auth_base, api_root, oauth_root):
        self.auth_base = auth_base
        self.api_root = api_root
        self.oauth_root = oauth_root

    @classmethod
    def discover(cls):
        gw = gateway_info()
        return cls(gw['empUri'], gw['thinqUri'], gw['oauthUri'])

    def oauth_url(self):
        return oauth_url(self.auth_base)


class Auth(object):
    def __init__(self, gateway, access_token, refresh_token):
        self.gateway = gateway
        self.access_token = access_token
        self.refresh_token = refresh_token

    @classmethod
    def from_url(cls, gateway, url):
        """Create an authentication using an OAuth callback URL.
        """

        access_token, refresh_token = parse_oauth_callback(url)
        return cls(gateway, access_token, refresh_token)

    def start_session(self):
        """Start an API session for the logged-in user. Return the
        Session object and a list of the user's devices.
        """

        session_info = login(self.gateway.api_root, self.access_token)
        session_id = session_info['jsessionId']
        return Session(self, session_id), as_list(session_info['item'])

    def refresh(self):
        """Refresh the authentication, returning a new Auth object.
        """

        new_access_token = refresh_auth(self.gateway.oauth_root,
                                        self.refresh_token)
        return Auth(self.gateway, new_access_token, self.refresh_token)


class Session(object):
    def __init__(self, auth, session_id):
        self.auth = auth
        self.session_id = session_id

    def post(self, path, data=None):
        """Make a POST request to the API server.

        This is like `lgedm_post`, but it pulls the context for the
        request from an active Session.
        """

        url = urljoin(self.auth.gateway.api_root + '/', path)
        return lgedm_post(url, data, self.auth.access_token, self.session_id)

    def get_devices(self):
        """Get a list of devices associated with the user's account.

        Return a list of dicts with information about the devices.
        """

        return as_list(self.post('device/deviceList')['item'])

    def monitor_start(self, device_id):
        """Begin monitoring a device's status.

        Return a "work ID" that can be used to retrieve the result of
        monitoring.
        """

        res = self.post('rti/rtiMon', {
            'cmd': 'Mon',
            'cmdOpt': 'Start',
            'deviceId': device_id,
            'workId': gen_uuid(),
        })
        return res['workId']

    def monitor_poll(self, device_id, work_id):
        """Get the result of a monitoring task.

        `work_id` is a string ID retrieved from `monitor_start`. Return
        a status result, which is a bytestring, or None if the
        monitoring is not yet ready.

        May raise a `MonitorError`, in which case the right course of
        action is probably to restart the monitoring task.
        """

        work_list = [{'deviceId': device_id, 'workId': work_id}]
        res = self.post('rti/rtiResult', {'workList': work_list})['workList']

        # The return data may or may not be present, depending on the
        # monitoring task status.
        if 'returnData' in res:
            # The main response payload is base64-encoded binary data in
            # the `returnData` field. This sometimes contains JSON data
            # and sometimes other binary data.
            return base64.b64decode(res['returnData'])
        else:
            return None
         # Check for errors.
        code = res.get('returnCode')  # returnCode can be missing.
        if code != '0000':
            raise MonitorError(device_id, code)


    def monitor_stop(self, device_id, work_id):
        """Stop monitoring a device."""

        self.post('rti/rtiMon', {
            'cmd': 'Mon',
            'cmdOpt': 'Stop',
            'deviceId': device_id,
            'workId': work_id,
        })

    def set_device_controls(self, device_id, values):
        """Control a device's settings.

        `values` is a key/value map containing the settings to update.
        """

        return self.post('rti/rtiControl', {
            'cmd': 'Control',
            'cmdOpt': 'Set',
            'value': values,
            'deviceId': device_id,
            'workId': gen_uuid(),
            'data': '',
        })

    def get_device_config(self, device_id, key, category='Config'):
        """Get a device configuration option.

        The `category` string should probably either be "Config" or
        "Control"; the right choice appears to depend on the key.
        """

        res = self.post('rti/rtiControl', {
            'cmd': category,
            'cmdOpt': 'Get',
            'value': key,
            'deviceId': device_id,
            'workId': gen_uuid(),
            'data': '',
        })
        return res['returnData']

    def delete_permission(self, device_id):
        self.post('rti/delControlPermission', {
            'deviceId': device_id,
        })

class Monitor(object):
    """A monitoring task for a device.
        
        This task is robust to some API-level failures. If the monitoring
        task expires, it attempts to start a new one automatically. This
        makes one `Monitor` object suitable for long-term monitoring.
        """
    
    def __init__(self, session, device_id):
        self.session = session
        self.device_id = device_id
    
    def start(self):
        self.work_id = self.session.monitor_start(self.device_id)
    
    def stop(self):
        self.session.monitor_stop(self.device_id, self.work_id)
    
    def poll(self):
        """Get the current status data (a bytestring) or None if the
            device is not yet ready.
            """
        self.work_id = self.session.monitor_start(self.device_id)
        try:
            return self.session.monitor_poll(self.device_id, self.work_id)
        except MonitorError:
            # Try to restart the task.
            self.stop()
            self.start()
            return None


    @staticmethod
    def decode_json(data):
        """Decode a bytestring that encodes JSON status data."""
        
        return json.loads(data.decode('utf8'))
    
    def poll_json(self):
        """For devices where status is reported via JSON data, get the
            decoded status result (or None if status is not available).
            """
        
        data = self.poll()
        return self.decode_json(data) if data else None
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, type, value, tb):
        self.stop()


class Client(object):
    """A higher-level API wrapper that provides a session more easily
        and allows serialization of state.
        """
    
    def __init__(self, gateway=None, auth=None, session=None):
        # The three steps required to get access to call the API.
        self._gateway = gateway
        self._auth = auth
        self._session = session
        
        # The last list of devices we got from the server. This is the
        # raw JSON list data describing the devices.
        self._devices = None
        
        # Cached model info data. This is a mapping from URLs to JSON
        # responses.
        self._model_info = {}
    
    @property
    def gateway(self):
        if not self._gateway:
            self._gateway = Gateway.discover()
        return self._gateway
    
    @property
    def auth(self):
        if not self._auth:
            assert False, "unauthenticated"
        return self._auth
    
    @property
    def session(self):
        if not self._session:
            self._session, self._devices = self.auth.start_session()
        return self._session
    
    @property
    def devices(self):
        """DeviceInfo objects describing the user's devices.
            """
        
        if not self._devices:
            self._devices = self.session.get_devices()
        return (DeviceInfo(d) for d in self._devices)
    
    def get_device(self, device_id):
        """Look up a DeviceInfo object by device ID.
            
            Return None if the device does not exist.
            """
        
        for device in self.devices:
            if device.id == device_id:
                return device
        return None
    
    @classmethod
    def load(cls, state):
        """Load a client from serialized state.
            """
        
        client = cls()
        
        if 'gateway' in state:
            data = state['gateway']
            client._gateway = Gateway(
            data['auth_base'], data['api_root'], data['oauth_root']
            )
        
        if 'auth' in state:
            data = state['auth']
            client._auth = Auth(
            client.gateway, data['access_token'], data['refresh_token']
            )
        
        if 'session' in state:
            client._session = Session(client.auth, state['session'])
                
        if 'model_info' in state:
            client._model_info = state['model_info']
                
        return client

    def dump(self):
        """Serialize the client state."""
        
        out = {
            'model_info': self._model_info,
        }
        
        if self._gateway:
            out['gateway'] = {
                'auth_base': self._gateway.auth_base,
                'api_root': self._gateway.api_root,
                'oauth_root': self._gateway.oauth_root,
        }
        
        if self._auth:
            out['auth'] = {
                'access_token': self._auth.access_token,
                'refresh_token': self._auth.refresh_token,
        }

        if self._session:
            out['session'] = self._session.session_id

        return out
    
    def refresh(self):
        self._auth = self.auth.refresh()
        self._session, self._devices = self.auth.start_session()
    
    @classmethod
    def from_token(cls, refresh_token):
        """Construct a client using just a refresh token.
            
            This allows simpler state storage (e.g., for human-written
            configuration) but it is a little less efficient because we need
            to reload the gateway servers and restart the session.
            """
        
        client = cls()
        client._auth = Auth(client.gateway, None, refresh_token)
        client.refresh()
        return client
    
    def model_info(self, device):
        """For a DeviceInfo object, get a ModelInfo object describing
            the model's capabilities.
            """
        url = device.model_info_url
        if url not in self._model_info:
            self._model_info[url] = device.load_model_info()
        return ModelInfo(self._model_info[url])


class DeviceType(enum.Enum):
    """The category of device."""
    
    REFRIGERATOR = 101
    KIMCHI_REFRIGERATOR = 102
    WATER_PURIFIER = 103
    WASHER = 201
    DRYER = 202
    STYLER = 203
    DISHWASHER = 204
    OVEN = 301
    MICROWAVE = 302
    COOKTOP = 303
    HOOD = 304
    AC = 401
    AIR_PURIFIER = 402
    DEHUMIDIFIER = 403
    ROBOT_KING = 501
    ARCH = 1001
    MISSG = 3001
    SENSOR = 3002
    SOLAR_SENSOR = 3102
    IOT_LIGHTING = 3003
    IOT_MOTION_SENSOR = 3004
    IOT_SMART_PLUG = 3005
    IOT_DUST_SENSOR = 3006
    EMS_AIR_STATION = 4001
    AIR_SENSOR = 4003


class DeviceInfo(object):
    """Details about a user's device.
        
    This is populated from a JSON dictionary provided by the API.
    """
    
    def __init__(self, data):
        self.data = data
    
    @property
    def model_id(self):
        return self.data['modelNm']
    
    @property
    def id(self):
        return self.data['deviceId']
    
    @property
    def model_info_url(self):
        return self.data['modelJsonUrl']
    
    @property
    def name(self):
        return self.data['alias']
    
    @property
    def type(self):
        """The kind of device, as a `DeviceType` value."""
        
        return DeviceType(self.data['deviceType'])
    
    def load_model_info(self):
        """Load JSON data describing the model's capabilities.
        """
        return requests.get(self.model_info_url).json()


EnumValue = namedtuple('EnumValue', ['options'])
RangeValue = namedtuple('RangeValue', ['min', 'max', 'step'])
BitValue = namedtuple('BitValue', ['options'])
ReferenceValue = namedtuple('ReferenceValue', ['reference'])


class ModelInfo(object):
    """A description of a device model's capabilities.
        """
    
    def __init__(self, data):
        self.data = data
    
    def value_type(self, name):
        if name in self.data['Value']:
            return self.data['Value'][name]['type']
        else:
            return None

    def value(self, name):
        """Look up information about a value.
        
        Return either an `EnumValue` or a `RangeValue`.
        """
        d = self.data['Value'][name]
        if d['type'] in ('Enum', 'enum'):
            return EnumValue(d['option'])
        elif d['type'] == 'Range':
            return RangeValue(d['option']['min'], d['option']['max'], d['option']['step'])
        elif d['type'] == 'Bit':
            bit_values = {}
            for bit in d['option']:
                bit_values[bit['startbit']] = {
                'value' : bit['value'],
                'length' : bit['length'],
                }
            return BitValue(
                    bit_values
                    )
        elif d['type'] == 'Reference':
            ref =  d['option'][0]
            return ReferenceValue(
                    self.data[ref]
                    )
        elif d['type'] == 'Boolean':
            return EnumValue({'0': 'False', '1' : 'True'})
        elif d['type'] == 'String':
            pass 
        else:
            assert False, "unsupported value type {}".format(d['type'])


    def default(self, name):
        """Get the default value, if it exists, for a given value.
        """
            
        return self.data['Value'][name]['default']
        
    def enum_value(self, key, name):
        """Look up the encoded value for a friendly enum name.
        """
        
        options = self.value(key).options
        options_inv = {v: k for k, v in options.items()}  # Invert the map.
        return options_inv[name]

    def enum_name(self, key, value):
        """Look up the friendly enum name for an encoded value.
        """
        if not self.value_type(key):
            return str(value)
                
        options = self.value(key).options
        return options[value]

    def range_name(self, key):
        """Look up the value of a RangeValue.  Not very useful other than for comprehension
        """
            
        return key
        
    def bit_name(self, key, bit_index, value):
        """Look up the friendly name for an encoded bit value
        """
        if not self.value_type(key):
            return str(value)
        
        options = self.value(key).options
        
        if not self.value_type(options[bit_index]['value']):
            return str(value)
        
        enum_options = self.value(options[bit_index]['value']).options
        return enum_options[value]

    def reference_name(self, key, value):
        """Look up the friendly name for an encoded reference value
        """
        value = str(value)
        if not self.value_type(key):
            return value
                
        reference = self.value(key).reference
                    
        if value in reference:
            comment = reference[value]['_comment']
            return comment if comment else reference[value]['label']
        else:
            return '-'

    @property
    def binary_monitor_data(self):
        """Check that type of monitoring is BINARY(BYTE).
        """
        
        return self.data['Monitoring']['type'] == 'BINARY(BYTE)'
    
    def decode_monitor_binary(self, data):
        """Decode binary encoded status data.
        """
        
        decoded = {}
        for item in self.data['Monitoring']['protocol']:
            key = item['value']
            value = 0
            for v in data[item['startByte']:item['startByte'] + item['length']]:
                value = (value << 8) + v
            decoded[key] = str(value)
        return decoded
    
    def decode_monitor_json(self, data):
        """Decode a bytestring that encodes JSON status data."""
        
        return json.loads(data.decode('utf8'))
    
    def decode_monitor(self, data):
        """Decode  status data."""
        
        if self.binary_monitor_data:
            return self.decode_monitor_binary(data)
        else:
            return self.decode_monitor_json(data)

class Device(object):
    """A higher-level interface to a specific device.
        
    Unlike `DeviceInfo`, which just stores data *about* a device,
    `Device` objects refer to their client and can perform operations
    regarding the device.
    """

    def __init__(self, client, device):
        """Create a wrapper for a `DeviceInfo` object associated with a
        `Client`.
        """
        
        self.client = client
        self.device = device
        self.model = client.model_info(device)

    def _set_control(self, key, value):
        """Set a device's control for `key` to `value`.
        """
        
        self.client.session.set_device_controls(
            self.device.id,
            {key: value},
            )
    
    def _get_config(self, key):
        """Look up a device's configuration for a given value.
            
        The response is parsed as base64-encoded JSON.
        """
        
        data = self.client.session.get_device_config(
               self.device.id,
               key,
        )
        return json.loads(base64.b64decode(data).decode('utf8'))
    
    def _get_control(self, key):
        """Look up a device's control value.
            """
        
        data = self.client.session.get_device_config(
               self.device.id,
                key,
               'Control',
        )

            # The response comes in a funky key/value format: "(key:value)".
        _, value = data[1:-1].split(':')
        return value


    def _delete_permission(self):
        self.client.session.delete_permission(
            self.device.id,
        )

"""------------------for Air Conditioner"""
class ACMode(enum.Enum):
    """The operation mode for an AC/HVAC device."""
    
    COOL = "@AC_MAIN_OPERATION_MODE_COOL_W"
    DRY = "@AC_MAIN_OPERATION_MODE_DRY_W"
    FAN_ONLY = "@AC_MAIN_OPERATION_MODE_FAN_W"
    AI = "@AC_MAIN_OPERATION_MODE_AI_W"
    HEAT = "@AC_MAIN_OPERATION_MODE_HEAT_W"
    AIRCLEAN = "@AC_MAIN_OPERATION_MODE_AIRCLEAN_W"
    ACO = "@AC_MAIN_OPERATION_MODE_ACO_W"
    AROMA = "@AC_MAIN_OPERATION_MODE_AROMA_W"
    ENERGY_SAVING = "@AC_MAIN_OPERATION_MODE_ENERGY_SAVING_W"
    SMARTCARE = "@AC_MAIN_WIND_MODE_SMARTCARE_W"

class ACWindstrength(enum.Enum):
    """The wind strength mode for an AC/HVAC device."""
    
    LOW = "@AC_MAIN_WIND_STRENGTH_LOW_MID_W"
    MID = "@AC_MAIN_WIND_STRENGTH_MID_W"
    HIGH = "@AC_MAIN_WIND_STRENGTH_HIGH_LEFT_W|AC_MAIN_WIND_STRENGTH_HIGH_RIGHT_W"
    RIGHT_LOW_LEFT_MID = "@AC_MAIN_WIND_STRENGTH_MID_LEFT_W|AC_MAIN_WIND_STRENGTH_LOW_RIGHT_W"
    RIGHT_LOW_LEFT_HIGH = "@AC_MAIN_WIND_STRENGTH_HIGH_LEFT_W|AC_MAIN_WIND_STRENGTH_LOW_RIGHT_W"
    RIGHT_MID_LEFT_LOW = "@AC_MAIN_WIND_STRENGTH_LOW_LEFT_W|AC_MAIN_WIND_STRENGTH_MID_RIGHT_W"
    RIGHT_MID_LEFT_HIGH = "@AC_MAIN_WIND_STRENGTH_HIGH_LEFT_W|AC_MAIN_WIND_STRENGTH_MID_RIGHT_W"
    RIGHT_HIGH_LEFT_LOW = "@AC_MAIN_WIND_STRENGTH_LOW_LEFT_W|AC_MAIN_WIND_STRENGTH_HIGH_RIGHT_W"
    RIGHT_HIGH_LEFT_MID = "@AC_MAIN_WIND_STRENGTH_MID_LEFT_W|AC_MAIN_WIND_STRENGTH_HIGH_RIGHT_W"
    RIGHT_ONLY_LOW = "@AC_MAIN_WIND_STRENGTH_LOW_RIGHT_W"
    RIGHT_ONLY_MID = "@AC_MAIN_WIND_STRENGTH_MID_RIGHT_W"
    RIGHT_ONLY_HIGH = "@AC_MAIN_WIND_STRENGTH_HIGH_RIGHT_W"
    LEFT_ONLY_LOW = "@AC_MAIN_WIND_STRENGTH_LOW_LEFT_W"
    LEFT_ONLY_MID = "@AC_MAIN_WIND_STRENGTH_MID_LEFT_W"
    LEFT_ONLY_HIGH = "@AC_MAIN_WIND_STRENGTH_HIGH_LEFT_W"

class ACOp(enum.Enum):
    """Whether a device is on or off."""
    
    OFF = "@AC_MAIN_OPERATION_OFF_W"
    RIGHT_ON = "@AC_MAIN_OPERATION_RIGHT_ON_W"
    LEFT_ON = "@AC_MAIN_OPERATION_LEFT_ON_W"
    ALL_ON = "@AC_MAIN_OPERATION_ALL_ON_W"

class ICEVALLEY(enum.Enum):
    OFF = "@OFF"
    ON = "@ON"

class LONGPOWER(enum.Enum):
    OFF = "@OFF"
    ON = "@ON"

class SMARTCARE(enum.Enum):
    OFF = "@OFF"
    ON = "@ON"

class AIRCLEAN(enum.Enum):
    OFF = "@AC_MAIN_AIRCLEAN_OFF_W"
    ON = "@AC_MAIN_AIRCLEAN_ON_W"

class POWERSAVE(enum.Enum):
    OFF = "@OFF"
    ON = "@ON"

class AUTODRY(enum.Enum):
    OFF = "@OFF"
    ON = "@ON"

class POWERSAVEDRY(enum.Enum):
    OFF = "@OFF"
    ON = "@ON"

class WDIRUPDOWN(enum.Enum):
    OFF = "@OFF"
    ON = "@ON"

class WDIRLEFTRIGHT(enum.Enum):
    LEFT_RIGHT_STOP = "@OFF"
    RIGHTSIDE_LEFT_RIGHT = "@RIGHT_ON"
    LEFTSIDE_LEFT_RIGHT = "@LEFT_ON"
    LEFT_RIGHT = "@ALL_ON"

class ACDevice(Device):
    """Higher-level operations on an AC/HVAC device, such as a heat
    pump.
    """
    
    @property
    def f2c(self):
        """Get a dictionary mapping Fahrenheit to Celsius temperatures for
        this device.
        
        Unbelievably, SmartThinQ devices have their own lookup tables
        for mapping the two temperature scales. You can get *close* by
        using a real conversion between the two temperature scales, but
        precise control requires using the custom LUT.
        """
        
        mapping = self.model.value('TempFahToCel').options
        return {int(f): c for f, c in mapping.items()}
    
    @property
    def c2f(self):
        """Get an inverse mapping from Celsius to Fahrenheit.
            
        Just as unbelievably, this is not exactly the inverse of the
        `f2c` map. There are a few values in this reverse mapping that
        are not in the other.
        """
        
        mapping = self.model.value('TempCelToFah').options
        out = {}
        for c, f in mapping.items():
            try:
                c_num = int(c)
            except ValueError:
                c_num = float(c)
            out[c_num] = f
        return out
    
    def set_celsius(self, c):
        """Set the device's target temperature in Celsius degrees.
        """
        
        self._set_control('TempCfg', c)
    
    def set_fahrenheit(self, f):
        """Set the device's target temperature in Fahrenheit degrees.
        """
        
        self.set_celsius(self.f2c[f])
    
    def set_mode(self, mode):
        """Set the device's operating mode to an `OpMode` value.
        """
        
        mode_value = self.model.enum_value('OpMode', mode.value)
        self._set_control('OpMode', mode_value)
    
    
    def set_windstrength(self, mode):
        """Set the device's operating mode to an `windstrength` value.
        """
        
        windstrength_value = self.model.enum_value('WindStrength', mode.value)
        self._set_control('WindStrength', windstrength_value)
    
    
    def set_on(self, is_on):
        """Turn on or off the device (according to a boolean).
        """
        
        op = ACOp.ALL_ON if is_on else ACOp.OFF
        op_value = self.model.enum_value('Operation', op.value)
        self._set_control('Operation', op_value)
    
    def set_icevalley(self, is_on):
        
        mode = ICEVALLEY.ON if is_on else ICEVALLEY.OFF
        mode_value = self.model.enum_value('IceValley', mode.value)
        self._set_control('IceValley', mode_value)
    
    def set_longpower(self, is_on):
        
        mode = LONGPOWER.ON if is_on else LONGPOWER.OFF
        mode_value = self.model.enum_value('FlowLongPower', mode.value)
        self._set_control('FlowLongPower', mode_value)
    
    def set_smartcare(self, is_on):
        
        mode = SMARTCARE.ON if is_on else SMARTCARE.OFF
        mode_value = self.model.enum_value('SmartCare', mode.value)
        self._set_control('SmartCare', mode_value)
    
    def set_airclean(self, is_on):
        
        mode = AIRCLEAN.ON if is_on else AIRCLEAN.OFF
        mode_value = self.model.enum_value('AirClean', mode.value)
        self._set_control('AirClean', mode_value)
    
    def set_powersave(self, is_on):
        
        mode = POWERSAVE.ON if is_on else POWERSAVE.OFF
        mode_value = self.model.enum_value('PowerSave', mode.value)
        self._set_control('PowerSave', mode_value)
    
    def set_autodry(self, is_on):
        
        mode = AUTODRY.ON if is_on else AUTODRY.OFF
        mode_value = self.model.enum_value('AutoDry', mode.value)
        self._set_control('AutoDry', mode_value)
    
    def set_wind_updown(self, is_on):
        
        wdir = WDIRUPDOWN.ON if is_on else WDIRUPDOWN.OFF
        wdir_value = self.model.enum_value('WDirUpDown', wdir.value)
        self._set_control('WDirUpDown', wdir_value)
    
    def set_wind_leftright(self, mode):
        
        wdir_value = self.model.enum_value('WDirLeftRight', mode.value)
        self._set_control('WDirLeftRight', wdir_value)
    
    def get_filter_state(self):
        """Get information about the filter."""
        
        return self._get_config('Filter')
    
    def get_mfilter_state(self):
        """Get information about the "MFilter" (not sure what this is).
        """
        return self._get_config('MFilter')
    
    def get_energy_target(self):
        """Get the configured energy target data."""
        
        return self._get_config('EnergyDesiredValue')
    
    def get_light(self):
        """Get a Boolean indicating whether the display light is on."""
        
        value = self._get_control('DisplayControl')
        return value == '0'  # Seems backwards, but isn't.
    
    def get_volume(self):
        """Get the speaker volume level."""
        
        value = self._get_control('SpkVolume')
        return int(value)
    
    def monitor_start(self):
        """Start monitoring the device's status."""
        
        self.mon = Monitor(self.client.session, self.device.id)
        self.mon.start()
    
    def monitor_stop(self):
        """Stop monitoring the device's status."""
        
        self.mon.stop()
    
    def delete_permission(self):
        self._delete_permission()
    
    def poll(self):
        """Poll the device's current state.
            
        Monitoring must be started first with `monitor_start`. Return
        either an `ACStatus` object or `None` if the status is not yet
        available.
        """
        data = self.mon.poll()
        if data:
            res = self.model.decode_monitor(data)
            """
            with open('/config/wideq/hvac_polled_data.json','w', encoding="utf-8") as dumpfile:
                json.dump(res, dumpfile, ensure_ascii=False, indent="\t")
            """
            return ACStatus(self, res)
        else:
            return None     

class ACStatus(object):
    """Higher-level information about an AC device's current status.
    """
    
    def __init__(self, ac, data):
        self.ac = ac
        self.data = data
    
    @staticmethod
    def _str_to_num(s):
        """Convert a string to either an `int` or a `float`.
        
        Troublingly, the API likes values like "18", without a trailing
        ".0",LEF for whole numbers. So we use `int`s for integers and
        `float`s for non-whole numbers.
        """
        
        f = float(s)
        if f == int(f):
            return int(f)
        else:
            return f

    @property
    def temp_cur_c(self):
        return self._str_to_num(self.data['TempCur'])
    
    @property
    def temp_cur_f(self):
        return self.ac.c2f[self.temp_cur_c]
    
    @property
    def temp_cfg_c(self):
        return self._str_to_num(self.data['TempCfg'])
    
    @property
    def temp_cfg_f(self):
        return self.ac.c2f[self.temp_cfg_c]
    
    def lookup_enum(self, key):
        return self.ac.model.enum_name(key, self.data[key])
    
    @property
    def mode(self):
        return ACMode(self.lookup_enum('OpMode'))
    
    @property
    def windstrength_state(self):
        return ACWindstrength(self.lookup_enum('WindStrength'))
    
    @property
    def wdirupdown_state(self):
        return WDIRUPDOWN(self.lookup_enum('WDirUpDown'))
    
    @property
    def wdirleftright_state(self):
        return WDIRLEFTRIGHT(self.lookup_enum('WDirLeftRight'))
    
    @property
    def is_on(self):
        op = ACOp(self.lookup_enum('Operation'))
        return op != ACOp.OFF
    
    @property
    def airclean_state(self):
        return AIRCLEAN(self.lookup_enum('AirClean'))
    
    @property
    def icevalley_state(self):
        return ICEVALLEY(self.lookup_enum('IceValley'))
    
    @property
    def longpower_state(self):
        return LONGPOWER(self.lookup_enum('FlowLongPower'))
    
    @property
    def autodry_state(self):
        return AUTODRY(self.lookup_enum('AutoDry'))
    
    @property
    def smartcare_state(self):
        return SMARTCARE(self.lookup_enum('SmartCare'))
    
    @property
    def powersave_state(self):
        return POWERSAVE(self.lookup_enum('PowerSave'))
    
    @property
    def humidity(self):
        return self.data['SensorHumidity']
    
    @property
    def sensorpm1(self):
        return self.data['SensorPM1']
    
    @property
    def sensorpm2(self):
        return self.data['SensorPM2']
    
    @property
    def sensorpm10(self):
        return self.data['SensorPM10']
    
    @property
    def total_air_polution(self):
        return self.data['TotalAirPolution']
    
    @property
    def air_polution(self):
        return self.data['AirPolution']



"""------------------for Refrigerator"""
class ICEPLUS(enum.Enum):

    OFF = "@CP_OFF_EN_W"
    ON = "@CP_ON_EN_W"

class FRESHAIRFILTER(enum.Enum):

    OFF = "@CP_TERM_OFF_KO_W"
    AUTO = "@RE_STATE_FRESH_AIR_FILTER_MODE_AUTO_W"
    POWER = "@RE_STATE_FRESH_AIR_FILTER_MODE_POWER_W"
    REPLACE_FILTER = "@RE_STATE_REPLACE_FILTER_W"
    SMARTCARE_ON = "@RE_STATE_SMART_SMART_CARE_ON"
    SMARTCARE_OFF = "@RE_STATE_SMART_SMART_CARE_OFF"
    SMARTCARE_WAIT = "@RE_STATE_SMART_SMART_CARE_WAIT"

class SMARTSAVING(enum.Enum):

    OFF = "@CP_TERM_USE_NOT_W"
    NIGHT = "@RE_SMARTSAVING_MODE_NIGHT_W"
    CUSTOM = "@RE_SMARTSAVING_MODE_CUSTOM_W"

class RefDevice(Device):
    
    def set_reftemp(self, temp):
        """Set the refrigerator temperature.
        """
        temp_value = self.model.enum_value('TempRefrigerator_C', temp)
        self._set_control('RETM', temp_value)
    
    def set_freezertemp(self, temp):
        """Set the freezer temperature.
        """
        temp_value = self.model.enum_value('TempFreezer_C', temp)
        self._set_control('REFT', temp_value)
    
    def set_iceplus(self, mode):
        """Set the device's operating mode to an `iceplus` value.
        """
        
        iceplus_value = self.model.enum_value('IcePlus', mode.value)
        self._set_control('REIP', iceplus_value)
    
    def set_freshairfilter(self, mode):
        """Set the device's operating mode to an `freshairfilter` value.
        """
        
        freshairfilter_value = self.model.enum_value('FreshAirFilter', mode.value)
        self._set_control('REHF', freshairfilter_value)
    
    def set_activesaving(self, value):
        self._set_control('REAS', value)

    def monitor_start(self):
        """Start monitoring the device's status."""
        
        self.mon = Monitor(self.client.session, self.device.id)
        self.mon.start()
    
    def monitor_stop(self):
        """Stop monitoring the device's status."""
        
        self.mon.stop()
    
    def delete_permission(self):
        self._delete_permission()
    
    def poll(self):
        """Poll the device's current state.
            
        Monitoring must be started first with `monitor_start`. Return
        either an `ACStatus` object or `None` if the status is not yet
        available.
        """
        
        data = self.mon.poll()
        if data:
            res = self.model.decode_monitor(data)
            """
            with open('/config/wideq/ref_polled_data.json','w', encoding="utf-8") as dumpfile:
                json.dump(res, dumpfile, ensure_ascii=False, indent="\t")
            """
            return RefStatus(self, res)
        
        else:
            return None


class RefStatus(object):
    
    """Higher-level information about an Ref device's current status.
    """
    
    def __init__(self, ref, data):
        self.ref = ref
        self.data = data
    
    def lookup_enum(self, key):
        return self.ref.model.enum_name(key, self.data[key])
    
    def lookup_enum_temp(self, key, value):
        return self.ref.model.enum_name(key, value)
        
    @property
    def current_reftemp(self):
        temp = self.lookup_enum('TempRefrigerator')
        return self.lookup_enum_temp('TempRefrigerator_C', temp)

    @property
    def current_midtemp(self):
        temp = self.lookup_enum('TempMiddle')
        return self.lookup_enum_temp('TempMiddle_C', temp)

    @property
    def current_freezertemp(self):
        temp = self.lookup_enum('TempFreezer')
        return self.lookup_enum_temp('TempFreezer_C', temp)
    
    @property
    def iceplus_state(self):
        return ICEPLUS(self.lookup_enum('IcePlus'))
    
    @property
    def freshairfilter_state(self):
        return FRESHAIRFILTER(self.lookup_enum('FreshAirFilter'))
    
    @property
    def smartsaving_mode(self):
        return self.lookup_enum('SmartSavingMode')
    
    @property
    def waterfilter_state(self):
        try:
            waterfilter = self.lookup_enum('WaterFilterUsedMonth')
        except AttributeError:
            return self.data['WaterFilterUsedMonth']
        if waterfilter:
            return waterfilter
    
    @property
    def door_state(self):
        return self.lookup_enum('DoorOpenState')
    
    @property
    def smartsaving_state(self):
        return self.lookup_enum('SmartSavingModeStatus')
    
    @property
    def locking_state(self):
        return self.lookup_enum('LockingStatus')
    
    @property
    def activesaving_state(self):
        return self.data['ActiveSavingStatus']



"""------------------for Dryer"""
class DRYERSTATE(enum.Enum):
    
    OFF = "@WM_STATE_POWER_OFF_W"
    INITIAL = "@WM_STATE_INITIAL_W"
    RUNNING = "@WM_STATE_RUNNING_W"
    PAUSE = "@WM_STATE_PAUSE_W"
    END = "@WM_STATE_END_W"
    ERROR = "@WM_STATE_ERROR_W"

class DRYERPROCESSSTATE(enum.Enum):
    
    DETECTING = "@WM_STATE_DETECTING_W"
    STEAM = "@WM_STATE_STEAM_W"
    DRY = "@WM_STATE_DRY_W"
    COOLING = "@WM_STATE_COOLING_W"
    ANTI_CREASE = "@WM_STATE_ANTI_CREASE_W"
    END = "@WM_STATE_END_W"

class DRYLEVEL(enum.Enum):
    
    IRON = "@WM_DRY24_DRY_LEVEL_IRON_W"
    CUPBOARD = "@WM_DRY24_DRY_LEVEL_CUPBOARD_W"
    EXTRA = "@WM_DRY24_DRY_LEVEL_EXTRA_W"

class ECOHYBRID(enum.Enum):
    
    ECO = "@WM_DRY24_ECO_HYBRID_ECO_W"
    NORMAL = "@WM_DRY24_ECO_HYBRID_NORMAL_W"
    TURBO = "@WM_DRY24_ECO_HYBRID_TURBO_W"

class DRYERERROR(enum.Enum):
    
    ERROR_DOOR = "@WM_US_DRYER_ERROR_DE_W"
    ERROR_DRAINMOTOR = "@WM_US_DRYER_ERROR_OE_W"
    ERROR_LE1 = "@WM_US_DRYER_ERROR_LE1_W"
    ERROR_TE1 = "@WM_US_DRYER_ERROR_TE1_W"
    ERROR_TE2 = "@WM_US_DRYER_ERROR_TE2_W"
    ERROR_F1 = "@WM_US_DRYER_ERROR_F1_W"
    ERROR_LE2 = "@WM_US_DRYER_ERROR_LE2_W"
    ERROR_AE = "@WM_US_DRYER_ERROR_AE_W"
    ERROR_dE4 = "@WM_WW_FL_ERROR_DE4_W"
    ERROR_NOFILTER = "@WM_US_DRYER_ERROR_NOFILTER_W"
    ERROR_EMPTYWATER = "@WM_US_DRYER_ERROR_EMPTYWATER_W"
    ERROR_CE1 = "@WM_US_DRYER_ERROR_CE1_W"

class DryerDevice(Device):
    
    def monitor_start(self):
        """Start monitoring the device's status."""
        
        self.mon = Monitor(self.client.session, self.device.id)
        self.mon.start()
    
    def monitor_stop(self):
        """Stop monitoring the device's status."""
        
        self.mon.stop()
    
    def delete_permission(self):
        self._delete_permission()
    
    def poll(self):
        """Poll the device's current state.
        
        Monitoring must be started first with `monitor_start`. Return
        either an `ACStatus` object or `None` if the status is not yet
        available.
        """
        
        data = self.mon.poll()
        if data:
            res = self.model.decode_monitor(data)
            """
            with open('/config/wideq/dryer_polled_data.json','w', encoding="utf-8") as dumpfile:
                json.dump(res, dumpfile, ensure_ascii=False, indent="\t")
            """
            return DryerStatus(self, res)
        
        else:
            return None


class DryerStatus(object):
    
    """Higher-level information about an Ref device's current status.
    """
    
    def __init__(self, dryer, data):
        self.dryer = dryer
        self.data = data
    
    def lookup_enum(self, key):
        return self.dryer.model.enum_name(key, self.data[key])
    
    def lookup_reference(self, key):
        return self.dryer.model.reference_name(key, self.data[key])
    
    def lookup_bit(self, key, index):
        bit_value = int(self.data[key])
        bit_index = 2 ** index
        mode = bin(bit_value & bit_index)
        if mode == bin(0):
            return 'OFF'
        else:
            return 'ON'


    @property
    def is_on(self):
        run_state = DRYERSTATE(self.lookup_enum('State'))
        return run_state != DRYERSTATE.OFF
    
    @property
    def run_state(self):
        return DRYERSTATE(self.lookup_enum('State'))
    
    @property
    def remaintime_hour(self):
        return self.data['Remain_Time_H']
    
    @property
    def remaintime_min(self):
        return self.data['Remain_Time_M']
    
    @property
    def initialtime_hour(self):
        return self.data['Initial_Time_H']
    
    @property
    def initialtime_min(self):
        return self.data['Initial_Time_M']

    @property
    def reservetime_hour(self):
        return self.data['Reserve_Time_H']
    
    @property
    def reservetime_min(self):
        return self.data['Reserve_Time_M']

    @property
    def reserveinitialtime_hour(self):
        return self.data['Reserve_Initial_Time_H']

    @property
    def reserveinitialtime_min(self):
        return self.data['Reserve_Initial_Time_M']
    
    @property
    def current_course(self):
        course = self.lookup_reference('Course')
        if course == '-':
            return 'OFF'
        else:
            return course

    @property
    def error_state(self):
        error = self.lookup_reference('Error')
        if error == '-':
            return 'OFF'
        elif error == 'No Error':
            return 'NO_ERROR'
        else:
            return DRYERERROR(error)

    @property
    def drylevel_state(self):
        drylevel = self.lookup_enum('DryLevel')
        if drylevel == '-':
            return 'OFF'
        return DRYLEVEL(drylevel)
    
    @property
    def ecohybrid_state(self):
        ecohybrid = self.lookup_enum('EcoHybrid')
        if ecohybrid == '-':
            return 'OFF'
        return ECOHYBRID(ecohybrid)
    
    @property
    def process_state(self):
        return DRYERPROCESSSTATE(self.lookup_enum('ProcessState'))
    
    @property
    def current_smartcourse(self):
        smartcourse = self.lookup_reference('SmartCourse')
        if smartcourse == '-':
            return 'OFF'
        else:
            return smartcourse

    @property
    def anticrease_state(self):
        return self.lookup_bit('Option1', 1)

    @property
    def childlock_state(self):
        return self.lookup_bit('Option1', 4)

    @property
    def selfcleaning_state(self):
        return self.lookup_bit('Option1', 5)

    @property
    def dampdrybeep_state(self):
        return self.lookup_bit('Option1', 6)

    @property
    def handiron_state(self):
        return self.lookup_bit('Option1', 7)



"""------------------for Washer"""

class WASHERSTATE(enum.Enum):
    
    OFF = "@WM_STATE_POWER_OFF_W"
    INITIAL = "@WM_STATE_INITIAL_W"
    PAUSE = "@WM_STATE_PAUSE_W"
    ERROR_AUTO_OFF = "@WM_STATE_ERROR_AUTO_OFF_W"
    RESERVE = "@WM_STATE_RESERVE_W"
    DETECTING = "@WM_STATE_DETECTING_W"
    ADD_DRAIN = "WM_STATE_ADD_DRAIN_W"
    DETERGENT_AMOUNT = "@WM_STATE_DETERGENT_AMOUNT_W"
    RUNNING = "@WM_STATE_RUNNING_W"
    PREWASH = "@WM_STATE_PREWASH_W"
    RINSING = "@WM_STATE_RINSING_W"
    RINSE_HOLD = "@WM_STATE_RINSE_HOLD_W"
    SPINNING = "@WM_STATE_SPINNING_W"
    DRYING = "@WM_STATE_DRYING_W"
    END = "@WM_STATE_END_W"
    FRESHCARE = "@WM_STATE_FRESHCARE_W"
    TCL_ALARM_NORMAL = "TCL_ALARM_NORMAL"
    FROZEN_PREVENT_INITIAL = "@WM_STATE_FROZEN_PREVENT_INITIAL_W"
    FROZEN_PREVENT_RUNNING = "@WM_STATE_FROZEN_PREVENT_RUNNING_W"
    FROZEN_PREVENT_PAUSE = "@WM_STATE_FROZEN_PREVENT_PAUSE_W"


class WASHERSOILLEVEL(enum.Enum):
    
    NO_SELECT = "@WM_TERM_NO_SELECT_W"
    LIGHT = "@WM_KR_TT27_WD_WIFI_OPTION_SOILLEVEL_LIGHT_W"
    NORMAL = "@WM_KR_TT27_WD_WIFI_OPTION_SOILLEVEL_NORMAL_W"
    HEAVY = "@WM_KR_TT27_WD_WIFI_OPTION_SOILLEVEL_HEAVY_W"
    PRE_WASH = "@WM_KR_TT27_WD_WIFI_OPTION_SOILLEVEL_PRE_WASH_W"
    SOAKING = "@WM_KR_TT27_WD_WIFI_OPTION_SOILLEVEL_SOAKING_W"
    
class WASHERWATERTEMP(enum.Enum):
    
    NO_SELECT = "@WM_TERM_NO_SELECT_W"
    COLD = "@WM_KR_TT27_WD_WIFI_OPTION_WATERTEMP_COLD_W"
    THIRTY = "@WM_KR_TT27_WD_WIFI_OPTION_WATERTEMP_30_W"
    FOURTY = "@WM_KR_TT27_WD_WIFI_OPTION_WATERTEMP_40_W"
    SIXTY = "@WM_KR_TT27_WD_WIFI_OPTION_WATERTEMP_60_W"
    NINTYFIVE = "@WM_KR_TT27_WD_WIFI_OPTION_WATERTEMP_95_W"

class WASHERSPINSPEED(enum.Enum):
    
    NO_SELECT = "@WM_TERM_NO_SELECT_W"
    EXTRA_LOW = "@WM_KR_TT27_WD_WIFI_OPTION_SPINSPEED_EXTRA_LOW_W"
    LOW = "@WM_KR_TT27_WD_WIFI_OPTION_SPINSPEED_LOW_W"
    MEDIUM = "@WM_KR_TT27_WD_WIFI_OPTION_SPINSPEED_MEDIUM_W"
    HIGH = "@WM_KR_TT27_WD_WIFI_OPTION_SPINSPEED_HIGH_W"
    EXTRA_HIGH = "@WM_KR_TT27_WD_WIFI_OPTION_SPINSPEED_EXTRA_HIGH_W"

class WASHERRINSECOUNT(enum.Enum):
    
    NO_SELECT = "@WM_TERM_NO_SELECT_W"
    ONE = "@WM_KR_TT27_WD_WIFI_OPTION_RINSECOUNT_1_W"
    TWO = "@WM_KR_TT27_WD_WIFI_OPTION_RINSECOUNT_2_W"
    THREE = "@WM_KR_TT27_WD_WIFI_OPTION_RINSECOUNT_3_W"
    FOUR = "@WM_KR_TT27_WD_WIFI_OPTION_RINSECOUNT_4_W"
    FIVE = "@WM_KR_TT27_WD_WIFI_OPTION_RINSECOUNT_5_W"

class WASHERDRYLEVEL(enum.Enum):
    
    NO_SELECT = "@WM_TERM_NO_SELECT_W"
    WIND = "@WM_KR_TT27_WD_WIFI_OPTION_DRYLEVEL_WIND_W"
    TURBO = "@WM_KR_TT27_WD_WIFI_OPTION_DRYLEVEL_TURBO_W"
    TIME_30 = "@WM_KR_TT27_WD_WIFI_OPTION_DRYLEVEL_TIME_30_W"
    TIME_60 = "@WM_KR_TT27_WD_WIFI_OPTION_DRYLEVEL_TIME_60_W"
    TIME_90 = "@WM_KR_TT27_WD_WIFI_OPTION_DRYLEVEL_TIME_90_W"
    TIME_120 = "@WM_KR_TT27_WD_WIFI_OPTION_DRYLEVEL_TIME_120_W"
    TIME_150 = "@WM_KR_TT27_WD_WIFI_OPTION_DRYLEVEL_TIME_150_W"

class WASHERERROR(enum.Enum):
    
    ERROR_dE2 = "@WM_KR_TT27_WD_WIFI_ERROR_DE2"
    ERROR_IE = "@WM_KR_TT27_WD_WIFI_ERROR_IE"
    ERROR_OE = "@WM_KR_TT27_WD_WIFI_ERROR_OE"
    ERROR_UE = "@WM_KR_TT27_WD_WIFI_ERROR_UE"
    ERROR_FE = "@WM_KR_TT27_WD_WIFI_ERROR_FE"
    ERROR_PE = "@WM_KR_TT27_WD_WIFI_ERROR_PE"
    ERROR_tE = "@WM_KR_TT27_WD_WIFI_ERROR_TE"
    ERROR_LE = "@WM_KR_TT27_WD_WIFI_ERROR_LE"
    ERROR_CE = "@WM_KR_TT27_WD_WIFI_ERROR_CE"
    ERROR_dHE = "@WM_KR_TT27_WD_WIFI_ERROR_DHE"
    ERROR_PF = "@WM_KR_TT27_WD_WIFI_ERROR_PF"
    ERROR_FF = "@WM_KR_TT27_WD_WIFI_ERROR_FF"
    ERROR_dCE = "@WM_KR_TT27_WD_WIFI_ERROR_DCE"
    ERROR_EE = "@WM_KR_TT27_WD_WIFI_ERROR_EE"
    ERROR_PS = "@WM_KR_TT27_WD_WIFI_ERROR_PS"
    ERROR_dE1 = "@WM_KR_TT27_WD_WIFI_ERROR_DE1"
    ERROR_LOE = "@WM_KR_TT27_WD_WIFI_ERROR_LOE"


class WasherDevice(Device):
    
    def monitor_start(self):
        """Start monitoring the device's status."""
        
        self.mon = Monitor(self.client.session, self.device.id)
        self.mon.start()
    
    def monitor_stop(self):
        """Stop monitoring the device's status."""
        
        self.mon.stop()
    
    def delete_permission(self):
        self._delete_permission()
    
    def poll(self):
        """Poll the device's current state.
        
        Monitoring must be started first with `monitor_start`. Return
        either an `ACStatus` object or `None` if the status is not yet
        available.
        """
        
        data = self.mon.poll()
        if data:
            res = self.model.decode_monitor(data)
            """
            with open('/config/wideq/washer_polled_data.json','w', encoding="utf-8") as dumpfile:
                json.dump(res, dumpfile, ensure_ascii=False, indent="\t")
            """
            return WasherStatus(self, res)
        
        else:
            return None

class WasherStatus(object):
    
    def __init__(self, washer, data):
        self.washer = washer
        self.data = data
    
    def lookup_enum(self, key):
        return self.washer.model.enum_name(key, self.data[key])
    
    def lookup_reference(self, key):
        return self.washer.model.reference_name(key, self.data[key])
    
    def lookup_bit(self, key, index):
        bit_value = int(self.data[key])
        bit_index = 2 ** index
        mode = bin(bit_value & bit_index)
        if mode == bin(0):
            return 'OFF'
        else:
            return 'ON'

    @property
    def is_on(self):
        run_state = WASHERSTATE(self.lookup_enum('State'))
        return run_state != WASHERSTATE.OFF
        
    @property
    def run_state(self):
        return WASHERSTATE(self.lookup_enum('State'))

    @property
    def pre_state(self):
        return WASHERSTATE(self.lookup_enum('PreState'))
    
    @property
    def remaintime_hour(self):
        return self.data['Remain_Time_H']
    
    @property
    def remaintime_min(self):
        return self.data['Remain_Time_M']
    
    @property
    def initialtime_hour(self):
        return self.data['Initial_Time_H']
    
    @property
    def initialtime_min(self):
        return self.data['Initial_Time_M']

    @property
    def reservetime_hour(self):
        return self.data['Reserve_Time_H']
    
    @property
    def reservetime_min(self):
        return self.data['Reserve_Time_M']

    @property
    def current_course(self):
        course = self.lookup_reference('APCourse')
        if course == '-':
            return 'OFF'
        else:
            return course

    @property
    def error_state(self):
        error = self.lookup_reference('Error')
        if error == '-':
            return 'OFF'
        elif error == 'No Error':
            return 'NO_ERROR'
        else:
            return WASHERERROR(error)

    @property
    def wash_option_state(self):
        soillevel = self.lookup_enum('SoilLevel')
        if soillevel == '-':
            return 'OFF'
        return WASHERSOILLEVEL(soillevel)
    
    @property
    def spin_option_state(self):
        spinspeed = self.lookup_enum('SpinSpeed')
        if spinspeed == '-':
            return 'OFF'
        return WASHERSPINSPEED(spinspeed)

    @property
    def water_temp_option_state(self):
        water_temp = self.lookup_enum('WaterTemp')
        if water_temp == '-':
            return 'OFF'
        return WASHERWATERTEMP(water_temp)

    @property
    def rinsecount_option_state(self):
        rinsecount = self.lookup_enum('RinseCount')
        if rinsecount == '-':
            return 'OFF'
        return WASHERRINSECOUNT(rinsecount)

    @property
    def drylevel_option_state(self):
        drylevel = self.lookup_enum('DryLevel')
        if drylevel == '-':
            return 'OFF'
        return WASHERDRYLEVEL(drylevel)
   
    @property
    def current_smartcourse(self):
        smartcourse = self.lookup_reference('SmartCourse')
        if smartcourse == '-':
            return 'OFF'
        else:
            return smartcourse

    @property
    def freshcare_state(self):
        return self.lookup_bit('Option1', 1)

    @property
    def childlock_state(self):
        return self.lookup_bit('Option1', 3)

    @property
    def steam_state(self):
        return self.lookup_bit('Option1', 4)

    @property
    def turboshot_state(self):
        return self.lookup_bit('Option2', 7)

    @property
    def tubclean_count(self):
        return self.data['TCLCount']

    @property
    def load_level(self):
        return self.lookup_enum('LoadLevel')


"""------------------for Dehumidifier"""
class DEHUMOperation(enum.Enum):
    
    ON = "@operation_on"
    OFF = "@operation_off"

class DEHUMOPMode(enum.Enum):
    
    SMART_DEHUM = "@AP_MAIN_MID_OPMODE_SMART_DEHUM_W"
    FAST_DEHUM = "@AP_MAIN_MID_OPMODE_FAST_DEHUM_W"
    SILENT_DEHUM = "@AP_MAIN_MID_OPMODE_CILENT_DEHUM_W"
    CONCENTRATION_DRY = "@AP_MAIN_MID_OPMODE_CONCENTRATION_DRY_W"
    CLOTHING_DRY = "@AP_MAIN_MID_OPMODE_CLOTHING_DRY_W"
    IONIZER = "@AP_MAIN_MID_OPMODE_IONIZER_W"

class DEHUMWindStrength(enum.Enum):

    LOW = "@AP_MAIN_MID_WINDSTRENGTH_DHUM_LOW_W"
    HIGH = "@AP_MAIN_MID_WINDSTRENGTH_DHUM_HIGH_W"

class DEHUMAIRREMOVAL(enum.Enum):

    OFF = "@AP_OFF_W"
    ON = "@AP_ON_W"

class DIAGCODE(enum.Enum):

    FAN_ERROR = "@ERROR_FAN"
    NORMAL = "@NORMAL"
    EEPROM_ERROR = "@ERROR_EEPROM"

class DehumDevice(Device):


    def set_on(self, is_on):
        mode = DEHUMOperation.ON if is_on else DEHUMOperation.OFF
        mode_value = self.model.enum_value('Operation', mode.value)
        self._set_control('Operation', mode_value)
            
    def set_mode(self, mode):
        
        mode_value = self.model.enum_value('OpMode', mode.value)
        self._set_control('OpMode', mode_value)

    def set_humidity(self, hum):
        """Set the device's target temperature in Celsius degrees.
        """
        self._set_control('HumidityCfg', hum)
    
    def set_windstrength(self, mode):

        windstrength_value = self.model.enum_value('WindStrength', mode.value)
        self._set_control('WindStrength', windstrength_value)
    
    def set_airremoval(self, is_on):
        
        mode = DEHUMAIRREMOVAL.ON if is_on else DEHUMAIRREMOVAL.OFF
        mode_value = self.model.enum_value('AirRemoval', mode.value)
        self._set_control('AirRemoval', mode_value)

    def monitor_start(self):
        """Start monitoring the device's status."""
        
        self.mon = Monitor(self.client.session, self.device.id)
        self.mon.start()
    
    def monitor_stop(self):
        """Stop monitoring the device's status."""
        
        self.mon.stop()
    
    def delete_permission(self):
        self._delete_permission()
    
    def poll(self):
        """Poll the device's current state.
            
        Monitoring must be started first with `monitor_start`. Return
        either an `ACStatus` object or `None` if the status is not yet
        available.
        """
        data = self.mon.poll()
        if data:
            res = self.model.decode_monitor(data)
            """
            with open('/config/wideq/dehumidifier_polled_data.json','w', encoding="utf-8") as dumpfile:
                json.dump(res, dumpfile, ensure_ascii=False, indent="\t")
            """
            return DEHUMStatus(self, res)
        else:
            return None     

class DEHUMStatus(object):
    """Higher-level information about an AC device's current status.
    """
    
    def __init__(self, dehum, data):
        self.dehum = dehum
        self.data = data


    def lookup_enum(self, key):
        return self.dehum.model.enum_name(key, self.data[key])

    @property
    def is_on(self):
        op = DEHUMOperation(self.lookup_enum('Operation'))
        return op == DEHUMOperation.ON

    @property
    def mode(self):
        return DEHUMOPMode(self.lookup_enum('OpMode'))
   
    @property
    def windstrength_state(self):
        return DEHUMWindStrength(self.lookup_enum('WindStrength'))
    
    @property
    def airremoval_state(self):
        return DEHUMAIRREMOVAL(self.lookup_enum('AirRemoval'))
    
    @property
    def current_humidity(self):
        return self.data['SensorHumidity']
    
    @property
    def target_humidity(self):
        return self.data['HumidityCfg']
    
    @property
    def sensorpm1(self):
        return self.data['SensorPM1']
    
    @property
    def sensorpm2(self):
        return self.data['SensorPM2']
    
    @property
    def sensorpm10(self):
        return self.data['SensorPM10']
    
    @property
    def total_air_polution(self):
        return self.data['TotalAirPolution']
    
    @property
    def air_polution(self):
        return self.data['AirPolution']
