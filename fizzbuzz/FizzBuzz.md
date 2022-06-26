# A Dozen Ways to do FizzBuzz

## First Things First

### What is FizzBuzz Anyway?
FizzBuzz is a programming problem with a simple premise:
> Print the numbers from 1 to 100. If a number is a multiple of 3, replace it with "Fizz". If it's a multiple of 5, replace it with "Buzz". If it's a multiple of both 3 and 5, replace it with "FizzBuzz".

Straightforward enough. Let's figure out how we want to go about this.

### Separating Concerns
To start, let's break the problem down into some big, coarse, pieces, so we can start writing code with some sort of structure in mind. Looking at the description, let's say these are the big parts:
 - Generate a list of numbers between 1 and 100
 - Figure out whether each of those numbers should be 'Fizz', 'Buzz', or 'FizzBuzz'
 - Print out the appropriate output
Of those parts, all the juicy interesting stuff is in the second one. Let's start off by separating the actual Fizzing and Buzzing components from the boring stuff like generating a list of numbers and printing stuff out. This will lead us to a solution that uses two functions: a fizzbuzz function, which takes a single integer and determines the correct output for that number, and a simple driver function that feeds a bunch of numbers to fizzbuzz and prints the output. That will end up looking something like this:
```python
def fizzbuzz_driver(limit: int = 100):
   for num in range(1, limit + 1):
      print(fizzbuzz_function(num))
```
There are other ways to break this down (some of which we'll talk about later on), but this is certainly good enough to start.

## Let's write some code

### If
Now that we have a plan, we have to actually figure out how to do this. 

Python evaluates if statements from top to bottom, and will execute the first condition that is met, so we need to put the most specific case first. For us, this is the '15' case. If we put the 3 or 5 case first, 

```python
def fizzbuzz_if(n: int) -> str:
   if n % 15 == 0:
      return "FizzBuzz"
   elif n % 3 == 0:
      return "Fizz"
   elif n % 5 == 0:
      return "Buzz"
   else:
      return str(n)
```



### If, with flag variables


As you can see below, this leaves us with some *exceptionally* readable if statements. 

```python
def fizzbuzz_if_with_flags(n: int) -> str:
   should_fizz = n % 3 == 0
   should_buzz = n % 5 == 0
   if should_fizz and should_buzz:
      return "FizzBuzz"
   elif should_fizz:
      return "Fizz"
   elif should_buzz:
      return "Buzz"
   else:
      return str(n)
```


### If, with support functions
 - if with support functions

```python
def fizzbuzz_with_flags(n: int) -> str:
   should_fizz = _is_fizzable(n)
   should_buzz = _is_buzzable(n)
   if should_fizz and should_buzz:
      return "FizzBuzz"
   elif should_fizz:
      return "Fizz"
   elif should_buzz:
      return "Buzz"
   else:
      return str(n)
```

Extracting the divisibility logic to dedicated functions gives us a little more room to breathe. For instance, we could write functions like these, which use divisibility rules instead of the modulo operator. Implementing FizzBuzz without using modulo at all is not really a design requirement here. I'm just using it to illustrate that 


```python
def _is_fizzable(n: int) -> bool:
   while len(str(n)) > 1:
        n = sum(int(c) for c in str(n))
    return n in {3, 6, 9}


def _is_buzzable(n: int) -> bool:
   return str(n)[-1] in {"0", "5"}
```


### SPM

What if we wanted to use Python's new Structural Pattern Matching, introduced in 3.10? That seems like a natural fit for a situation like this one, where we've got a set number of possibilities, only one of which can be true. 
 - brute force

```python
def fizzbuzz_SPM_blunt(n: int) -> str:
   match n:
      case _ if n % 15 == 0:
         return "FizzBuzz"
      case _ if n % 3 == 0:
         return "Fizz"
      case _ if n % 5 == 0:
         return "Buzz"
      case _:
         return str(n)
```
Well, it works, and we are indeed using structural pattern matching, but that's about all the nice things there are to say about this approach. It mimics exactly our original 'if' approach, only we've bolted on a whole new syntax to no meaningful effect. 

#### Using Modular Arithmetic
What if we really lean into this whole modulo thing? 

We can use this to construct a more reasonable pattern matching approach to FizzBuzz:

```python
def fizzbuzz_SPM_mod(n: int) -> str:
   match n % 15:
      case 0:
         return "FizzBuzz"
      case 3 | 6 | 9 | 12:
         return "Fizz"
      case 5 | 10:
         return "Buzz"
      case _:
         return str(n)
```
These are the same 4 conditions we've been dealing with the whole time, but we're looking at them from a different angle here. We start by getting the value of n modulo 15which we then use to drive our analysis. Since 15 is a multiple of 3, if n modulo 15 yields a number that is also a multiple of 3, it means n is a multiple of 3 away from a known multiple of 3, which means n must also be a multiple of three. The same goes for 5 and multiples of 5. Since there aren't a ton of multiples of either number between 0 and 14, it's manageable to write out all the possibilities. So here's what this match statement is actually doing:

 - Take the value of n modulo 15
 - If that value is 0, n is a multiple of 15, which means we return "FizzBuzz"
 - If that value is either 3, 6, 9, or 12, n is a multiple of 3, which means we return "Fizz"
 - If that value is either 5 or 10, n is a multiple of 5, which means we return "Buzz"
 - Otherwise, return n as a string

> As an aside, this kind of modular arithmetic reasoning can be used in some pretty interesting ways. For instance, it lets you prove that all prime numbers greater than 3 are either one less or one more than some multiple of 6, which, to me, is not otherwise intuitive.


#### Pattern Matching Using a Tuple
If, instead of using a single mod operation, we do 

 - mod tuple

```python
def fizzbuzz_SPM_tuple(n: int) -> str:
   match (n % 3, n % 5):
      case (0, 0):
         return "FizzBuzz"
      case (0, _):
         return "Fizz"
      case (_, 0):
         return "Buzz"
      case _:
         return str(n)
```


## How are we doing so far?
These approaches all work. That's good, but is it enough? Let's imagine that the product requirements change. Let's say our second number is 4 instead of 5, and it's "Bizz" now instead of "Fizz". What do we have to do to bring our code in line with the new spec?
 - We have to change all the 5s to 4s
 - Since we were using 15 as a shorthand for '3 and 5', we need to go find all of our 15s and change them to 12s
 - We have to pay particular attention to our modular arithmetic driven match statement, since changing our modulus changes the set of values we care about
 - We have to change all instances of "Fizz" to "Bizz".
 - If we're being diligent (we are, of course, being diligent) we should also change references to Fizz in our functions and variable names to Bizz instead. It's BizzBuzz now.

None of this is *hard* per se, but each of these changes manifest in our code in multiple places, and it's easy to miss a spot. We would be in better shape for refactors like this if our code weren't so hardwired to the specific values in the initial description. For instance, our "if with flags" approaches don't require as much care, since they treat the 'FizzBuzz' case as 'divisible by 3 and divisible by 5' rather than 'divisible by 15,' and that goes for the "structural pattern matching with tuple" approach too.

What if the product requirements change in a different way? What if instead of FizzBuzz, it's FizzBuzzBazz, and 3, 5 and 7 instead of just 3 and 5? Now we've got a bigger problem. Adding a factor means we no longer have 4 conditions to worry about, we have 8. Each number can be divisible by:
 - 3, 5, and 7
 - 3 and 5
 - 5 and 7
 - 3 and 7
 - Just 3
 - Just 5
 - Just 7
 - Neither 3, 5, nor 7

Going from 2 factors to 3 doubled the number of conditions we need to keep track of. In fact, the number of conditions will double every time a new factor is added. By the time we get to FizzBuzzFuzzBazzFazz we've got 32 conditions to deal with. Wrangling 4 conditions by hand is manageable enough. 8 is pushing it. 16? 32?? No thanks. 

## Now what?
These refactors have shown us that the approaches we've tried so far are brittle. When you push on them they don't bend, they break. If we want to write this in a way that is readable, extensible, and maintainable, let's start by identifying some dream characteristics of an ideal FizzBuzz function built to withstand change. 

FizzBuzz Vision Board:
 - Automatic handling of different combinations of however many factors we may end up with
 - As few explicit descriptions of our factors and fizzbuzz text as we can get away with, to keep refactors short and sweet

Are these achievable goals? Let's take a step back and see if we can come up with a more generalized version of the problem description, one that doesn't mention any specific numbers or Fizzes or Buzzes, so we aren't tempted to tie ourselves down prematurely.

> Given a list of factors, each with some associated text, print the numbers from 1 to 100, replacing each number with a combination of the text associated with all of the given factors that evenly divide that number.

Certainly more general. What can we do with this?

Well, the fact that there is text *associated with* each factor is interesting. Python has a built in dictionary type that is designed to store values with this kind of associative relationship. What could we do with something like this?

```python
factor_dict = {
   3: "Fizz",
   5: "Buzz",
}
```

We should be able to write something that looks at every factor in this dictionary and adds text to some output value depending on whether a given number is divisible by that factor. 

```python
output = ""
for factor, text in factor_dict.items():
   if n % factor == 0:
      output += text
```

But what if we get through all the factors and none of them divide the number? Now that we're using a loop instead of an `if` statement, we don't get to use a final `else` to catch the stragglers. But what actually happens in our code if a number isn't divisible by any of our factors? That `output` value will never have anything added to it. We'll get through our whole dict, and it will still be an empty string. If we add an if statement after the loop that checks to see whether or not `output` has a value, we'll be able to catch numbers that aren't divisible by any of our factors. We can make use of the fact that empty strings in Python evaluate to `False`, and add a line like this:

```python
if not output:
   output = str(n)
```

This way our `output` value will be whatever combination of Fizz and Buzz or whatever is appropriate, or it will just be the number itself. Bringing it all together, this gives us:

```python
def fizzbuzz_constructed(n: int) -> str:
   factor_dict = {
      3: "Fizz",
      5: "Buzz",
   }
   output = ""
   for factor, text in factor_dict.items():
      if n % factor == 0:
         output += text
   if not output:
      output = str(n)
   return output
```
How about that? We've done FizzBuzz, but we only mention any factors or text in one dictionary, right at the top of the function. If we need to change one of them, we know right away where to look. If we need to add a factor, we just add it to the dictionary. So long as we make sure the factors are listed in the right order, the rest will take care of itself. What's the least common multiple of all our factors? Who cares? We don't need to worry about that.

What can we improve from here? Personally, I'm happy with this functionality. This is how I'd *want* FizzBuzz to work. It meets the spec, and it makes our lives easy as programmers trying to maintain code. There are a couple things we can do to make this more concise, though. If we replaced the for loop with a comprehension, and added a conditional expression, we could get the meat of this function down to one line:

```python
def fizzbuzz_constructed_concise(n: int) -> str:
   factor_dict = {
      3: "Fizz",
      5: "Buzz",
   }
   return "".join(text for factor, text in factor_dict.items() if n % factor == 0) or str(n)
```

Whether this is better than the last version is not a cut and dry question. It's certainly shorter, and fewer lines of code is generally a good thing. On the other hand, it compresses an awful lot of meaning into a single line, which makes it harder to understand that line's intent. This line isn't exactly inscrutable, especially if you're comfortable with comprehensions in Python, but we are definitely making a trade between compactness and expressiveness here. You'll have to decide for yourself what your appetite is for this sort of thing.


## What if broke the problem down differently?

So we've gotten FizzBuzz down to a dictionary and a single line of code, and we can modify it easily if our requirements change on us. That's pretty cool. Where can we go from here? What if we try to approach it from a different angle entirely? There's an argument to be made, for instance, that dealing with FizzBuzz one number at a time is not essential to the solution. Indeed, the problem statement says "print the numbers 1 to 100," and not something like "determine the correct output for *x*." What happens if instead of isolating the core of our solution from the sequential aspect of the problem, we embraced it?

## FizzBuzz as a sequence


If we apply some light mathematical reasoning, it's not too hard to conclude that there is an inherent pattern embedded in fizzbuzz, since our behavior is controlled by the divisibility of numbers. and every third number  fixed pattern in the output of FizzBuzz, as a consequence of the fixed pattern in numbers that are divisible by 3 or 5. Essentially, we're changing our thinking from 'numbers divisible by 3' to 'every 3rd number'. There will be a certain pattern of Fizzes Buzzes and plain numbers up to 15, where there's a FizzBuzz, and then the pattern starts again from the beginning. What can we do with this?

Python's `itertools` module, part of the standard library, has some tools we can import to help us take advantage of this pattern. Specifically, the `cycle` class, which lets us loop through a collection of items indefinitely, would allow us to put this pattern to use.
Since we're starting a whole new approach, let's not worry about being clever for now. Let's just write out that cycle of 15 values, using empty strings to stand in for plain numbers, and see if we can do something with it.

```python
from itertools import cycle

fizzbuzz_pattern = [
   "",
   "",
   "Fizz",
   "",
   "Buzz",
   "Fizz",
   "",
   "",
   "Fizz",
   "Buzz",
   "",
   "Fizz",
   "",
   "",
   "FizzBuzz",
]

fizzbuzz_cycle = cycle(fizzbuzz_pattern)
```

Alright, now we've got an object that will let us cycle through fizzes and buzzes in the correct sequence, but we haven't addressed our plain numbers yet. Also, now that we're trying to generate our output in bulk, rather than on number at a time, our old driver code is no longer useful. We've also got a more daunting problem. We can't just loop through this cycle like we could through a normal range or list. The cycle is infinite. The loop would never end. We've got to come up with a way to figure out when we're done, and stop.

### How about `enumerate()`?
Python's `enumerate()` function will 
If we introduce a `limit` variable and use enumerate to keep track of how many numbers we've processed, we should be able to break out of the otherwise infinite loop once we've done the first 100 numbers. An important detail here is that `enumerate()` by default will start at 0 while our output should start at 1, so we have to make sure to tell it to start at 1 instead.

```python
output = []
for i, fb in enumerate(fb_cycle, 1):
   if i > limit:
      break
   output.append(fb or str(i))
return output
```

Hmm. This works, but it feels a little inelegant. In Python, `for` loops are generally expected to execute once per item in the collection of items being looped over. This setup, where we terminate the loop after a certain number of items have been processed, is a little counterintuitive. It may not be easy for people to quickly figure out when this loop stops, or why it's set up this way. What can we do differently?

### `zip()` to the rescue
Python's built in `zip()` function can help us out of this jam. `zip()` takes two or more collections of items, and generates a new collection of tuples where the first tuple holds the first item in all the collections, the second tuple holds all the second items, etc. For example, if we had two lists, `['a', 'b', 'c']` and `[1, 2, 3]`, and we passed these lists to `zip()`, we'd get `[('a', 1), ('b', 2), ('c', 3)]`. It's like a zipper, running through our lists and joining elements together into one unit. Crucially, `zip()` will keep bundling up the items in our lists until it reaches the end of the shortest list. If we gave it `[1, 2, 3, 4, 5]` instead, we'd get the same output of 3 tuples, since our list of letters only contains 3 items. `zip()` is so named because it is like a zipper, running through our lists and joining elements together into one unit. The zipper analogy helps to make this intuitive, too. If the right side of your jacket's zipper went all the way up, but the left side only went halfway, you'd only be able to zip your jacket halfway. Once the zipper hits the end of the shortest track, that's it.

Now that we've gotten acquainted with `zip()` how do we actually put it to use? We've got `fb_cycle`, which is infinite, and we need a convenient, clearly understandable way to stop once we've processed 100 numbers. If we take our cycle, and feed it to `zip()` along with a nice, finite, list of numbers up to our maximum value, it will produce a collection of tuples that's only as long as we need it to be, which we can then iterate through with a normal `for` loop.

```python
output = []
for fb, num in zip(fb_cycle, range(1, limit + 1)):
   output.append(fb or str(num))
```

Granted, there's some additional conceptual overhead here, since you need to be familiar with `zip()` to understand how this code works, but in exchange for that we get fewer lines of more conventional code. This leaves us with a function like this:

```python
from itertools import cycle

def fizzbuzz_cycle(limit: int) -> list:
   fb_pattern = [
      "",
      "",
      "Fizz",
      "",
      "Buzz",
      "Fizz",
      "",
      "",
      "Fizz",
      "Buzz",
      "",
      "Fizz",
      "",
      "",
      "FizzBuzz",
   ]
   fb_cycle = cycle(fizzbuzz_pattern)

   output = []
   for fb, num in zip(fb_cycle, range(1, limit + 1)):
      output.append(fb or str(num))
   return output
```

Now that we've got a working proof of concept for writing FizzBuzz using a `cycle`, we've got plenty of improvements to make.

## Cycles upon Cycles
From our previous efforts, we know that big, explicit descriptions of FizzBuzz conditions lead to brittle code, and this cycle is about as big and explicit as they come. If something changes, we have to undertake the extremely fussy operation of editing the list of strings by hand, making sure we're changing the right one to the right thing, and not making any typos. We can definitely improve on this.

For starters, what if we thought of this not as a pattern of 15 elements, but two overlapping patterns, one of 3 elements and one of 5. If we make cycles of these smaller patterns, We can use our new friend `zip()` to merge them together. Here's what that would look like:

```python
from itertools import cycle

def fizzbuzz_subcycles(limit: int) -> list:
   pattern_3 = cycle(["", "", "Fizz"])
   pattern_5 = cycle(["", "", "", "", "Buzz"])
   combined_pattern = (fizz + buzz for fizz, buzz in zip(pattern_3, pattern_5))
   output = []
   for fb, num in zip(combined_pattern, range(1, limit + 1)):
      output.append(fb or str(num))
   return output
```
There's some additional and subtle conceptual overhead here. When we create `combined_pattern`, it's critical that we use what's called a 'generator expression' rather than a normal comprehension. When Python sees a list comprehension, it tries to construct the entire list before moving on. Since our cycles are infinite, such a comprehension will never complete. Generator expressions, on the other hand, are only evaluated one element at a time, and only when that element is accessed somewhere else in the code. Essentially, we're not telling Python what's *in* the collection `combined_pattern`, we're telling it *how to figure out what's next* in the collection once it needs to. Generator expressions are created just like comprehensions, but they are wrapped in parentheses rather than brackets or curly braces. It's a pretty slight different in syntax for something that behaves so differently under the hood, but in many cases, comprehensions and generator expressions are effectively interchangeable. Indeed, I've used a few generator expressions in the FizzBuzz implementations we've looked at so far, and they could all be swapped out for comprehensions without issue. Here, though, now that we're using collections that extent infinitely, it's make or break.

With that subtlety out of the way, this function is pretty similar to what we had before. The difference is, now that we're using two smaller cycles, we're taking the next item in each cycle, concatenating them together, and using that to determine what the output should be.
This is definitely an improvement. It's way more compact, and it's much less brittle. We're in *better* shape for refactors, but we're still manually defining the fact that there are exactly 2 cycles, and what those cycles contain. What can we do to get back to the condition we had before, where that would be taken care of automatically?

## Constructing Cycles
If we take a look at the patterns we wrote out in the last example, we can see that they follow a definite formula. The 3 pattern has 3 elements, the last of which is the text associated with 3, and the same formula applies to the 5 pattern. If we reintroduce the dictionary of factors and text we used before, we can write a helper function that takes a factor and its text and returns a properly constructed pattern.

```python
def _construct_pattern(factor: int, text: str) -> tuple:
   pattern = [""] * factor
   pattern[-1] = text
   return tuple(pattern)
```

We can 

 - bring back the dict
 - a cycle making helper

## Infinite FizzBuzz
 - Generators
 - Slicing a Generator