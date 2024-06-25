from sympy import N

class Interval:
    def __init__(self,min, max):
        self.min = min
        self.max = max

    def __str__(self):
        return f"[{self.min}... {self.max}]"
    
    def in_range(self, number: float) -> bool:
        return N(number) >= self.min and N(number) <= self.max and number.is_real
