# Actions-python

## Overview
Actions-python is a Python package designed to manage actions with event-driven behavior. 
It provides a flexible way to connect handlers (callbacks) to actions, ensuring that handler argument types are 
validated before invocation. This helps maintain strict type consistency while enabling dynamic behavior 
in event-driven systems.

## Features
- **Event-driven architecture**: Connect handlers to actions and invoke them when the action is triggered.
- **Type validation**: Ensures that handler argument types match the expected types defined when the action is initialized.
- **Dynamic handling**: Allows flexible addition of handlers at runtime, each with its own argument type validation.
- **Supports multiple argument types**: Can handle multiple types of arguments for a single action.

## Installation

To install the project you can use pip:

```bash
pip install https://github.com/Allorak/actions-python
```

Or install from PyPI index:
```bash
pip install actions_python
```

## Core ideas
- Actions: An action is an event that can have one or more handlers (callbacks) connected to it. 
When the action is triggered, all handlers are invoked with the specified arguments.
- Handlers: Callbacks that are connected to actions. 
Each handler should expect arguments of a specific type, 
which are validated at both the connection stage and the invocation stage.
- Type validation: When a handler is connected, the types of its arguments are validated to ensure they match the
expected types. Similarly, when invoking the action, arguments are validated against the expected types.

## Example

Usage examples can be found in `examples/` folder