## [v0.1.13](https://pypi.org/project/amsdal_cli/0.1.13/) - 2024-05-09


### Added

- Added --all option: `amsdal cloud deps --all`. (all-dependencies)
- Added `amsdal --version` command. (amsdal-version)
- Added supporting for multi-word default values, e.g `name:string:default='John Doe'`. (multi-word-default)

### Changed

- Updated `amsdal generate model --help` docs by adding examples. (amsdal-generate-model-help)
- Updated GitHub workflow template to use updated commands. (ci-cd-github)
- Deploy command now allows to install missing dependencies. (deploy-with-dependencies)

### Fixed

- Fixed generating model with 'unique' properties. (amsdal-generate-model-help)


## [v0.1.12](https://pypi.org/project/amsdal_cli/0.1.12/) - 2024-05-03


### Added

- Print GitHub instructions after generating CI/CD config. (ci-cd-instruction)
- Added 'clean' command. (clean-command)

### Changed

- Reorganized CLI commands. Added commands aliases. (reorganized-commands)
