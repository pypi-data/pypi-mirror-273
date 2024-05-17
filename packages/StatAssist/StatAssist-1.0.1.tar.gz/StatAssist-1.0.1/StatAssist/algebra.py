import math


class ALGEBRAIC_EQS:
    @staticmethod
    def polynomial(x: float, coefficients: list) -> float:
        """
        Returns an evaluation of a polynomial.
        :param x: float
        :param coefficients: list, by increasing degree.
        :return: float
        """
        P = 0
        degree = len(coefficients)
        for i in range(degree):
            P += coefficients[i] * pow(x, i)

        return P

    @staticmethod
    def exponential_equation_1(x: float, Args: list = [1, 0]) -> float:
        """
        Returns an evaluation of a basic exponential equation with base e.
        :param x: float, exponent of e.
        :param Args: list, [coefficient of e, constant]; Default: [1, 0].
        :return: float
        """
        A = Args[0]
        C = Args[1]
        return A * math.exp(x) + C

    @staticmethod
    def exponential_equation_2(x: float, Args: list = [1, 2, 0]) -> float:
        """
        Returns an evaluation of a basic general exponential equation.
        :param x: float, exponent of base.
        :param Args: list, [coefficient of base, base, constant]; Default: [1, 2, 0].
        :return: float
        """
        A = Args[0]
        B = Args[1]
        C = Args[2]
        return A * pow(B, x) + C

    @staticmethod
    def log_equation(x: float, Args: list = [1, 0, 10]) -> float:
        """
        Returns an evaluation of a basic logarithmic equation.
        :param x: float
        :param Args: list, [coefficient of log_n(x), constant, base]; Default: [1, 0, 10].
        :return: float
        """
        A = Args[0]
        C = Args[1]
        base = Args[2]

        return A * math.log(x, base) + C


funcs_ = ALGEBRAIC_EQS()
