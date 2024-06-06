# pylc

pylc is a small CLI tool to solve leetcode problems.

## Installation

Make sure you have python installed in your system.  
Then run `pip install pylc_cli`  
After installation, the `pylc` command will be available.  

Run `pylc update` to populate the cache database.  
Open up your config.toml file (located at $HOME/.pylc) and paste your `session` and `csrftoken` values.

Commands:

```bash
pylc pick <id> # Display problem statement
pylc solve <id> # Open up your editor (default editor is vim)
pylc test <id> # Send your typed code to leetcode servers for testing
pylc submit <id> # Submit your code
pylc update # Updates the cache database
```
