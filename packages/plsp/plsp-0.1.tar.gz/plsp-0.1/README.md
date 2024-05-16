# Please Log Shit Please (or `plsp`)

## Notes

```text
info inject is a module allowing you to compile python source code with added debug information.
this means that the interesting parts of the code stay separate from printing and other debug code.
```

```text
=====================
Pieces of the puzzle.
=====================

Logger 			- The piece that does the logging.

DebugContext 		- Use this along side with the logger to separate different areas of an application.
			- For example, you may have a rendering context and a physics context inside a game engine.

DebugMode 		- Use this to specify different levels of debug information.
			- For example, you may have a "info" mode and a "detail" mode.
			- If the "info" mode is active, any messages that are in the "detail" mode will not be printed.
			- This is because the "detail" mode extends from the "info" mode.
			- If the "detail" mode is active, any messages that are in the "info"
			-   and "detail" mode will be printed.

ColorConfiguration 	- Use this to specify the colors of the debug information.
			- For example, you may want to have the rendering context to be in green
			-   and the physics context to be in red.

InfoInjector 		- The piece that injects the debug information into the source code.
			- Uses the Logger to log the debug information.

formatters/ 		- The pieces that format the debug information.
			- For example, you may want to have the time of the debug information to
			-   be formatted in a specific way.
			- You may also want to have the caller of the debug information to be formatted in a specific way.
			- The formatters may be added onto any specified debug context. Then, when the Logger is used
			-   by said context, the formatters will be used to format the debug information.



====================================
How the pieces relate to each other.
====================================

> Nodes A that is down from node B means that A depends on, or is used by, B.

	Logger
	/ \
	+  +--------------------+
	|                       |
	Debug Context           Debug Mode
	/ \
	+  +--------------------+
	|                       |
	Color Configuration     formatters/
```

## Usage

```python
from pls.Logger import plsp
#from formatters import TimeFormatter, CallerFormatter
from plsp.DebugMode import DebugMode
from plsp.Direction import IODirection

import sys

# use below to separate log files based on debug mode instead of debug context.
#plsp.set("io_based_on_mode", True)



# The below sets the global context to generic.
plsp.set("global_context", "generic")



# Below is adding a debug context.
# It is a bit more complicated than setting up debug contexts so you dont have to set all the parameters at once.
plsp.add_debug_context("generic")
plsp.add_debug_context("rendering")
plsp.add_debug_context("physics")



# Below is adding a debug mode.
# You can:
# - Use the `write_to_file` parameter to specify a file to write to.
# - Use the `write_to_io` parameter to specify an io object to write to.
# - Use the `separate` parameter to specify if this is a standalone debug mode, meaning, if this mode is active,
#     the previous debug mode will not be active.
plsp.add_debug_mode("info")
plsp.add_debug_mode("detail")
plsp.add_debug_mode("debug")
plsp.add_debug_mode("error", separate=True)



# START OF MODIFYING DEBUG CONTEXTS #

# You may modify the debug contexts after they are created.
# Access the debug context by using the `Logger.debug_contexts` dictionary.

pls.get_debug_context("generic").set_can_ever_write(True)
plsp.get_debug_context("generic").add_direction(IODirection(False, sys.stdout.fileno(), None))
plsp.get_debug_context("rendering").set_can_ever_write(True)
plsp.get_debug_context("rendering").add_direction(IODirection(False, sys.stdout.fileno(), None))
plsp.get_debug_context("physics").set_can_ever_write(True)
plsp.get_debug_context("physics").add_direction(IODirection(False, sys.stdout.fileno(), None))
					       
# The below will add the time before each log message.
#plsp.get_debug_context("generic").add_format_layer(TimeFormatter)
#plsp.get_debug_context("rendering").add_format_layer(TimeFormatter)
#plsp.get_debug_context("physics").add_format_layer(TimeFormatter)
#
## The below will add which ever function called the log message.
#plsp.get_debug_context("generic").add_format_layer(CallerFormatter)
#plsp.get_debug_context("rendering").add_format_layer(CallerFormatter)
#plsp.get_debug_context("physics").add_format_layer(CallerFormatter)
#

# END OF MODIFYING DEBUG CONTEXTS #



# Now we can use the debug contexts to log messages.
plsp.set_debug_mode("info")

plsp().info("This is using the generic context.")
plsp().info("It works since we set a global context.")



class renderer:
	def __init__(self):
		plsp().rendering.detail("The rendering engine in this engine is pretty simple!")



class physics:
	def __init__(self):
		plsp().physics.detail("The physics engine in this engine is pretty simple!")


#my_renderer = renderer()
my_physics = physics()

plsp.set_debug_mode("detail")

my_physics = physics()







from plsp.infoinject import InfoInjector

@InfoInjector.add_instruction(line=1, debug_mode="info", debug_context="generic", args_for_logger=(
	f"n = {InfoInjector.VariableReference('n')}",
))
@InfoInjector.add_instruction(line=2, debug_mode="detail", debug_context="generic", args_for_logger=(
	f"n is", "less than or equal to 1"
),
	end="\n.\n"
)
@InfoInjector.add_instruction(line=4, debug_mode="info", debug_context="generic", args_for_logger=(
	f"n is greater than 1",
	f"Now actually calculating... n-1 and n-2"
))
@InfoInjector.inject(globals(), locals())
def fib(n):
	if n <= 1:
		return n
	else:
		return fib(n-1) + fib(n-2)

fib(5)
```