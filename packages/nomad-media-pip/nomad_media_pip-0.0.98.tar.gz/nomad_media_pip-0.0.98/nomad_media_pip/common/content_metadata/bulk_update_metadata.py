from nomad_media_pip.exceptions.api_exception_handler import _api_exception_handler
from nomad_media_pip.common.asset.get_asset_details import _get_asset_details
import requests, json

def _bulk_update_metadata(AUTH_TOKEN, URL, CONTENT_IDS, COLLECTION_IDS, RELATED_CONTENT_IDS, 
                          TAG_IDS, SCHEMA_NAME, DEBUG):
    
    API_URL = f"{URL}/api/admin/content/bulk-metadata-update"

    # Create header for the request
    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    ASSET_DETAILS =  _get_asset_details(AUTH_TOKEN, URL, CONTENT_IDS[0], "admin", DEBUG)

    # Create body for the request
    BODY = {
        'collections': (COLLECTION_IDS if COLLECTION_IDS else []) + 
                       ([item['id'] for item in ASSET_DETAILS['collections']] if 'collections' in ASSET_DETAILS and ASSET_DETAILS['collections'] else []),
        'contents': CONTENT_IDS,
        'relatedContents': (RELATED_CONTENT_IDS if RELATED_CONTENT_IDS else []) + 
                           ([item['id'] for item in ASSET_DETAILS['relatedContents']] if 'relatedContents' in ASSET_DETAILS and ASSET_DETAILS['relatedContents'] else []),
        'tags': (TAG_IDS if TAG_IDS else []) + 
                 ([item['id'] for item in ASSET_DETAILS['tags']] if 'tags' in ASSET_DETAILS and ASSET_DETAILS['tags'] else []),
        'schemaName': SCHEMA_NAME
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: POST\nBODY: {json.dumps(BODY, indent= 4)}")

    try:
        # Send the request
        RESPONSE = requests.post(API_URL, headers= HEADERS, data= json.dumps(BODY))

        if not RESPONSE.ok:
            raise Exception()
    
    except:
        _api_exception_handler(RESPONSE, "Bulk update metadata failed")