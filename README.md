# Junkpy: Extended JSON Library for Configuration Files.

Junkpy is a Python library specifically designed for working with configuration files in JSON format. It offers a flexible approach to handling JSON objects, allowing for easier modification and manipulation of configuration data. With Junkpy, you can work with a more lenient syntax, accommodating variations in JSON structure commonly found in configuration files.

## Features

- **JSON Configuration Handling**: Junkpy focuses on managing JSON as configuration files, ensuring compatibility and ease of use.
- **Flexible Syntax**: Junkpy supports a more relaxed syntax, allowing for variations and non-strict JSON structures commonly found in configuration files.
- **Value Modification**: Modify values within JSON configuration files using a straightforward syntax provided by Junkpy.
- **Class Assignment**: Assign specific classes or attributes to JSON values, enabling better organization and categorization of configuration data.
- **Extensible Modification Capabilities**: Junkpy provides an extensible framework that allows you to incorporate your own custom value modifiers, giving you the freedom to adapt and extend the library's functionality according to your specific requirements.
- **Seamless Integration**: Junkpy can seamlessly integrate into your Python projects, providing enhanced configuration handling capabilities.

## Installation

You can install Junkpy using `pip`. Open your terminal and run the following command:

```shell
pip install junkpy
```

## Usage

To use the Junkpy library in your Python projects, follow these steps:

1. Import the `Junkpy` class from the `junkpy` module:

```python
from junkpy import Junkpy
```

2. Create an instance of the `Junkpy` class:

```python
junkpy_parser = Junkpy()
```

3. Load data from a file using the `load_file()` method:

```python
data = junkpy_parser.load_file("file.junk")
```

Replace `"file.junk"` with the path to your own file.

The `load_file(file_path)` method reads the contents of the specified file and processes it using the Junkpy parser, returning the loaded data.
Additional methods such as `loads(string)` and `load(fp)` parse data from a string or a file-like object respectively.


### Custom Type Processors

The `junkpy` library allows you to create custom type processors to extend its functionality and tailor it to your specific needs. Here's an example of how you can create one:

```python
from junkpy import Junkpy, JunkpyTypeProcessor

class BoundedValueTypeProcessor(JunkpyTypeProcessor):
    CLASS = float  # Output class
    KEYWORD = "bounded-value"  # Modifier keyword

    def load(self, value, file_path, **kwargs):
        obj = self.CLASS(value)
        
        if "min" in kwargs:
            obj = max(kwargs["min"], obj)
            
        if "max" in kwargs:
            obj = min(kwargs["max"], obj)
            
        return obj


# Instantiate the Junkpy parser with the custom type processor
junkpy_parser = Junkpy([BoundedValueTypeProcessor])
```

A basic type processor class requires defining `CLASS` and `KEYWORD` attributes and `load` method.
- `CLASS`: Defines the output type of the processed value. Type checking is performed after the value has been processed.
- `KEYWORD`: A string that will trigger this type processor when parsing data.`
- `load`: An instance method aimed at processing and returning a value given its parameters:
	- `self`: Reference to the own type processor instance.
	- `value`: The value to be processed. This object could be of any type.
	- `file_path`: A `Path` object containing the path of the current file being processed if any, otherwise `None`.
	- `**kwargs`: Keyword arguments received from data being parsed.


By including your custom type processor in the parser's initialization, you enable the parser to recognize and apply the specified modifications when loading files.

## Feature Overview
### Autodetected Values

The Junkpy library supports autodetection of JSON-like values, which means it can handle values that are identical to those in regular JSON. Here's an example of various autodetected values:

```json
{
  "string_value": "Hello, world!",
  "integer_value": 42,
  "float_value": 3.14,
  "boolean_value": true,
  "array_value": [1, 2, 3],
  "object_value": {"key": "value"},
  "null_value": null
}
```

### Unquoted Keys

Junkpy allows unquoted keys in JSON-like data. This means that keys can be specified without enclosing them in double quotes (`"`).
It's important to note that while unquoted keys are supported in Junkpy, they are not part of the standard JSON syntax.

```json
{
  unquoted_key: "value",
  another_unquoted_key: 42
}
```

### Trailing Commas in Dictionaries and Lists

Junkpy allows both dictionaries and lists to have a trailing comma after the last element. This means that you can include a comma at the end of the last key-value pair in a dictionary or the last item in a list, or omit it without causing a syntax error.

#### Trailing Comma in a Dictionary
```json
{
  "key1": "value1",
  "key2": "value2",
  "key3": "value3",
}
```

#### Trailing Comma in a List
```json
[
  "item1",
  "item2",
  "item3",
]
```

Junkpy can handle both cases, with or without the trailing comma, when parsing the JSON-like data.

### Null Values

Junkpy supports the concept of null values, where the absence of a value is represented as `null`. When a key-value pair has no value assigned, Junkpy treats it as a null value. Here are examples of null values in different scenarios:

#### Null Values without Forced Types

```json
{
  "null_key": null,
  "empty_value": 
}
```

- `"null_key"`: The key `"null_key"` is explicitly assigned a null value. In Python it will be converted to `None`.
- `"empty_value"`: The key `"empty_value"` has no value assigned, resulting in a null value.


#### Null Values with Forced Types

```json
{
  "empty_value_as_string": (string) ,
  "empty_value_as_custom_type": (custom_type) 
}
```

- `"empty_value_as_string"`: The key `"empty_value_as_string"` has a forced type `(string)` with a value treated as null.. The Python representation will be a string object with the value `"None"`.
- `"empty_value_as_custom_type"`: The key `"empty_value_as_custom_type"` has a forced type `(custom_type)` with a value treated as null. The behavior will depend on the implementation of the custom type.

Note: Not all forced types in Junkpy can be initialized with a null value. For example, when a forced type is `(string)`, a Python string object with the value `"None"` will be created. However, if the forced type is `(int)`, it will result in an error since null cannot be converted to an integer. It's important to be cautious when using forced types and ensure they are compatible with null values.

### Comments

Junkpy allows you to include comments in your configuration files using the `#` symbol. Comments are ignored during parsing and serve as annotations or explanations for the configuration.

Here's an example showcasing the usage of comments:

```json
{
    "key1": "value1",     # This is a comment about key1
    "key2": "value2",     # This is a comment about key2
    "key3": "value3"      # This is a comment about key3
}
```

### Forced Types

Junkpy allows you to force specific types for values by using type modifiers. These modifiers can be placed in front of any value (except keys) to indicate the desired type. You can also chain multiple type modifiers together or include arguments within the forced value itself.

#### Single Forced Type
```json
"forced_int": (int) "123",
"forced_float": (float) "3.14",
"forced_string": (string) 456,
```

In the examples above, the values are forced to be of the specified type (`int`, `float`, and `string`). Junkpy will perform the necessary conversion during parsing.

#### Chained Forced Types
```json
"forced_multiple_types": (string) (int) (float) "123",
```

In this case, multiple forced types are chained together for the value "123". Junkpy will attempt to convert the value to each specified type in the order they appear (from left to right).

#### Forced Types with Arguments
```json
"forced_with_arguments": (custom_type, arg1=5, arg2="test") 123,
```

With the given example, the value "123" is forced to a custom type (`custom_type`) with two arguments (`arg1` and `arg2`). The arguments are specified within parentheses after the forced type.

#### Forcing Value Types in Different Contexts
This example showcases the different scenarios where you can force the type of a value:

```json
{
    "dict_with_forced_types": {
        "key1": (string) "value1",
        "key2": (int) "123",
        "key3": (float) "3.14"
    },
    "list_with_forced_types": [
        (string) "value1",
        (float) 3.14159,
        (int) "123"
    ],
    "custom_type_with_forced_type_argument": (custom, arg=(int) "10") "example"
}
```

- In the dictionary example, the forced value types are applied to its values. This ensures that the values for "key1", "key2", and "key3" have specific data types: string, integer, and float respectively.
- Forced value types can also be used in lists. In the example, the list "list_with_forced_types" contains elements with enforced types, including a string, a float, and an integer.
- The arguments of a forced type modifier can also have a forced type. The modifier of "custom_type_with_forced_type_argument" has an argument of forced integer type.

#### Built-in types

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
6. Open a pull request, providing a detailed description of your changes.


## License

Junkpy is released under the [GNU GPLv3](https://github.com/samoxiaki/junkpy/blob/main/LICENSE.txt). You are free to use, modify, and distribute this library as per the terms of the license.

## Support

If you need any assistance or have any questions regarding Junkpy, please feel free to [open an issue](https://github.com/samoxiaki/junkpy/issues) on the GitHub repository. We'll be happy to help you.
