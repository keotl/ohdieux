# ProgrammeWithoutCuesheet


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | [**ProgrammeWithoutCuesheetContent**](ProgrammeWithoutCuesheetContent.md) |  | 
**header** | [**ProgrammeWithoutCuesheetHeader**](ProgrammeWithoutCuesheetHeader.md) |  | 
**canonical_url** | **str** |  | 

## Example

```python
from ohdieux.ohdio.generated.models.programme_without_cuesheet import ProgrammeWithoutCuesheet

# TODO update the JSON string below
json = "{}"
# create an instance of ProgrammeWithoutCuesheet from a JSON string
programme_without_cuesheet_instance = ProgrammeWithoutCuesheet.from_json(json)
# print the JSON string representation of the object
print ProgrammeWithoutCuesheet.to_json()

# convert the object into a dict
programme_without_cuesheet_dict = programme_without_cuesheet_instance.to_dict()
# create an instance of ProgrammeWithoutCuesheet from a dict
programme_without_cuesheet_form_dict = programme_without_cuesheet.from_dict(programme_without_cuesheet_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


