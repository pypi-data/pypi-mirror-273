from functools import cached_property
import numpy as np


def div_to_prob(numerator, denominator):
    return np.divide(numerator, denominator, out=np.ones_like(numerator), where=denominator != 0)


def div_check_zero(numerator, denominator):
    return np.divide(numerator, denominator, out=np.full_like(numerator, np.inf), where=denominator != 0)


class InterestMeasures:
    _function_registry = []

    def __init__(self, A, B, AB, N):
        """
        Initializes an Interest Measures.

        :param A: A list representing the probabilities for events in A. List or numpy array.
        :param B: A list representing the probabilities for events in B. List or numpy array.
        :param AB: A list representing the probabilities for events in AB. List or numpy array.
        :param N: An integer representing the number of transactions. Default is 10.
        """

        super().__init__()

        self.A = np.array(A)
        self.B = np.array(B)
        self.AB = np.array(AB)
        self.N = N

        self.notB = 1 - self.B  # P(~B)
        self.notA = 1 - self.A  # P(~self.A)
        self.AnotB = self.A - self.AB  # P(self.A~B)
        self.notAB = self.B - self.AB  # P(~self.AB)
        self.notAnotB = 1 - self.B - self.A + self.AB  # P(~self.A~B)
        self.B_A = div_to_prob(self.AB, self.A)  # P(B|self.A)
        self.A_B = div_to_prob(self.AB, self.B)  # P(self.A|B)
        self.B_notA = div_to_prob(self.notAB, self.notA)  # P(B|~self.A)
        self.A_notB = div_to_prob(self.AnotB, self.notB)  # P(self.A|~B)
        self.notB_notA = 1 - self.B_notA  # P(~B|~self.A)
        self.notA_notB = 1 - self.A_notB  # P(~self.A|~B)
        self.notB_A = 1 - self.B_A  # P(~B|self.A)
        self.notA_B = 1 - self.A_B  # P(~self.A|B)

        self.equations = []

    def _len__(self):
        return len(self.A)

    @cached_property
    def one_way_support(self):
        return self.B_A * np.log2(self.B_A / self.B)

    @cached_property
    def two_way_support(self):
        return self.AB * np.log2(self.AB / (self.A * self.B))

    @cached_property
    def accuracy(self):
        return self.AB + self.notAnotB

    @cached_property
    def added_value(self):
        return self.B_A - self.B

    @cached_property
    def chi_square(self):
        return div_check_zero(((self.AB - (self.A * self.B)) ** 2) * self.N, self.A * self.notA * self.B * self.notB)

    @cached_property
    def collective_strength(self):
        return (((self.AB + self.notAnotB) / ((self.A * self.B) + (self.notA * self.notB))) *
                (div_check_zero(1 - (self.A * self.B) - (self.notA * self.notB),
                                np.around((1 - self.AB - self.notAnotB), 10))))

    @cached_property
    def complement_class_support(self):
        """
        Complement Class Support

        Negative interest measure.
        """
        return -1 * div_check_zero(self.AnotB, self.notB)

    @cached_property
    def conditional_entropy(self):
        return (-1 * self.B_A * np.log2(self.B_A) +
                np.where(self.notB_A == 0, 0, -1 * self.notB_A * np.log2(self.notB_A)))

    @cached_property
    def confidence(self):
        return self.B_A

    @cached_property
    def confidence_causal(self):
        return (self.B_A + self.notA_notB) / 2

    @cached_property
    def confirm_causal(self):
        return self.AB + self.notAnotB - (2 * self.AnotB)

    @cached_property
    def confirm_descriptive(self):
        return self.AB - self.AnotB

    @cached_property
    def confirmed_confidence_causal(self):
        return ((self.B_A + self.notA_notB) / 2) - self.notB_A

    @cached_property
    def conviction(self):
        return div_check_zero(self.A * self.notB, self.AnotB)

    @cached_property
    def correlation_coefficient(self):
        return div_check_zero(self.AB - (self.A * self.B), np.sqrt(self.A * self.B * self.notA * self.notB))

    @cached_property
    def cosine(self):
        return self.AB / np.sqrt(self.A * self.B)

    @cached_property
    def coverage(self):
        return self.A

    @cached_property
    def dir(self):
        result = np.zeros(self.B.shape)

        result = np.where(np.logical_and((self.B <= 0.5), (self.B_A <= 0.5)), 0, result)

        result = np.where(
            np.logical_and(
                np.logical_and((self.B <= 0.5), (self.B_A > 0.5)), (self.B_A != 1)
            ),
            1 + (self.B_A * np.log2(self.B_A)) + (self.notB_A * np.log2(self.notB_A)),
            result,
        )

        result = np.where(
            np.logical_and(
                np.logical_and((self.B <= 0.5), (self.B_A > 0.5)), (self.B_A == 1)
            ),
            1,
            result,
        )

        result = np.where(
            np.logical_and((self.B > 0.5), (self.B_A <= 0.5)),
            1 + (1 / (self.B * np.log2(self.B) + self.notB * np.log2(self.notB))),
            result,
        )

        result = np.where(
            np.logical_and(
                np.logical_and((self.B > 0.5), (self.B_A > 0.5)), (self.B_A != 1)
            ),
            1 - ((self.B_A * np.log2(self.B_A) + self.notB_A * np.log2(self.notB_A)) / (
                    self.B * np.log2(self.B) + self.notB * np.log2(self.notB))),
            result,
        )

        result = np.where(
            np.logical_and(np.logical_and((self.B > 0.5), (self.B_A > 0.5)), (self.B_A == 1)),
            1 - ((self.B_A * np.log2(self.B_A)) / (self.B * np.log2(self.B) + self.notB * np.log2(self.notB))),
            result,
        )

        result = np.where(self.B == 1, -np.inf, result)

        return result

    def _dir_for_tic(self, A, B, AB):
        B_A = np.around(AB / A, 11)
        notB = 1 - B
        notB_A = np.around(1 - B_A, 11)

        result = np.zeros(B.shape)

        result = np.where(np.logical_and((B <= 0.5), (B_A <= 0.5)), 0, result)

        result = np.where(
            np.logical_and(np.logical_and((B <= 0.5), (B_A > 0.5)), (B_A != 1)),
            1 + B_A * np.log2(B_A) + notB_A * np.log2(notB_A),
            result,
        )

        result = np.where(
            np.logical_and(np.logical_and((B <= 0.5), (B_A > 0.5)), (B_A == 1)),
            1 + B_A * np.log2(B_A),
            result,
        )

        result = np.where(
            np.logical_and((B > 0.5), (B_A <= 0.5)),
            1 + (1 / (B * np.log2(B) + notB * np.log2(notB))),
            result,
        )

        result = np.where(
            np.logical_and(np.logical_and((B > 0.5), (B_A > 0.5)), (B_A != 1)),
            1
            - (B_A * np.log2(B_A) + notB_A * np.log2(notB_A))
            / (B * np.log2(B) + notB * np.log2(notB)),
            result,
        )

        result = np.where(
            np.logical_and(np.logical_and((B > 0.5), (B_A > 0.5)), (B_A == 1)),
            1 - (B_A * np.log2(B_A)) / (B * np.log2(B) + notB * np.log2(notB)),
            result,
        )

        result = np.where(B == 1, -np.inf, result)

        return result

    @cached_property
    def exemple_and_counterexemple_rate(self):
        return 1 - (self.AnotB / self.AB)

    @cached_property
    def f_measure(self):
        return (2 * self.A_B * self.B_A) / (self.A_B + self.B_A)

    @cached_property
    def ganascia(self):
        return (2 * self.B_A) - 1

    @cached_property
    def gini_index(self):
        return ((self.A * ((self.B_A ** 2) + (self.notB_A ** 2))) +
                (self.notA * ((self.B_notA ** 2) + (self.notB_notA ** 2))) -
                (self.B ** 2) -
                (self.notB ** 2))

    @cached_property
    def goodman_kruskal(self):
        part1 = (
                np.max([self.AB, self.AnotB], axis=0)
                + np.max([self.notAB, self.notAnotB], axis=0)
                + np.max([self.AB, self.notAB], axis=0)
                + np.max([self.AnotB, self.notAnotB], axis=0)
                - np.max([self.A, self.notA], axis=0)
                - np.max([self.B, self.notB], axis=0)
        )

        part2 = (
                2
                - np.max([self.A, self.notA], axis=0)
                - np.max([self.B, self.notB], axis=0)
        )

        return div_check_zero(part1, part2)

    @cached_property
    def implication_index(self):
        """
        Implication Index

        Negative interest measure.
        """
        return -1 * div_check_zero((self.AnotB - (self.A * self.notB)), np.sqrt(self.A * self.notB))

    @cached_property
    def information_gain(self):
        return np.log2((self.AB / (self.A * self.B)))

    @cached_property
    def jaccard(self):
        return self.AB / (self.A + self.B - self.AB)

    @cached_property
    def j_measure(self):
        return (self.AB * np.log2(self.B_A / self.B) +
                (np.where((self.notB * self.notB_A) == 0, 0, self.AnotB * np.log2(self.notB_A / self.notB), )))

    @cached_property
    def kappa(self):
        return div_check_zero(
            ((self.B_A * self.A) + (self.notB_notA * self.notA) - (self.A * self.B) - (self.notA * self.notB)),
            1 - (self.A * self.B) - (self.notA * self.notB))

    @cached_property
    def klosgen(self):
        return np.sqrt(self.A) * (self.B_A - self.B)

    @cached_property
    def k_measure(self):
        return (self.B_A * np.log2(self.B_A / self.B) +
                self.B_A * np.log2(self.B_A / self.notB) -
                np.where(self.notB_notA == 0, 0, (self.notB_notA * np.log2(self.notB_notA / self.notB))) -
                np.where(self.notB_notA == 0, 0, (self.notB_notA * np.log2(self.notB_notA / self.B))))

    @cached_property
    def kulczynski_1(self):
        return div_check_zero(self.AB, self.AnotB + self.notAB)

    @cached_property
    def kulczynski_2(self):
        return ((self.AB / self.A) + (self.AB / self.B)) / 2

    @cached_property
    def laplace_correction(self):
        return (self.N * self.AB + 1) / (self.N * self.A + 2)

    @cached_property
    def least_contradiction(self):
        return (self.AB - self.AnotB) / self.B

    @cached_property
    def leverage(self):
        return self.B_A - (self.A * self.B)

    @cached_property
    def lift(self):
        return self.AB / (self.A * self.B)

    @cached_property
    def loevinger(self):
        return np.where(self.notB == 0, 0, 1 - (self.AnotB / (self.A * self.notB)))

    @cached_property
    def logical_necessity(self):
        """
        Logical Necessity

        Negative interest measure.
        """
        return -1 * div_check_zero(self.notA_B, self.notA_notB)

    @cached_property
    def mutual_information(self):
        return (self.AB * np.log2(self.AB / (self.A * self.B)) +
                np.where(self.AnotB == 0, 0, self.AnotB * np.log2(self.AnotB / (self.A * self.notB))) +
                np.where(self.notAB == 0, 0, self.notAB * np.log2(self.notAB / (self.notA * self.B))) +
                np.where(self.notAnotB == 0, 0, self.notAnotB * np.log2(self.notAnotB / (self.notA * self.notB))))

    @cached_property
    def normalized_mutual_information(self):
        return div_check_zero(np.around(self.mutual_information, 10),
                              np.where(
                                  self.A == 1,
                                  (-self.A * np.log2(self.A)),
                                  (-self.A * np.log2(self.A)) - (self.notA * np.log2(self.notA)),
                              ))

    @cached_property
    def odd_multiplier(self):
        return div_check_zero(self.AB * self.notB, self.B * self.AnotB)

    @cached_property
    def odds_ratio(self):
        return div_check_zero(self.AB * self.notAnotB, self.AnotB * self.notAB)

    @cached_property
    def piatetsky_shapiro(self):
        return self.AB - (self.A * self.B)

    @cached_property
    def prevalence(self):
        return self.B

    @cached_property
    def putative_causal_dependency(self):
        return (((self.B_A - self.B) / 2) +
                (self.notA_notB - self.notA) -
                (self.notB_A - self.notB) -
                (self.A_notB - self.A))

    @cached_property
    def recall(self):
        return self.A_B

    @cached_property
    def relative_risk(self):
        return div_check_zero(self.B_A, self.B_notA)

    @cached_property
    def sebag_schoenaure(self):
        return div_check_zero(self.AB, self.AnotB)

    @cached_property
    def specificity(self):
        return self.notB_notA

    @cached_property
    def support(self):
        return self.AB

    @cached_property
    def theil_uncertainty_coefficient(self):
        return div_check_zero(np.around(self.mutual_information, 10),
                              np.where(self.B == 1,
                                       (-self.B * np.log2(self.B)),
                                       (-self.B * np.log2(self.B)) - (self.notB * np.log2(self.notB)),
                                       ))

    @cached_property
    def tic(self):
        part2 = np.around(self._dir_for_tic(A=self.notB, B=self.notA, AB=self.notAnotB), 10)
        return np.where(self.B == 1, -np.inf, np.sqrt(np.around(self.dir, 10) * part2))

    @cached_property
    def yuleQ(self):
        return div_check_zero((self.AB * self.notAnotB) - (self.AnotB * self.notAB),
                              (self.AB * self.notAnotB) + (self.AnotB * self.notAB))

    @cached_property
    def yuleY(self):
        return div_check_zero(np.sqrt(self.AB * self.notAnotB) - np.sqrt(self.AnotB * self.notAB),
                              np.sqrt(self.AB * self.notAnotB) + np.sqrt(self.AnotB * self.notAB))

    @cached_property
    def zhang(self):
        part1 = self.AB - (self.A * self.B)
        part2 = np.max([self.AB * (1 - self.B), self.B * (self.A - self.AB)], axis=0)

        return div_check_zero(part1, part2)

    @cached_property
    def modified_lift(self):
        return self.notAnotB / self.AnotB

    @cached_property
    def dm2(self):
        return self.notAnotB / (self.AnotB * np.sqrt(self.B))

    @cached_property
    def dm3(self):
        return (self.notAnotB * self.A) / (self.AnotB * np.sqrt(self.B))

    @cached_property
    def dm4(self):
        return self.notAnotB / (self.AnotB * np.sqrt(self.A))
