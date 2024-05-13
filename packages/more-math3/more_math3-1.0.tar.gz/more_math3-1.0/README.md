<h1>More Math Python Library</h1>

<h2>An Introduction</h2>

Welcome to the More Math Python library!

In this library, you will have many functions that are not in the built-in "math"
module.

<h2>A Brief Summary of this Module</h2>

<h3>Basic Functions</h3>

Here are some basic functions:

<code>is_prime(number: int) -> bool</code> and <code>is_composite(number: int) -> bool</code> check the primality of a number.

<code>is_square(number: int) -> bool</code> checks whether a number is a square or not.

<code>is_cube(number: int) -> bool</code> checks whether a number is a cube or not.

All numbers in these functions must be greater than 2.

<h3>HCF and LCM</h3>

<code>hcf(*numbers: int) -> int</code> returns the highest common factor of the numbers.

<code>lcm(*numbers: int) -> int</code> returns the lowest common multiple of the numbers.

<h3>Exponents and Roots</h3>

<code>is_power_of(number: int, x: int) -> bool:</code> which checks whether <code>number</code> is a power of <code>x</code>.

<code>nth_power_of(number: int, x: int) -> int:</code> which checks which power of <code>x</code> is <code>number</code>.

<code>nth_root_of(number: int, x: int) -> int:</code> which checks which root of <code>x</code> is <code>number</code>.

<h3>Combinations</h3>

<code>combinations(number: int, *, keep_length: bool = True, repeat: bool = False) -> list[int]</code> generates a list of all possible combinations
with a set of numbers. <code>keep_length</code> and <code>repeat</code> are optional, but they are keyword-only arguments.
<code>keep_length</code> allows you to keep the length of the specified number, and is by default set to <code>True</code>.
<code>repeat</code> allows repeating digits, and is by default set to <code>False</code>.

<code>nth_combination(number: int, index: int, *, keep_length: bool = True, repeat: bool = False) -> int</code> 
returns the nth combination generated with a set of numbers. <code>index</code> is n here.

<code>min_and_max_combination(number: int, *, keep_length: bool = True, repeat: bool = False) -> tuple[int]</code>
returns the lowest and highest number generated with a set of digits.

<h3>Encoding and Decoding</h3>

<code>encode_number(number: int, base: int) -> int</code> encodes the number into an alphanumeric number of a specific base.

<code>decode_number(number: str, base: int) -> int</code> decodes the number from an alphanumeric number of a specific base to an integer.

<h3>Other Properties of Numbers (returns <code>bool</code>)</h3>

<code>is_triangular(number: int) -> bool</code> returns whether a number is triangular 
(=that is a sum of digits from 1 to a number) or not.

<code>is_pentagonal(number: int) -> bool</code> returns whether a number is pentagonal (=that is n(3n+1) / 2) or not.

<code>is_hexagonal(number: int) -> bool</code> returns whether a number is hexagonal (=that is n(2n+1)) or not.

<code>is_strong(number: int) -> bool</code> returns whether the sum of factorials of the digits of a number add up to the number.

<code>is_armstrong(number: int) -> bool</code> returns whether the sum of cubes of the digits of the number add up to the number.

<code>is_mersenne_prime(number: int) -> bool</code> returns whether a number is a Mersenne prime or not.
A Mersenne prime is a prime number which is 1 plus a power of 2.

<h3>Exceptions</h3>

Exceptions are raised in many of the functions when you enter a number that is less than 1.
They are also raised in <code>nth_power_of(number: int, x: int) -> bool</code> when you enter
<code>number</code> when it is not a power of <code>x</code>.

<h3>How to Install the Module</h3>

1. Open your terminal or command line
2. Run <code>pip install more_math_3</code>.
3. Add it to your PATH.


Thank you! I hope you like my module.
Reach out to me here: unknownuser170911@gmail.com
Enjoy using the module!