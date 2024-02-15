# ProgrammeWithoutCuesheetContentContentDetailItemsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** |  | 
**title** | **str** |  | 
**summary** | **str** |  | [optional] 
**playlist_item_id** | [**ProgrammeWithoutCuesheetContentContentDetailItemsInnerPlaylistItemId**](ProgrammeWithoutCuesheetContentContentDetailItemsInnerPlaylistItemId.md) |  | 
**media2** | [**ProgrammeWithoutCuesheetContentContentDetailItemsInnerMedia2**](ProgrammeWithoutCuesheetContentContentDetailItemsInnerMedia2.md) |  | 
**global_id** | [**ProgrammeWithoutCuesheetContentContentDetailItemsInnerPlaylistItemIdGlobalId2**](ProgrammeWithoutCuesheetContentContentDetailItemsInnerPlaylistItemIdGlobalId2.md) |  | 
**duration** | [**Duration**](Duration.md) |  | 
**broadcasted_first_time_at** | **datetime** |  | 

## Example

```python
from ohdieux.ohdio.generated.models.programme_without_cuesheet_content_content_detail_items_inner import ProgrammeWithoutCuesheetContentContentDetailItemsInner

# TODO update the JSON string below
json = "{}"
# create an instance of ProgrammeWithoutCuesheetContentContentDetailItemsInner from a JSON string
programme_without_cuesheet_content_content_detail_items_inner_instance = ProgrammeWithoutCuesheetContentContentDetailItemsInner.from_json(json)
# print the JSON string representation of the object
print ProgrammeWithoutCuesheetContentContentDetailItemsInner.to_json()

# convert the object into a dict
programme_without_cuesheet_content_content_detail_items_inner_dict = programme_without_cuesheet_content_content_detail_items_inner_instance.to_dict()
# create an instance of ProgrammeWithoutCuesheetContentContentDetailItemsInner from a dict
programme_without_cuesheet_content_content_detail_items_inner_form_dict = programme_without_cuesheet_content_content_detail_items_inner.from_dict(programme_without_cuesheet_content_content_detail_items_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


