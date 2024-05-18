class MathOperations:
    def __init__(self, num1, num2) -> None:
        self.num1 = num1
        self.num2 = num2

    def add(self):
        return self.num1 + self.num2
    
    def sub(self):
        return self.num1 - self.num2
    
    def mult(self):
        return self.num1 * self.num2
    
    def div(self):
        if self.num2 == 0:
            raise Exception('Sorry, I Cannot divide by 0')
        else:
            return self.num1 / self.num2
        
    def mod(self):
        return self.num1 % self.num2
    
    def pow(self):
        return self.num1 ^ self.num2