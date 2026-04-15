# EMC Checks based on df

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p9-blue)
<!-- compatibility-badges:end -->

Adds filesystem monitoring for EMC VNX pools and EMC Server mpfs filesystems by reusing Checkmk's built-in `df` check logic. Two sections (`emc_vnx_pool`, `emc_server_df`) are parsed with the same parser that Checkmk uses for `df`, so levels, inode handling, grouping and the `filesystem` ruleset behave exactly like the native check.

## How it works

Agents or monitoring sources that can produce `df`-style output emit sections `<<<emc_vnx_pool>>>` and `<<<emc_server_df>>>`. The plugin [`filesystems.py`](src/emc/agent_based/filesystems.py) imports `discover_df`, `check_df`, `BlocksSubsection`, `InodesSubsection` and `FILESYSTEM_DEFAULT_PARAMS` from Checkmk's bundled `df` implementation, provides its own `parse_df()` copy (to keep the parser stable against upstream changes) and registers two check plugins that share it.

Services:

- `Filesystem EMC VNX Pool <mountpoint>`
- `Filesystem EMC Server mpfs <mountpoint>`

Both use `check_ruleset_name = "filesystem"` and `discovery_ruleset_name = "inventory_df_rules"`, so all existing filesystem rules apply.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/emc/agent_based/filesystems.py` | Parser plus two `CheckPlugin`s wired to the native `df` discovery and check functions. |

## Installation

1. Install the MKP on the Checkmk site.
2. Feed the appropriate `<<<emc_vnx_pool>>>` / `<<<emc_server_df>>>` sections into the relevant host (from a custom agent, a piggyback source, or a script on the storage platform).
3. Run service discovery.

## Known limitations

- The plugin imports internal modules from `cmk.base.plugins.agent_based.utils.df` and `cmk.base.plugins.agent_based.df`. These are not public APIs and may move or change between Checkmk versions.
- This package only supplies check plugins; it does not include an agent or special agent to collect the sections on its own.
