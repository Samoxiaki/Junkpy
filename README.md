# Junkpy
Junkpy is a Python library for processing Junk configuration files.


## Junk File Format
Junk is a file format for configuration files that extends the capabilities of the standard JSON format by introducing additional options and features.


### Junk Features Overview
- Unquoted Keys:
```json
{
  unquoted_key: "value",
  another_unquoted_key: 42
}
```

- Trailing Commas in Objects and Arrays:
```json
{
  "key1": "value1",
  "key2": "value2",
  "key3": "value3",
}
```
```json
[
  "item1",
  "item2",
  "item3",
]
```

- Implicit null values:
```json
{
  "null_key": null,
  "empty_value": ,
}
```

- Comments:
```json
{
    "key1": "value1",     # This is a comment about key1
    "key2": "value2",     # This is a comment about key2
    "key3": "value3"      # This is a comment about key3
}
```

- Type conversion and custom types:
```json
{
	"int_value": (int) "123",
	"float_value": (float) "3.14",
	"string_value": (string) 456,
	"chained_types_value": (string) (int) 99.99,
	"custom_type_value": (custom_type) "abcd",
	"array_with_different_types": [
		(int) 55.6,
		(float) 88,
		(string) 1234,
	]
}
```
- Arguments on type conversion:
```json
{
	"custom_type_value1": (custom_type, arg1 = 33, arg2 = "1234") 333,
	"custom_type_value2": (custom_type, arg1 = (int) 99.5, arg2 = (string) 5678) 444,
}
```


## Installation
You can install Junkpy using `pip`. Open your terminal and run the following command:

```shell
pip install junkpy
```

## Usage
To use the Junkpy library in your Python projects, follow these steps:

1. Import the `JunkParser` class from the `junkpy` module:

```python
from junkpy import JunkParser
```

2. Create an instance of the `JunkParser` class:

```python
junk_parser = JunkParser()
```

3. Load data from a file using the `load_file()` method:

```python
data = junk_parser.load_file("file.junk")
```

Replace `"file.junk"` with the path to your own file.

The `load_file(file_path)` method reads the contents of the specified file and processes it using the Junk parser.

Avalaible load methods:
- `load_file(file_path)` parses data from a file.
- `loads(string)` parses data from a string.
- `load(fp)` parses data from a file-like object.
- `load_file_from_env(env_var)` parses data from a file specified in an environment variable.


### Pydantic support
All load methods support validation to pydantic models with the `validate_to` parameter:

```python
from junkpy import JunkParser
from pydantic import BaseModel

class TestModel(BaseModel):
	key1: int
	key2: str


junk_parser = JunkParser()
data = junk_parser.load_file("file.junk", validate_to=TestModel)

assert isinstance(data, TestModel) # True

```


### Custom Type Processors
The `junkpy` library allows you to create custom type processors to manage how a Junk file is parsed. Here's an example of how you can create one:

```python
from junkpy import JunkParser, JunkTypeProcessor

class BoundedValueTypeProcessor(JunkTypeProcessor):
    CLASS = float  # Output class
    KEYWORD = "bounded-value"  # Custom type keyword

    def load(self, value, **kwargs):
        obj = self.CLASS(value)
        
        if "min" in kwargs:
            obj = max(kwargs["min"], obj)
            
        if "max" in kwargs:
            obj = min(kwargs["max"], obj)
            
        return obj


# Instantiate the Junk parser with a list of custom type processors
junk_parser = JunkParser([BoundedValueTypeProcessor])
```

A basic type processor class requires defining `CLASS` and `KEYWORD` attributes and `load` method.
- `CLASS`: Defines the output type of the processed value. __Type checking is performed after the value has been processed.__
- `KEYWORD`: A string that will trigger this type processor when parsing data.`
- `load`: An instance method aimed at processing and returning a value given its parameters:
	- `self`: Reference to the own type processor instance.
	- `value`: The value to be processed. This object could be of any type.
	- `**kwargs`: Keyword arguments received from data being parsed.

Every type processor contains a shared property called `metadata` which can be accessed inside `load` method. This property stores the following data:
- `file_path`: Path of the current file being parsed, if any, otherwise `None`.

The `metadata` can also be used to store data and share it across different type processors.

Retrieve the current parser instance from the `parser` property of type processors. This allows parsing data recursively while processing is ongoing.

By including your custom type processor during the parser's initialization, you enable the parser to recognize and apply the specified modifications when loading files.

Note: Not all type conversions in Junkpy can be initialized with a null value. For example, when a `null` value is converted to the type `(string)`, a Python string object with the value `"None"` will be created. However, if the type is `(int)`, it will result in an error since `null` cannot be converted to an integer. It's important to exercise caution when using type conversions and ensure they are compatible with null values.


### Extending the Parser Class

Junkpy provides the flexibility to extend and customize the parsing process by subclassing the `JunkParser` class and overriding two extensible methods: `before_parsing` and `after_parsing`. These methods allow you to perform additional actions or processing steps before and after parsing Junk files.

The `before_parsing` method is called before the parsing of a Junk file begins. It receives `metadata`, which contains information about the file being parsed. You can use this method to perform any pre-processing tasks or set up configurations specific to your needs.

```python
class MyCustomParser(JunkParser):
    def before_parsing(self, metadata: JunkMetadata):
        # Perform pre-processing tasks or configuration setup here

```

The `after_parsing` method is called after the parsing of a Junk file is complete. It receives `metadata`, which contains information about the parsed file, and `parsed_data`, which is the resulting parsed data as an object. You can use this method to perform any post-processing tasks, validation, or additional actions on the parsed data.

```python
class MyCustomParser(JunkParser):
    def after_parsing(self, metadata: JunkMetadata, parsed_data: object) -> object:
        # Perform post-processing tasks or validation on parsed_data here
        # Return the modified parsed_data
        return parsed_data
```

### Built-in types

| Type       | Return Value        | Supported Values                                                                              | Example Initialization                                                                                         |
|------------|---------------------|-----------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| string     | str                 | Any string value                                                                              | (string) "Hello, World!"                                                                                       |
| regex      | re.Pattern          | Valid regular expression patterns                                                             | (regex) "[A-Za-z]+[0-9]*"                                                                                      |
| env        | str                 | Environment variable names/expresions                                                         | (env) "$HOME"                                                                                                  |
| path       | pathlib.Path        | File system paths (environment variables supported on path string)                            | (path) "$HOME/path/to/file.txt"                                                                                |
| int        | int                 | Integer values                                                                                | (int) 123                                                                                                      |
| bin        | int                 | Binary integer values                                                                         | (bin) "10101"                                                                                                  |
| octal      | int                 | Octal integer values                                                                          | (octal) "123"                                                                                                  |
| hex        | int                 | Hexadecimal integer values                                                                    | (hex) "1234567890ABCDEF"                                                                                       |
| complex    | complex             | Complex number values                                                                         | (complex) "3+4j"                                                                                               |
| float      | float               | Floating-point values                                                                         | (float) 3.14159                                                                                                |
| decimal    | decimal.Decimal     | Decimal values                                                                                | (decimal) "3.14"                                                                                               |
| bool       | bool                | Boolean values                                                                                | (bool) true                                                                                                    |
| set        | set                 | Sets of values                                                                                | (set) [1, 2, 3]                                                                                                |
| timestamp  | datetime.datetime   | Unix timestamp values                                                                         | (timestamp) 1623345600                                                                                         |
| timedelta  | datetime.timedelta  | Time differences in seconds                                                                   | (timedelta) 60                                                                                                 |
|            |                     | Time differences in a list [DAYS, SECONDS, MICROSECONDS, MILLISECONDS, MINUTES, HOURS, WEEKS] | (timedelta) [5, 10, 200, 150, 3, 4, 8]                                                                         |
|            |                     | Time differences in a dict with keyword arguments as keys                                     | (timedelta) {"days": 1, "seconds": 3600}                                                                       |
| time       | datetime.time       | Time values in ISO 8601 format, [HH[:MM[:SS[.mmm[uuu]]]]][+HH:MM]                             | (time) "12:30:45"                                                                                              |
|            |                     | Time values in a list [HOUR, MINUTE, SECOND, MICROSECOND]                                     | (time) [12, 30, 45, 152]                                                                                       |
|            |                     | Time values in a dict with keyword arguments as keys                                          | (time) {"hour": 12, "minute": 30, "second": 45}                                                                |
| date       | datetime.date       | Date values in ISO 8601 format, YYYY-MM-DD                                                    | (date) "2021-07-10"                                                                                            |
|            |                     | Date values in a list [YEAR, MONTH, DAY]                                                      | (date) [2021, 7, 10]                                                                                           |
|            |                     | Date values in a dict with keyword arguments as keys                                          | (date) {"year": 2021, "month": 7, "day": 10}                                                                   |
| datetime   | datetime.datetime   | Date and time values in ISO 8601 format, YYYY-MM-DD [HH[:MM[:SS[.mmm[uuu]]]]][+HH:MM]         | (datetime) "2021-07-10 12:30:45"                                                                               |
|            |                     | Date and time values in a list [YEAR, MONTH, DAY, HOUR, MINUTE, SECOND, MICROSECOND]          | (datetime) [2021, 7, 10, 12, 30, 45, 580]                                                                      |
|            |                     | Date and time values in a dict with keyword arguments as keys                                 | (datetime) {"year": 2021, "month": 7, "day": 10, "hour": 12, "minute": 30, "second": 45}                       |


## Contributing

Contributions to Junkpy are welcome! If you encounter any issues, have suggestions for improvements, or would like to add new features, please feel free to submit a pull request. 

To contribute to Junkpy, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Implement your changes.
4. Write tests to ensure the correctness of your code.
5. Commit and push your changes to your forked repository.
6. Open a pull request and provide a detailed description of your changes.


## License

Junkpy is released under the [GNU GPLv3](https://github.com/samoxiaki/junkpy/blob/main/LICENSE.txt) license. You are free to use, modify, and distribute this library as per the terms of the license.

## Support

If you need assistance or have questions about Junkpy, please feel free to [open an issue](https://github.com/samoxiaki/junkpy/issues) on the GitHub repository. We'll be happy to assist you.