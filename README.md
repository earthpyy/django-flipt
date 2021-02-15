# django-flipt

<p>
<img src="https://img.shields.io/pypi/v/django-flipt">
<img src="https://img.shields.io/pypi/l/django-flipt">
<img src="https://img.shields.io/pypi/pyversions/django-flipt">
<img src="https://img.shields.io/pypi/dm/django-flipt">
<img src="https://img.shields.io/github/workflow/status/earthpyy/django-flipt/CI/main">
<img src="https://img.shields.io/github/workflow/status/earthpyy/django-flipt/CodeQL/main?label=CodeQL">
</p>

<p>Flipt Integration for Django and Django REST Framework</p>

## Installation

```shell
pip install django-flipt
```

## Usage

1. Add `flipt` into `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...
    'flipt',
]
```

2. Define Flipt gRPC endpoint in `settings.py`

```python
FLIPT_GRPC_HOST = 'flipt:9000'
```

3. Ready to go!

### Overriding Flags

You can override any flag by defining your flag key and overriding value

```python
FLAG_OVERRIDDEN = {
    'some-flag-key': True
}
```

### Available Classes/Functions

- `flag_enabled`
- `flag_disabled`
- `FlaggedRouter`
- `@flag_check`
- `@override_flags`
- `{% featureflag %} ... {% endfeatureflag %}`
- `FeatureFlagListView`

## Development

### Requirements

- Docker

### Run Project

```shell
$ make
```

### Linting/Test Project

```shell
$ make lint
$ make test
```

## Credits

- [Flipt](https://flipt.io)
- Inspired by [django-flags](https://github.com/cfpb/django-flags)
