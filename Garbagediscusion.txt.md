Generational Garbage Collection is a form of automatic memory management that classifies objects by how long they have been in memory. It's based on the observation that most objects die young, i.e., many of the objects that are allocated are quickly dereferenced and become garbage.

Here's a high-level overview of how it works:

1. Generations: Memory is divided into two or more "generations". New objects are allocated in the youngest generation. When the youngest generation fills up, it triggers a garbage collection.

2. Minor Collection: The garbage collector first performs a "minor collection", which involves the youngest generation. It uses a Mark and Sweep algorithm, but only on the objects in the youngest generation.

3. Promotion: If an object survives a certain number of minor collections, it's assumed to be long-lived and is "promoted" to an older generation. The threshold for promotion can be adjusted for performance.

4. Major Collection: Occasionally, a "major collection" is performed that involves all generations. This is more time-consuming, but it happens less frequently.

The advantage of Generational Garbage Collection is that it can be much faster than a simple Mark and Sweep. Since minor collections involve only a subset of memory (the youngest generation), they can be done quickly. And since most objects die young, this means most garbage can be collected with these quick minor collections.

Python's garbage collector uses a form of Generational Garbage Collection. It has three generations in total, and an object gets promoted to an older generation after surviving a certain number of collections.


---

```python
class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.age = 0

class Variables:
    def __init__(self):
        self.generations = [[], [], []]  # Three generations

    def add_variable(self, name, value):
        var = Variable(name, value)
        self.generations[0].append(var)

    def collect_garbage(self):
        # Minor collection in the youngest generation
        self.generations[0] = [var for var in self.generations[0] if var.value is not None]
        for var in self.generations[0]:
            var.age += 1
            if var.age > 2:  # If a variable has survived 2 collections, promote it
                self.generations[1].append(var)
        self.generations[0] = []

        # Occasionally perform a major collection
        if len(self.generations[1]) > 100:  # If the second generation gets too large
            self.generations[1] = [var for var in self.generations[1] if var.value is not None]
            for var in self.generations[1]:
                var.age += 1
                if var.age > 5:  # If a variable has survived 5 collections in the second generation, promote it
                    self.generations[2].append(var)
            self.generations[1] = []

        if len(self.generations[2]) > 1000:  # If the oldest generation gets too large
            self.generations[2] = [var for var in self.generations[2] if var.value is not None]
```

---

```python
class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.age = 0

class Variables:
    def __init__(self):
        self.generations = [[], [], []]  # Three generations

    def add_variable(self, name, value):
        var = Variable(name, value)
        self.generations[0].append(var)

    def collect_garbage(self):
        # Minor collection in the youngest generation
        self.generations[0] = [var for var in self.generations[0] if var.value is not None]
        for var in self.generations[0]:
            var.age += 1
            if var.age > 2:  # If a variable has survived 2 collections, promote it
                self.generations[1].append(var)
        self.generations[0] = []

        # Occasionally perform a major collection
        if len(self.generations[1]) > 100:  # If the second generation gets too large
            self.generations[1] = [var for var in self.generations[1] if var.value is not None]
            for var in self.generations[1]:
                var.age += 1
                if var.age > 5:  # If a variable has survived 5 collections in the second generation, promote it
                    self.generations[2].append(var)
            self.generations[1] = []

        if len(self.generations[2]) > 1000:  # If the oldest generation gets too large
            self.generations[2] = [var for var in self.generations[2] if var.value is not None]
```