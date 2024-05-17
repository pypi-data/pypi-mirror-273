import random
import math
from sklearn.mixture import GaussianMixture
import torch
import torch.nn as nn


class STATS:
    @staticmethod
    def get_mean(*Data: list) -> list:
        """
        Returns the mean for multiple sets of data
        :param Data: list, contains a list of datasets.
        :return: list, Measure of the average of a dataset.
        """
        means = []
        for dataset in Data:
            temp = 0
            n = len(dataset)
            for datapoint in dataset:
                temp += datapoint / n

            means.append(temp)
        return means

    @staticmethod
    def get_variance(datasets: list, means: list) -> list:
        """
        Returns the variance for multiple datasets.
        :param datasets: list, contains a list of datasets.
        :param means: list, means for each dataset.
        :return: list, Measure of the 'spread' of a dataset.
        """
        variances = []

        if len(datasets) == len(means):
            for i in range(len(means)):
                n = len(datasets[i])
                temp = 0

                for j in range(n):
                    temp += pow(datasets[i][j] - means[i], 2) / n

                variances.append(temp)

            return variances

        return ["len(datasets) != len(means)"]

    @staticmethod
    def get_covariance(datasets: list, means: list) -> float:
        """
        Obtains the covariance for two datasets, x and y.
        :param datasets: list, [dataset 'x', dataset 'x'].
        :param means: list, ['x' mean, 'y' mean].
        :return: float, covariance for datasets x and y.
        """
        covariance = 0
        mu_x = means[0]
        mu_y = means[1]
        x = datasets[0]
        y = datasets[1]
        n = len(datasets[0])

        for i in range(n):
            covariance += (x[i] - mu_x) * (y[i] - mu_y) / n

        return covariance

    @staticmethod
    def get_correlation_coefficient(covariance_xy: float, variance_x: float, variance_y: float) -> float:
        """
        Returns the correlation coefficient for dataset x and y.
        :param covariance_xy: float.
        :param variance_x: float.
        :param variance_y: float.
        :return: flaot, measure of correlation between datasets x and y.
        """
        return covariance_xy / math.sqrt(variance_x * variance_y)

    @staticmethod
    def calculate_confidence(data: list, mean: float, variance: float, z: float = 1.96) -> list:
        """
        Calculates the 95% confidence interval for the population.
        :param data: list, the number of datapoints.
        :param mean: float, the average of the data
        :param variance: float, measure of how 'spread-apart' the data is.
        :param z: Z-score associated with the desired confidence level; Default: 1.96 (95%)
        :return: list, Upper bound and lower bound for desired confidence level.
        """
        pop_size = len(data)
        A = z * math.sqrt(variance / pop_size)

        return [mean - A, mean + A]

    @staticmethod
    def get_linreg_slope(*Args: float) -> float:
        """
        Calculates the slope for a linear regression.
        :param Args: (3) -> correlation coefficient, variance_x, variance_y; (2) -> covariance_xy, variance_x
        :return: float, linear regression slope.
        """
        m = 0
        if len(Args) == 3:
            m = Args[0] * math.sqrt(Args[2] / Args[1])

        if len(Args) == 2:
            m = Args[0] / Args[1]

        return m

    @staticmethod
    def normal(x: float, mean_var: list) -> float:
        """
        Returns an evaluation of the normal distribution at x.
        :param x: float.
        :param mean_var: list, mean/variance
        :return: float.
        """
        mu = mean_var[0]
        variance = mean_var[1]

        A = 1 / math.sqrt(2 * math.pi)
        xp = -0.5 * pow(x - mu, 2) / variance

        return A * math.exp(xp)

    def std_normal_prob(self, x: float, mean: float, variance: float) -> float:
        """
        Returns an evaluation of the standard normal distribution at z; given x, mu, and sigma.
        :param x: float.
        :param mean: float
        :param variance, float
        :return: float
        """
        mu = mean

        z = (x - mu) / math.sqrt(variance)
        P = 0

        dx = 0.0001
        x = -10000
        while x < z:
            P += self.normal(x, [0, 1]) * dx
            x += dx

        return P

    @staticmethod
    def gamma_dist(x: float, Args: list) -> float:
        """
        Gamma distribution function
        :param x: float, value > 0.
        :param Args: list, [shape param (alpha), scale/stretch param (beta)]; beta > 0
        :return: float
        """
        alpha = Args[1]
        beta = Args[2]

        return pow(beta, alpha)*pow(x, alpha - 1)*math.exp(-beta*x)

    def gamma_prob(self, alpha: float, beta: float, interval: list=[.00001, 10000]) -> float:
        """
        Returns probability on an interval
        :param alpha: float, shape parameter
        :param beta: float, scale/stretch parameter
        :param interval: list, Default: [.00001, 10000]
        :return: float
        """
        P = 0

        dx = 0.0001
        area = 0
        x = interval[0]
        while x < interval[1]:
            area += self.gamma_dist(x, [alpha, beta]) * dx
            x += dx

        return P

    @staticmethod
    def monte_carlo_1(sample_space: list, success: float, num_trials: int = 10000) -> float:
        """
        Returns probability via monte carlo method; Success is determined by exact value.
        :param sample_space: list, contains all historical outcomes.
        :param success: float, only values equal to this value constitute a success.
        :param num_trials: int, number of times the historical outcomes will be sampled; Default: 1000
        :return: float, probability of observing 'success' parameter.
        """
        num_success = 0
        for trial in range(num_trials):
            if random.choice(sample_space) == success:
                num_success += 1

        return num_success / num_trials

    @staticmethod
    def monte_carlo_2(sample_space: list, success_threshold: float, num_trials: int = 10000) -> float:
        """
        Returns probability via monte carlo method; Success is determined by a threshold value.
        :param sample_space: list, contains all historical outcomes.
        :param success_threshold: float, values greater than or equal to this value constitute a success.
        :param num_trials: int, number of times the historical outcomes will be sampled; Default: 1000
        :return: float, probability of observing values greater than or equal to 'success_threshold' parameter.
        """
        num_success = 0
        for trial in range(num_trials):
            if random.choice(sample_space) >= success_threshold:
                num_success += 1

        return num_success / num_trials

    @staticmethod
    def monte_carlo_3(sample_space: list, success_interval: list, num_trials: int = 1000) -> float:
        """
        Returns probability via monte carlo method; Success is determined by a success interval.
        :param sample_space: list, contains all historical outcomes.
        :param success_interval: list, values within this interval constitute a success.
        :param num_trials: int, number of times the historical outcomes will be sampled; Default: 1000.
        :return: float, probability of observing values within the 'success_interval' parameter.
        """
        num_success = 0
        for trial in range(num_trials):
            if success_interval[0] < random.choice(sample_space) < success_interval[1]:
                num_success += 1

        return num_success / num_trials

    @staticmethod
    def gaussian_mixed_model(data: list, *, n_clusters=1):
        gmm = GaussianMixture(n_components=n_clusters, random_state=31415, max_iter=1000).fit_predict(data)

    @staticmethod
    def ml_linreg_1(dataset_xy, EPOCH=500, *, slope: float) -> float:
        """
        PyTorch machine learning algorithm for linear regression.
        :param dataset_xy: list, containing two 1-dimensional lists of the same length.
        :param slope: float, known slope of the line.
        :return: float, y-intercept
        """
        x = []
        y = []
        for i in range(len(dataset_xy[0])):
            x.append([dataset_xy[0][1]])
            y.append([dataset_xy[1][1]])

        x = torch.Tensor(x)
        y = torch.Tensor(y)

        b = nn.Parameter(torch.randn(1, 1))
        M = torch.Tensor([slope])
        loss_f = torch.nn.MSELoss(size_average=False)
        optimizer = torch.optim.SGD([b], lr=0.001)

        epoch = 0
        while epoch < EPOCH:
            pred_y = M * x + b
            optimizer.zero_grad()
            loss = loss_f(pred_y, y)
            loss.backward()
            optimizer.step()

            epoch += 1

        return b.item()

    @staticmethod
    def ml_linreg_2(dataset_xy, *, y_intercept):
        """
        PyTorch machine learning algorithm for linear regression.
        :param dataset_xy: list, containing two 1-dimensional lists of the same length.
        :param y_intercept: float, known y-intercept of the line.
        :return: float, slope
        """
        x = []
        y = []
        for i in range(len(dataset_xy[0])):
            x.append([dataset_xy[0][1]])
            y.append([dataset_xy[1][1]])

        x = torch.Tensor(x)
        y = torch.Tensor(y)

        m = nn.Parameter(torch.randn(1, 1))
        B = torch.Tensor([y_intercept])
        loss_f = torch.nn.MSELoss(size_average=False)
        optimizer = torch.optim.SGD([m], lr=0.001)

        epoch = 0
        while epoch < 1500:
            pred_y = m * x + B
            optimizer.zero_grad()
            loss = loss_f(pred_y, y)
            loss.backward()
            optimizer.step()

            epoch += 1

        return m.item()


statistics_ = STATS()
