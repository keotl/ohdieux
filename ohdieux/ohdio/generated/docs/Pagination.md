# Pagination


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_number_of_items** | **float** |  | 
**previous_page_url** | **str** |  | 
**page_size** | **float** |  | 
**page_number** | **float** |  | 
**page_max_length** | **float** |  | 
**next_page_url** | **str** |  | 

## Example

```python
from ohdieux.ohdio.generated.models.pagination import Pagination

# TODO update the JSON string below
json = "{}"
# create an instance of Pagination from a JSON string
pagination_instance = Pagination.from_json(json)
# print the JSON string representation of the object
print Pagination.to_json()

# convert the object into a dict
pagination_dict = pagination_instance.to_dict()
# create an instance of Pagination from a dict
pagination_form_dict = pagination.from_dict(pagination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


