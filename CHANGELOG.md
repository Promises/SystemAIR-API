# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub issue templates
- Pre-commit hooks configuration
- More comprehensive error handling
- CONTRIBUTING.md with contribution guidelines
- CHANGELOG.md to track changes
- LICENSE file with MIT license
- MANIFEST.in file for package distribution
- Development dependencies in requirements-dev.txt

### Changed
- Improved package setup with proper metadata
- Enhanced documentation with more usage examples
- Updated README with PyPI installation instructions
- Refactored code structure for better organization
- Improved logging throughout the codebase

### Fixed
- Token refresh handling

## [0.1.0] - 2025-03-15

### Added
- Initial release
- Authentication with Systemair Home Solutions cloud
- Token management with automatic refresh
- Real-time monitoring via WebSocket connection
- Retrieve unit information and status
- Control ventilation modes and airflow levels
- Monitor temperatures, humidity, and air quality
- View and manage alarms
- Track active functions (heating, cooling, etc.)
- Unit testing suite with >85% code coverage