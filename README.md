# PyLC

PyLC is a small CLI tool to solve leetcode problems.

## Installation

Make sure you have python installed in your system.  
Then run `pip install pylc_cli`  
After installation, the `pylc` command will be available. Run `pylc update` to populate the cache database. 

`pylc` or `pylc --help` will display all available subcommands. 

## Submitting problems to server

To submit problems to leetcode servers, the user needs to set their `csrftoken` and `session` variables in `config.toml` (located in `$HOME/.pylc`).  
To get the variables follow this [link](https://github.com/clearloop/leetcode-cli/?tab=readme-ov-file#cookies).

## Boilerplate generation

To make LSPs happy, pylc can add boilerplate code (for example, importing necessary libraries or adding header files).
Edit the `~/.pylc/inject.toml` file.

```toml
# An example
[cpp]
inject_before = ["#include <bits/stdc++.h>", "using namespace std;"]
```

## Credits

This tool is heavily inspired from [clearloop/leetcode-cli](https://github.com/clearloop/leetcode-cli).
