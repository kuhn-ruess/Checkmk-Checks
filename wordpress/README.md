# Wordpress Instance Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0p1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p8-blue)
<!-- compatibility-badges:end -->

Monitors the WordPress core version of every WordPress installation found on a Linux host. A PHP agent plugin discovers WordPress instances, loads each one via `wp-load.php`, asks the WordPress update API whether a newer core is available, and publishes the result as a JSON document in the `<<<wordpress_instances>>>` agent section.

## How it works

1. The bakery ships `wp_instances.php` and a `wp_instances.cfg` config file with `BASEDIR` and `SEARCH_STRING` variables.
2. At runtime, the PHP plugin uses `locate <search_string> | grep <basedir>` to find all WordPress installations under the base directory.
3. For each install it `chdir`s into the WordPress directory, `require`s `wp-load.php`, then calls `wp_version_check`, `wp_update_plugins` and `wp_update_themes` and reads the `update_core`, `update_plugins`, `update_themes` site transients.
4. One JSON record per instance is emitted, wrapped as `{"instances": [...]}` under the `<<<wordpress_instances>>>` header.
5. The check plugin `wordpress_instances` discovers one `Wordpress Core <name>` service per instance and maps the numeric `core_status` (0/1/2) from the PHP plugin directly onto `State.OK` / `WARNING` / `CRITICAL`, reporting installed vs available version. Metric `core_status` is emitted.

The PHP plugin's core-status logic compares `MAJOR.MINOR.PATCH`: a patch-only update yields status 1, a major or minor update yields status 2.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agents/plugins/wp_instances.php` | Linux agent plugin (PHP) that locates WordPress installs and emits JSON. |
| `src/wordpress/agent_based/bakery.py` | Bakery hook that deploys `wp_instances.php` + `wp_instances.cfg`. |
| `src/wordpress/agent_based/wp_instances.py` | Section parser and check plugin (`wordpress_instances`). |
| `src/wordpress/rulesets/bakery.py` | WATO `AgentConfig` rule *Wordpress Monitoring (Linux)*. |

## Installation

1. Install the MKP on the Checkmk site.
2. Make sure the Linux target host has `php`, `locate` (`mlocate`), and access to the WordPress install directory.
3. Deploy the plugin with the bakery rule (below) and bake the agent, or copy `wp_instances.php` manually to the agent plugin directory and create `/etc/check_mk/wp_instances.cfg` with `BASEDIR=...` and `SEARCH_STRING=...`.
4. Run service discovery; one `Wordpress Core <instance>` service will appear per install.

## Configuration

WATO rule: *Setup > Agents > Agent rules > Wordpress Monitoring (Linux)* (topic *Operating System*).

| Parameter | Type | Default | Meaning |
| --- | --- | --- | --- |
| `deployment` | CascadingSingleChoice | `cached` | `sync` (every agent run), `cached` (async with interval), or `do_not_deploy`. |
| `base_dir` | String | `/var/www/sites.d` | Directory prefix used as the `grep` filter over `locate` output. |
| `search_string` | String | `deploy/current` | Filename pattern passed to `locate` to find WordPress roots. |

## Services & metrics

- **Service:** `Wordpress Core <instance>` — one per WordPress install.
- **State logic:** OK when `core_status == 0`, WARN when `1` (patch update available), CRIT when `2` (major/minor update available or WordPress < 3).
- **Metric:** `core_status`.

## Known limitations

- The check plugin has a latent bug in `parse_wp_instances`: it references the undefined name `section` instead of the `string_table` argument and will raise at runtime if the section is non-empty. Fix before production use.
- The PHP plugin requires `locate` / `mlocate`, which must be installed and have an up-to-date database on the target host.
- Plugin and theme update data is collected by the PHP plugin but is not evaluated by the check — only core status is reported as a Checkmk service.
- The agent runs `wp-load.php` for every WordPress instance, which can be slow on hosts with many sites — use the `cached` deployment mode.
