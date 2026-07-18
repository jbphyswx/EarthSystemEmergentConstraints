# earth_system_emergent_constraints

Python client for the EarthSystemEmergentConstraints catalog.

```python
from earth_system_emergent_constraints import load_registry, load_collection

reg = load_registry()
c = reg["hall_qu_2006_snow_albedo"]
print(c.status, c.citation.doi)

starter = load_collection("starter")
```

Set `ESEC_DATA_ROOT` to the monorepo root if needed.
