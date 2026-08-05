# ChangeLog

## v2.0.0 - 2026-8-04

### Added

- Added verification for password existence.
- Added 3 other example requests in [api.md](api.md)
- Added searching feature with the `search` query parameter

### Changed

- Updated response formats to match API docs at [api.md](api.md).
- Overrided the default values for `PASSWORD` and `USER` env variables.
- Improved documentation.

### Fixed

- Fixed max length of the `title` property to _50_ instead of _49_, for _create_ and _update_ routes.
- Fixed error responses to be consistent.

### Removed

- Removed `title` path parameter to prevent conflicts with `search` paramater.

### Security

- Solved dupliate IDs edge case in `/delete/`

## 2.0.1 - 2026-8-05

### Fixed

- Removed trailing slashes in the main _APIRouter_ object.
- Fixed SQL Queries structure to enable Ordering by IDs.
