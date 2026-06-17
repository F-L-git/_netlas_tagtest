# _netlas_tagtest
> checking the operation of tags to improve the search as part of the _netlas utility

Testing allows you to create an up-to-date catalog of working tags that can be used in other projects.

## Key technical details
### API and authentication
- All requests require an API key, which is obtained on the Netlas [profile page](https://app.netlas.io/profile/)
- The key is passed when creating the object `netlas.Netlas(api_key=api_key)'
- The SDK handles basic errors automatically, but the scripts have added their own retry logic

### Rate Limits
- The `Netlas API' has limits on the number of requests (depends on the subscription).
- The scripts implement the processing of the 'Request limit' error with a pause of 60 seconds before trying again.
- A 1-second delay has been added between checks of different tags.

> [!TIP]
> Script structure
> - `tag_test_1.1.py` — basic test (tag + version).
> - `tag_test_1.1_focus.py` — advanced test with detailed logging.
> - `tag_test_1.1_version_support.py` — version support test only.

### Query format
- Search by tag: `tag.name:nginx`
- Search by tag version: `tag.nginx.version:1.18.0`
- Version support check: `tag.nginx.version:<10000` (finds all records with any version)

### Additional context
  Netlas uses **passive scanning** — it does not send malicious requests, but only analyzes the public responses of the services. This makes it a safe tool for exploration. Tags are a key element of this system. They allow not only to identify technologies, but also to link them to known vulnerabilities (CVEs).

  Understanding which tags work and which versions support is critical for:
- **Search for vulnerable systems** (for example, `tag.apache.version:2.4.49`)
- **Analysis of the technological stack of companies**
- **Automation of OSINT fees via API**
