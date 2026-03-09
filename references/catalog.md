# Code Smells Catalog

Author: [Yoan Thirion](https://github.com/ythirion)

Source: [sammancoaching.org](https://www.sammancoaching.org/reference/code_smells/index.html) — CC-BY-SA-4.0
Based on: Martin Fowler, *Refactoring* (2nd edition)

28 smells organized in 4 families.

---

## Family 1 — Readability / Naming

### [Mysterious Name](https://www.sammancoaching.org/code_smells/mysterious_name.html)
> "When a code element like a function, class or variable has a name that is obscure or difficult to understand."

Obscure naming creates friction for every developer reading the code. Invest in names that clearly convey purpose and usage — this pays dividends in comprehension and reduced cognitive load.

**Refactoring:** Rename Function / Rename Variable / Rename Field.

---

### [Comments](https://www.sammancoaching.org/code_smells/comments.html)
> "Sometimes people write comments instead of taking the time to make the actual code readable and self-explanatory."

Comments are not always a smell — explaining *why* code is written a certain way is valuable. The smell appears when comments substitute for clear code. A comment that explains *what* the code does is a sign the code itself should be clearer.

**Secondary signals:** often points to Mysterious Name, Primitive Obsession, or undocumented assumptions that could be expressed as assertions.

**Refactoring:** Rename to eliminate the need for the comment; Extract Function to name the intent; replace assumption comments with assertions.

---

### [Paragraph of Code](https://www.sammancoaching.org/code_smells/paragraph.html)
> "A section of code within a longer function or method that belongs together, does something specific, and might make sense to extract and name as a method."

**Visual indicators:** a comment preceding the block; consistent indentation grouping; a control structure (for, if, try) starting the section; blank lines above and below; repeated variable names within the section.

Unnamed paragraphs are harder to understand than explicitly named methods with clear inputs and outputs.

**Refactoring:** Extract Function — give the paragraph a name and explicit parameters.

---

## Family 2 — Size / Complexity

### [Long Function / Long Method](https://www.sammancoaching.org/code_smells/long_function.html)
> "If the function is too long then it will often be difficult to read and understand."

Modern compilers impose no meaningful performance penalty for extracting code into subroutines. A key warning sign: when a developer adds a comment to explain a block of code, that block should be extracted into a named function instead.

**Refactoring:** Extract Function; decompose into well-named private methods.

---

### [Large Class](https://www.sammancoaching.org/code_smells/large_class.html)
> "When a class is doing too much. It has too many fields and/or too many methods."

Large classes are a prime breeding ground for duplicated code, redundancy, and confusion about the class's purpose. Identify subsets of methods and fields that are used together and extract them into their own focused classes.

**Refactoring:** Extract Class; Extract Subclass; identify groupings of co-used methods and fields.

---

### [Long Parameter List](https://www.sammancoaching.org/code_smells/long_parameter_list.html)
> "If the argument list is long, then your function or method is probably difficult to understand and reason about."

When multiple parameters logically belong together, they signal a missing abstraction. Group them into a dedicated class or object.

**Anti-pattern to avoid:** do not resolve long parameter lists by introducing global variables — this creates worse problems than the original smell.

**Refactoring:** Introduce Parameter Object; Preserve Whole Object; Replace Parameter with Query.

---

### [Deep Nesting](https://www.sammancoaching.org/code_smells/deep_nesting.html)
> "If code has many conditionals and loops nested inside one another, perhaps more than about 3 levels, then you'd say it has 'deep nesting'."

The human brain has a limit to how much complexity it can hold at once. Deeply nested code exceeds that limit by requiring the developer to track all active conditions simultaneously.

**Alternative names:** Heavy Indentation; Snarled Method (Michael Feathers); Arrow Anti-Pattern.

**Note:** when multiple sections within a single method each show deep nesting, the smell is called **Bumpy Road**.

**Refactoring:** Extract Function for each nested section; use guard clauses and early returns to flatten conditionals.

---

### [Bumpy Road](https://www.sammancoaching.org/code_smells/bumpy_road.html)
> "A method or function contains multiple sections, each exhibiting deep nesting."

The irregular indentation pattern — several distinct "bumps" — signals mixed concerns. Each bump typically represents a separate responsibility that should be its own function.

**Origin:** identified by Adam Tornhill (CodeScene).

**Refactoring:** Extract each deeply nested section into its own dedicated function.

---

### [Loops](https://www.sammancoaching.org/code_smells/loop.html)
> "Loops using `for` and `while` and suchlike are a bit outdated these days."

Explicit loops are less expressive than pipeline operations. `map`, `filter`, `reduce` and similar constructs name the operation being performed, making intent clearer and composition easier.

**Refactoring:** Replace Loop with Pipeline; use functional collection operations.

---

### [Variable with Long Scope](https://www.sammancoaching.org/code_smells/variable_with_long_scope.html)
> "Any local variable that is in scope for more than a handful of lines is going to tax your short-term memory, especially if it is updated in several places."

Long-scoped variables also hinder refactoring — even a read-only variable that spans many lines makes function extraction harder. Global variables and mutable singletons are extreme variants of this smell.

**Refactoring:** Extract Function to narrow variable scope; eliminate or encapsulate global/singleton mutable state.

---

## Family 3 — Coupling / Cohesion

### [Feature Envy](https://www.sammancoaching.org/code_smells/feature_envy.html)
> "When a function in one class or module makes extensive use of functions and/or data from another class or module, so much so that it probably belongs there."

In object-oriented design, methods should live with the data they operate on. Feature Envy violates this: the function is more interested in another object's internals than its own.

**Refactoring:** Move Function to the class it envies.

---

### [Insider Trading](https://www.sammancoaching.org/code_smells/insider_trading.html)
> "Classes or modules that know too much about the inside details of one another. They may pass private data between them."

Particularly problematic in inheritance: subclasses accessing protected or private details of parent classes. Internal implementation details leak across boundaries, creating brittle dependencies and violating encapsulation.

**Refactoring:** Move Function / Move Field; Hide Delegate; replace inheritance with composition when subclasses know too much about their parent.

---

### [Message Chains](https://www.sammancoaching.org/code_smells/message_chains.html)
> "When a client asks one object for another object, then for another object, and another object down a chain."

Example: `A.getB().getC().getD().getE()`. Violates the Law of Demeter. Any structural change within the chain propagates outward and can break client code unexpectedly.

**Refactoring:** Hide Delegate; introduce a method on the first object that provides the needed result directly.

---

### [Middle Man](https://www.sammancoaching.org/code_smells/middle_man.html)
> "A class that doesn't do much more than forward all the calls to another class, with little or no behaviour of its own."

The intermediary adds no value. Clients might as well communicate directly with the underlying class.

**Refactoring:** Remove Middle Man; inline delegation into the caller.

---

### [Divergent Change](https://www.sammancoaching.org/code_smells/divergent_change.html)
> "Divergent change occurs when lots of different kinds of changes all affect the same module or class."

Signals a **cohesion problem**: the module bundles responsibilities that should be separated. Ideally, each kind of change touches only one module.

**Distinction:** differs from Shotgun Surgery, which is a *coupling* problem (one change scatters across many modules).

**Refactoring:** Extract Class to separate concerns; Split Phase.

---

### [Shotgun Surgery](https://www.sammancoaching.org/code_smells/shotgun_surgery.html)
> "When you want to change one thing and it ends up you have to make a lot of additional changes before the original thing is working properly."

Signals a **coupling problem**: things that change together are not living together. The risk of missing a required change and introducing a bug is high.

**Distinction:** differs from Divergent Change, which is a *cohesion* problem (many reasons to change one module).

**Refactoring:** Move Function / Move Field to consolidate related behavior; Inline Class to merge overly-split classes.

---

### [Alternative Classes with Different Interfaces](https://www.sammancoaching.org/code_smells/alternative_classes_different_interfaces.html)
> "When you have two or more classes that should theoretically be interchangeable with one another, but their actual interfaces differ in practice."

Prevents true substitutability, violates the Liskov Substitution Principle, and complicates client code that needs to work with either class.

**Refactoring:** Rename Function; Move Function; Extract Superclass to create a common interface.

---

## Family 4 — Data Structures / Modeling

### [Data Class](https://www.sammancoaching.org/code_smells/data_class.html)
> "The class has fields, i.e. mutable state, but no other behaviour. There may be get and set methods for the fields, or they may be public."

A data class functions as a passive container. Functions that operate on this data exist elsewhere, leading to Feature Envy in other classes.

**Refactoring:** Move related functions into the class; Encapsulate Record; remove unnecessary setters.

---

### [Data Clumps](https://www.sammancoaching.org/code_smells/data_clumps.html)
> "When the same group of fields or parameters or classes often crop up together."

**Diagnostic test:** remove one element from the group — if the remaining elements still make sense together without it, they do not form a clump. If they feel incomplete, the group should be a class.

**Refactoring:** Extract Class to bundle the clump; Introduce Parameter Object.

---

### [Primitive Obsession](https://www.sammancoaching.org/code_smells/primitive_obsession.html)
> "When you use plain built-in primitive types like string, int, float etc. It can be a sign you should have classes to represent domain concepts."

Using primitives for domain concepts loses type safety and the ability to enforce business rules. Classic risks: unit confusion (inches vs centimetres), format inconsistency (phone numbers), missing validation.

**Refactoring:** Replace Primitive with Object; create domain classes (`Money`, `PhoneNumber`, `Coordinates`) that encapsulate validation and formatting.

---

### [Global Data](https://www.sammancoaching.org/code_smells/global_data.html)
> "Data that can be modified from anywhere in the codebase."

Difficult to reason about and nearly impossible to test reliably. Singletons and class-level mutable variables are variants. Immutable global data (constants) is far less problematic.

**Refactoring:** Encapsulate Variable; pass data explicitly; convert mutable singletons to injected dependencies.

---

### [Mutable Data](https://www.sammancoaching.org/code_smells/mutable_data.html)
> "Data is changed during runtime, and other parts of the program keep a reference to it."

When a data structure is modified in place, all code holding a reference to it is silently affected. Particularly dangerous in multithreaded contexts. Prefer returning a new copy of the data with changes applied (immutable style).

**Refactoring:** Encapsulate Variable; Replace Derived Variable with Query; use immutable data structures.

---

### [Temporary Field](https://www.sammancoaching.org/code_smells/temporary_field.html)
> "A class has a field which is only set in particular circumstances. At other times it may be empty or null."

The class carries data that isn't consistently populated, signalling a cohesion violation — the class is handling multiple distinct responsibilities.

**Refactoring:** Extract Class for the temporary field and its associated methods; move related behaviour alongside the data.

---

### [Refused Bequest](https://www.sammancoaching.org/code_smells/refused_bequest.html)
> "When a subclass inherits methods and fields from their parents, but doesn't need them."

Signals that the inheritance hierarchy is not properly structured. The subclass cannot reliably substitute for its parent (Liskov Substitution Principle violation).

**Refactoring:** Replace Subclass with Delegate; Push Down Method / Push Down Field; reconsider whether inheritance is the right relationship.

---

### [Speculative Generality](https://www.sammancoaching.org/code_smells/speculative_generality.html)
> "Extra code and hooks and special cases to handle things that aren't (yet) required."

Code written for hypothetical future needs that never materialised. Detection: the code is only called from tests, or IDE analysis flags it as unused.

**Refactoring:** Remove dead code (YAGNI — You Aren't Gonna Need It); version control makes it recoverable if the need ever arises.

---

### [Duplicated Code](https://www.sammancoaching.org/code_smells/duplicated_code.html)
> "When you have the same code in more than one place, perhaps with small variations."

When identical or nearly identical code exists in multiple locations, every change must be applied everywhere. Missing one copy introduces inconsistency. Related to Shotgun Surgery.

**Refactoring:** Extract Function; Pull Up Method; Form Template Method.

---

### [Repeated Switches](https://www.sammancoaching.org/code_smells/repeated_switches.html)
> "If you see the same `switch` statement in several places, it's a sign that you could be using a more flexible and dynamic structure like polymorphism."

A single switch may be acceptable. Multiple instances of the same switch scattered across a codebase signal that adding a new case requires synchronising every occurrence — a maintenance risk.

**Refactoring:** Replace Conditional with Polymorphism; use strategy objects or subclasses.

---

### [Lazy Element](https://www.sammancoaching.org/code_smells/lazy_element.html)
> "Unneeded structure that could easily be inlined without losing anything important."

Common manifestations: a function whose name merely restates what its body does; a wrapper class with no added abstraction; indirection that obscures rather than clarifies.

**Common origins:** post-refactoring remnants; consequences of Speculative Generality.

**Refactoring:** Inline Function; Inline Class; collapse the unnecessary layer.
