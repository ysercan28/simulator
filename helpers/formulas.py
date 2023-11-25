class Formulas:
    def __init__(self, c, G):
        self.c = c
        self.G = G

    def calc_gravitational_force(self, mass1, mass2):
        """
        Calculate gravitational force between two masses in a 1D space.
        """

        try:
            force = self.G * mass1 * mass2
        except ZeroDivisionError:
            force = 0
        return force

    def a(self, F,m):
        """
        Calculate acceleration from force and mass.
        """
        try:
            a = F/m
        except ZeroDivisionError:
            a = 0
        return a

    def c_limit(self, v):
        """
        Cap velocity to c.
        """
        
        if v < 0: return max(v, -self.c)
        else: return min(v, self.c)