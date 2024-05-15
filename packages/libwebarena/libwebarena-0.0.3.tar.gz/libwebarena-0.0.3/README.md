**Warning: use at your own risks!**

Unofficial [WebArena](https://github.com/web-arena-x/webarena) port for compatibility with [BrowserGym](https://github.com/ServiceNow/BrowserGym). Changes below.

More flexible/recent dependencies
 - playwright>=1.32,<1.40
 - openai>=1
 - transformers

Packaging into a single Python namespace
```bash
pip install libwebarena
```

```python
import webarena
import webarena.browser_env
import webarena.agent
import webarena.evaluation_harness
import webarena.llms
import webarena.llms.providers
```

Making `HTMLContentEvaluator` idempotent (`validate()` should not alter the browser's state)
