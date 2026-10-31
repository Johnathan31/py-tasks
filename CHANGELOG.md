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

## v2.0.0 - 2026-10-31

### Added

- [c51a105](https://github.com/Johnathan31/py-tasks/commit/c51a105297db1f94285c786bace204a8b434b44a): Added Docker support.
- [3280d31](https://github.com/Johnathan31/py-tasks/commit/3280d31032feca25d09b4100331424ac1410e244): Added test coverage.

### Changed

- [5d1a51d](https://github.com/Johnathan31/py-tasks/commit/5d1a51dd7f08d681f912c84374a2ccadf8911677): Renamed environment variables.

### Fixed

- [12e75d8](https://github.com/Johnathan31/py-tasks/commit/12e75d89894e4906154c61a0a3fe3fc46dfe497a): Fixed some Docker config and database config.
- [03d823e](https://github.com/Johnathan31/py-tasks/commit/03d823e2a9e15d615c0469899160e0439484157e): `start.sh` is now executable by default.

### features

- [82eedaf](https://github.com/Johnathan31/py-tasks/commit/82eedafd6c1ae88fa62be1f9b28982387e0d5e9f): `priority` and `done` are now optional fields.
