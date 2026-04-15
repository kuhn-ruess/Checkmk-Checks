# Oxidized export

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p5-blue)
<!-- compatibility-badges:end -->

Exports a list of hosts from Checkmk for consumption by
[Oxidized](https://github.com/ytti/oxidized) (network device configuration
backup). The script runs every 15 minutes on the Checkmk site and writes a
JSON file containing hostname and OS for each host returned by a dedicated
Checkmk view.

## How it works

1. The helper script [`export_oxidized`](src/bin/export_oxidized) runs on
   the Checkmk site.
2. It reads the automation secret of the `oxidized` automation user from
   `$OMD_ROOT/var/check_mk/web/oxidized/automation.secret`.
3. It queries the Checkmk REST view `oxidized_hosts` with
   `output_format=json` and extracts hostname and OS tag (matched from the
   second column) for each host.
4. Output is printed as a JSON list:

   ```text
   [
      { "hostname": "sw1.example", "os": "ios" },
      { "hostname": "rtr2.example", "os": "junos" }
   ]
   ```

5. When invoked with `--cron`, it also installs a logrotate config at
   `etc/logrotate.d/export_oxidized` and a cron entry under
   `etc/cron.d/export_oxidized` that runs the export every 15 minutes and
   writes the JSON to `$OMD_ROOT/var/www/open/oxidized.json`.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/bin/export_oxidized` | Site script: queries Checkmk view and emits the Oxidized host list as JSON. Self-installs cronjob and logrotate when run with `--cron`. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create an automation user named `oxidized` and grant it permission to
   read the view `oxidized_hosts` (you must create this view so it returns
   the hostnames and an OS tag of the form `[os_name]` in the second
   column).
3. Run `export_oxidized --cron` once on the site to install the logrotate
   config and the cron entry. From then on the export runs every 15 minutes
   and the resulting JSON file is served from
   `$OMD_ROOT/var/www/open/oxidized.json`, ready to be consumed by Oxidized
   as a source.

## Known limitations

- The target URL is hardcoded to `https://016-mon-001/mon` inside the
  script — adjust the script for your site before installing.
- The cron entry and lock file paths are hardcoded to the `mon` site.
- TLS verification is disabled by default and only re-enabled with the
  `--dis-verify` flag.
