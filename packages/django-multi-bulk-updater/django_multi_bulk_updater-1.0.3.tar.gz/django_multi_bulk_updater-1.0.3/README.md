# django-multi-bulk-updater

```
from django_multi_bulk_updater import ParallelyQueryExcecutor

ParallelyQueryExcecutor().Multi_Parallel_Bulk_Update(
    yourModel=YourModelName,
    results=yourResultsList,
    fields=["field1", "field2"],
    batch_size=1000,
)
```
For more info, please read the [blog](https://medium.com/@sushilprasad60649/unlocking-the-power-of-row-level-updates-with-our-latest-package-ccc11d148c85).