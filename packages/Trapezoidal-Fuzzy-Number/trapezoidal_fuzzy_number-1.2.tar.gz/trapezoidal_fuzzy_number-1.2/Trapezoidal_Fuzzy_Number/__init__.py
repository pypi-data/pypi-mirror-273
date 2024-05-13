class TrapezoidalFuzzyNumber:
    def __init__(self, l):
        self.a = l[0]
        self.b = l[1]
        self.c = l[2]
        self.d = l[3]

    def __repr__(self):
        return f"TrapezoidalFuzzyNumber({self.a}, {self.b}, {self.c}, {self.d})"

    def __add__(self, other):
        # Addition of two trapezoidal fuzzy numbers
        return [self.a + other.a, self.b + other.b, self.c + other.c, self.d + other.d]

    def __sub__(self, other):
        # Subtraction of two trapezoidal fuzzy numbers
        return [self.a - other.d, self.b - other.c, self.c - other.b, self.d - other.a]

    def __mul__(self, other):
        # Multiplication of two trapezoidal fuzzy numbers
        return [self.a * other.a, self.b * other.b, self.c * other.c, self.d * other.d]

    def __rmul__(self, scalar):
        # Multiplication of a real number and a trapezoidal fuzzy number
        return [scalar * self.a, scalar * self.b, scalar * self.c, scalar * self.d]

    def __truediv__(self, other):
        # Division of two trapezoidal fuzzy numbers
        return [self.a / other.d, self.b / other.c, self.c / other.b, self.d / other.a]

    def __rtruediv__(self, scalar):
        # Division of a real number and a fuzzy number
        return [scalar / self.d, scalar / self.c, scalar / self.b, scalar / self.a]

    def __floordiv__(self, scalar):
        # Division of a trapezoidal fuzzy number and a real number
        return [self.a // scalar, self.b // scalar, self.c // scalar, self.d // scalar]