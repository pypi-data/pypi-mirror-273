# configureout

Configureout is a lightweight Python module designed to simplify the process of loading and accessing configuration data from JSON files. It provides a simple and intuitive interface for managing configuration settings within your Python applications.

## Features

- **Easy Configuration Loading:** Configureout allows you to load configuration settings from JSON files with just a few lines of code.
- **Nested Configuration Support:** Easily access nested configuration settings using dot notation.
- **Flexible and Extensible:** The module can be easily extended to suit your specific needs, allowing for customization and flexibility.
- **Pythonic Interface:** Configureout provides a Pythonic interface for accessing configuration settings, making it easy to integrate into your projects.

## Installation

You can install configureout via pip:

```
pip install configureout
```

## Usage

```
from configureout import Config

# Load configuration from a JSON file
config = Config("config.json")

# Access configuration settings
print(config.setting_name)
print(config.section.subsection.another_setting)
```

## Example
Consider the following JSON configuration file ('config.json'):
```
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "username": "user",
    "password": "password"
  },
  "logging": {
    "level": "info",
    "file_path": "/var/log/app.log"
  }
}
```
With configureout, you can easily load and access these settings in your Python code:
```
from configureout import Config

config = Config("config.json")

# Access database host
print(config.database.host)

# Access logging level
print(config.logging.level)
```

## License
This project is licensed under the MIT License