# etc

This directory contains configuration files for the application commands.

## config.yaml

YAML file containing application-specific configuration. This file should
contain application configuration that does not change when running on
the test/qa/production servers.

Configuration that may change based on which server the application is running
on should be placed in the ".env" environment configuration file (see the
"env_example" file).

## circrequests_FIRST.json

Contains an empty JSON array, so that the first run of "circrequests"
automatically considers all entries in the first source response to be new
items.

## items_FIRST.json

Contains an JSON file with the initial "last query" timestamp to send to
Aleph on the first run of "items".
