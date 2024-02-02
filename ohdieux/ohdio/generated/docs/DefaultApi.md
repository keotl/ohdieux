# ohdieux.ohdio.generated.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_media_stream**](DefaultApi.md#get_media_stream) | **GET** /media/validation/v2 | 
[**get_playlist_item**](DefaultApi.md#get_playlist_item) | **GET** /neuro/sphere/v1/medias/apps/playback-lists/{playlistItemId} | 
[**get_programme_without_cuesheet**](DefaultApi.md#get_programme_without_cuesheet) | **GET** /neuro/sphere/v1/audio/apps/products/programmes-without-cuesheet-v2/{programmeId}/{pageNumber} | 


# **get_media_stream**
> MediaStreamDescriptor get_media_stream(app_code, connection_type, device_type, id_media, multibitrate, output, tech)



### Example


```python
import time
import os
import ohdieux.ohdio.generated
from ohdieux.ohdio.generated.models.media_stream_descriptor import MediaStreamDescriptor
from ohdieux.ohdio.generated.models.streaming_tech import StreamingTech
from ohdieux.ohdio.generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = ohdieux.ohdio.generated.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
async with ohdieux.ohdio.generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ohdieux.ohdio.generated.DefaultApi(api_client)
    app_code = 'app_code_example' # str | 
    connection_type = 'connection_type_example' # str | 
    device_type = 'device_type_example' # str | 
    id_media = 'id_media_example' # str | 
    multibitrate = 'multibitrate_example' # str | 
    output = 'output_example' # str | 
    tech = ohdieux.ohdio.generated.StreamingTech() # StreamingTech | 

    try:
        api_response = await api_instance.get_media_stream(app_code, connection_type, device_type, id_media, multibitrate, output, tech)
        print("The response of DefaultApi->get_media_stream:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_media_stream: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_code** | **str**|  | 
 **connection_type** | **str**|  | 
 **device_type** | **str**|  | 
 **id_media** | **str**|  | 
 **multibitrate** | **str**|  | 
 **output** | **str**|  | 
 **tech** | [**StreamingTech**](.md)|  | 

### Return type

[**MediaStreamDescriptor**](MediaStreamDescriptor.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Ok |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_playlist_item**
> PlaylistItem get_playlist_item(playlist_item_id, context, global_id)



### Example


```python
import time
import os
import ohdieux.ohdio.generated
from ohdieux.ohdio.generated.models.playlist_item import PlaylistItem
from ohdieux.ohdio.generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = ohdieux.ohdio.generated.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
async with ohdieux.ohdio.generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ohdieux.ohdio.generated.DefaultApi(api_client)
    playlist_item_id = 'playlist_item_id_example' # str | 
    context = 'context_example' # str | 
    global_id = 'global_id_example' # str | 

    try:
        api_response = await api_instance.get_playlist_item(playlist_item_id, context, global_id)
        print("The response of DefaultApi->get_playlist_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_playlist_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **playlist_item_id** | **str**|  | 
 **context** | **str**|  | 
 **global_id** | **str**|  | 

### Return type

[**PlaylistItem**](PlaylistItem.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Ok |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_programme_without_cuesheet**
> ProgrammeWithoutCuesheet get_programme_without_cuesheet(programme_id, page_number)



### Example


```python
import time
import os
import ohdieux.ohdio.generated
from ohdieux.ohdio.generated.models.programme_without_cuesheet import ProgrammeWithoutCuesheet
from ohdieux.ohdio.generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = ohdieux.ohdio.generated.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
async with ohdieux.ohdio.generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ohdieux.ohdio.generated.DefaultApi(api_client)
    programme_id = 'programme_id_example' # str | 
    page_number = 3.4 # float | 

    try:
        api_response = await api_instance.get_programme_without_cuesheet(programme_id, page_number)
        print("The response of DefaultApi->get_programme_without_cuesheet:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_programme_without_cuesheet: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **programme_id** | **str**|  | 
 **page_number** | **float**|  | 

### Return type

[**ProgrammeWithoutCuesheet**](ProgrammeWithoutCuesheet.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Ok |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

