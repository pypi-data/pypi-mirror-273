# noinspection PyPackageRequirements
from numpy import array, ndarray, vstack, ones_like, identity, cos, sin


class Affine:
    """
    Object representing an affine transformation matrix
    """
    def __init__(self):
        self._matrix = identity(3, dtype=float)

    def __call__(self, x: ndarray, y: ndarray) -> tuple[ndarray, ndarray]:
        """
        Computes the affine transformation and returns the transformed x and y vectors.
        :param x: ndarray representing the x-axis
        :param y: ndarray representing the y-axis
        :return: transformed x and y vectors
        """
        arr = vstack((x, y, ones_like(x)))
        arr = self._matrix.dot(arr)

        return arr[0, :].T, arr[1, :].T

    def rotate(self, angle: float):
        """
        Sets the affine matrix to rotate by angle
        :param angle: the angle to rotate
        """
        self._matrix[0:2, 0:2] = array([[cos(angle), -sin(angle)],
                                        [sin(angle), cos(angle)]])

    def translate(self, dx: float = 0, dy: float = 0):
        """
        Sets the affine matrix to translate by dx and dy from its current position.
        :param dx: the amount to move in the x direction
        :param dy: the amount to move in the y direction
        """
        self._matrix[0, 2] += dx
        self._matrix[1, 2] += dy

    def scale(self, x_scale: float = 1, y_scale: float = 1):
        """
        Sets the affine matrix to scale by x-scale and y-scale from its current value.
        :param x_scale: the amount to scale the x-axis
        :param y_scale: the amount to scale the y-axis
        """
        self._matrix[0, 0] *= x_scale
        self._matrix[1, 0] *= x_scale
        self._matrix[1, 1] *= y_scale
        self._matrix[0, 1] *= y_scale
