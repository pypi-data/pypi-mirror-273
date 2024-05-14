## Changelog 🔄
All notable changes to `semchunk` will be documented here. This project adheres to [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.4] - 2024-05-13
### Changed
- Improved chunking performance with larger chunk sizes by switching from linear to binary search for the identification of optimal chunk boundaries, courtesy of [@R0bk](https://github.com/R0bk) ([#3](https://github.com/umarbutler/semchunk/pull/3)) ([1e3ddb9](https://github.com/umarbutler/semchunk/pull/3/commits/1e3ddb91698f072da1d8a7d809a66467e1d31ff8)).

## [0.2.3] - 2024-03-11
### Fixed
- Ensured that memoization does not overwrite `chunk()`'s function signature.

## [0.2.2] - 2024-02-05
### Fixed
- Ensured that the `memoize` argument is passed back to `chunk()` in recursive calls.

## [0.2.1] - 2023-11-09
### Added
- Memoized `chunk()`.

### Fixed
- Fixed typos in README.

## [0.2.0] - 2023-11-07
### Added
- Added the `memoize` argument to `chunk()`, which memoizes token counters by default to significantly improve performance.

### Changed
- Improved chunking performance.

## [0.1.2] - 2023-11-07
### Fixed
- Fixed links in the README.

## [0.1.1] - 2023-11-07
### Added
- Added new test samples.
- Added benchmarks.

### Changed
- Improved chunking performance.
- improved test coverage.

## [0.1.0] - 2023-11-05
### Added
- Added the `chunk()` function, which splits text into semantically meaningful chunks of a specified size as determined by a provided token counter.

[0.2.4]: https://github.com/umarbutler/semchunk/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/umarbutler/semchunk/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/umarbutler/semchunk/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/umarbutler/semchunk/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/umarbutler/semchunk/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/umarbutler/semchunk/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/umarbutler/semchunk/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/umarbutler/semchunk/releases/tag/v0.1.0