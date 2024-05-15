### Sample Usage

```
indexer = CarbonRegistryIndexer(azure_blob_conn_str='your_conn_str', 
                            azure_blob_container='your_container_name')
indexer.setup_storage()  # creates or purges data folder

# functions to initiate specific sync calls
indexer.sync_gold_standard()
indexer.sync_climate_action_data_trust()
indexer.sync_american_carbon_registry()
indexer.sync_climate_action_reserve()
```
