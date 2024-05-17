"""
Enables beartype for the entire package.

This module enables beartype for all modules within this package, enforcing
static type checking and improving code reliability.

The `beartype_this_package` function from the `beartype.claw` module is imported
and called to achieve this behavior. This function automatically applies type
annotations and verification throughout the package.
"""

from beartype.claw import beartype_this_package
beartype_this_package()
