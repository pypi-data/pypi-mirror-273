import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr

class LinearR:
    # Linear Regression Class
    def __init__(self, x_data, y_data):
        # Initialization
        x = np.array(x_data).reshape(-1, 1)
        y = np.array(y_data)
        modelo = LinearRegression()
        modelo.fit(x, y)
        self.corr = pearsonr(x_data, y_data)[0]
        self.mx = float(modelo.coef_)
        self.bx = modelo.intercept_
    def predicty(self, x_pred):
        # Prediction of 'y' based on 'x'
        predicty = self.mx * x_pred + self.bx
        return predicty
    def predictx(self, y_pred):
        # Prediction of 'x' based on 'y'
        predictx = (y_pred - self.bx) / self.mx
        return predictx
    def r(self):
        # Pearson correletion coeficient
        return self.corr
    def r2(self):
        # Determination coeficient
        return self.corr ** 2
    def m(self):
        # Slope
        return self.mx
    def b(self):
        # Intercept
        return self.bx
    def eq(self):
        # Linear ecuation in the form 'y = mx + b'
        if self.bx > 0:
            s = '+'
        elif self.bx < 0:
            s = '-'
        elif self.bx == 0:
            s = ''
        eq = f"y = {self.mx}x {s} {abs(self.bx)}"
        return eq
