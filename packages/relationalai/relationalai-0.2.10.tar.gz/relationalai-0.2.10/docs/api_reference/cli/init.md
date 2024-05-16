# `init`

```sh
rai init
```

Initialize a new project.

`rai init` walks you through setting up a RelationalAI project,
connecting to a cloud platform, and saving a configuration file.

The first time you run `rai init`, you will be prompted to enter your connection information:

- **For Snowflake:** Enter your Snowflake username and password.
  Then, select the Snowflake account and role to use for the project.
  The account must have the RelationalAI Native App installed and the role must be granted permission to use the app.
  Finally, select the RelationalAI native app and Snowflake compute warehouse to use with your project.
- **For Azure:** Enter your RelationalAI OAuth client ID and client secret.
  See [RAI Accounts, User Profiles, and OAuth Clients](https://docs.relational.ai/preview/snowflake/integration-management/accounts)
  for more information.

Connection information and other settings are saved in a `raiconfig.toml` file in the same directory from which `rai init` is run.
You have the option of saving your settings as the default configuration profile or as a named profile.

The next time you invoke `rai init`, the current working directory and its parents are searched for a `raiconfig.toml` file.
If an existing configuration file is found, settings from the default profile are presented as suggestions.
You may override these suggestions as needed.
