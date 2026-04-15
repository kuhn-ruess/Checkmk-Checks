# Agent JSON

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p9-blue)
<!-- compatibility-badges:end -->

Will query via HTTP JSON data and parse it for usage as local check.


## Result format needed:

```
{'checks', [{’name': 'My Check', ’status': 'UP', 'data': {'info1': „info', ’infox': 'more info'}]}
```
