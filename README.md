# LOGIC
A programming language based on physical logic gates. Values can only be binary numbers, which can also be assigned to variables.

### Grammer

The grammer of LOGIC follows a simple path, most lines are written as instruction executions. Executing an instruction is done by specifying the instruction to run, followed by the maximum bit length of the return value, followed by the return variable and and lastly followed by the required arguments ended by a terminator.

### Syntax
**Instruction execution syntax:**

`` <i>[@l] [r] [a0 a1 a2 ... ]; ``
* *i*, the identifier for the instruction to use.
* *l*, the "bit cap", or the maximum bit length for the return value. If this is exceeded an Overflow exception is raised.
* *r*, the identifier of the variable of which to store the return value.
* *a*, the zero or more required arguments, that can be either a binary constant or a variable.

**Instruction execution example:**

`` AND@8 C 1001 A; ``

This line of code will execute the instruction ``AND`` parsing the binary constant of ``1001`` and the variable ``A``, there after storing the return value in the variable ``C``, raising an Overflow exception if the return variable's bit length is greater than 8, as told by the bit cap ``@8``.
A bit cap on every instruction execution is not required if, and only if one have already been set. This can be done by typing the following on a newline: ``@8;``, every return value after this point will be capped at a bit length of 8.
