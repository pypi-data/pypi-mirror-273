# Frequenz Weather API Release Notes

## Summary

## Upgrading

- The location and pagination proto files are now again imported from the
 ´frequenz-api-common´ submodule instead of being imported from local files.
 The local files are removed.

- The required version of the ´frequenz-channels` is updated to 1.0.0.

- The required version of the ´frequenz-client-base` dependency is updated to v0.3.x.

## New Features

- The client has been extended to iterate over historical weather forecast data.

- Historical location forecast data pages are now exposed as a flattened numpy array for easier use.

## Bug Fixes
