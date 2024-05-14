import math
import numpy as np
import unsatfit


class Fit(unsatfit.Fit):
    """hystfit - Fit soil water retention function with hysteresis

    Implementation of Zhao model as a subclass of unsatfit.Fit class.

    Zhao, A. (2013) A contact angle-dependent hysteresis model for soil–water retention behaviour,
         Computers and Geotechnics 49: 36-42. https://doi.org/10.1016/j.compgeo.2012.10.004

    Website: https://sekika.github.io/hystfit/
    Author: Katsutoshi Seki
    License: MIT License
    """

    # Initialization

    def __init__(self):
        super(Fit, self).__init__()
        self.debug = False
        self.no_warn = False
        # cos(gamma_R), where gamma_R is the receding contact angle
        self.cos_gr = 1
        # cos(gamma_0), where gamma_0 is the initial contact angle
        self.cos_g0 = 1
        self.delta_theta = 0.0001  # step of calculation of d_theta
        self.delta_h = 1  # step of calculation of d_h when dSe/dt is small
        self.dry_se = lambda h: False  # Mark that drying curve is not set
        self.lsq_ftol_hyst = 1e-8  # Tolerance of least square optimization
        self.max_se = 1  # Maximum Se
        # Bound of parameters
        self.b_cos_g = (0, 1)
        self.b_b = (0, 1)

    def init_hyst(self):
        import sys
        if self.model_name == 'VG':
            a, m = self.get_init_vg()
            qs = max(self.swrc[1])
            self.set_model('VG', const=['qr=0', 'q=1'])
            self.ini = (qs, a, m)
            self.b_qs = (qs * 0.99, qs * 1.1)
            self.optimize()
            qs, a, m = self.fitted
            qr = 0.0
            n = 1 / (1 - m)
            self.set_vg(qs, qr, a, n)
        elif self.model_name == 'FX':
            a, m, n = self.get_init_fx()
            qs = max(self.swrc[1])
            self.set_model('FX', const=['qr=0'])
            self.ini = (qs, a, m, n)
            self.b_qs = (qs * 0.99, qs * 1.1)
            self.optimize()
            qs, a, m, n = self.fitted
            qr = 0.0
            self.set_fx(qs, qr, a, m, n)
        else:
            print(
                f'Model name {self.model_name} is not implemented in hystfit.')
            sys.exit(1)

    # VG model (van Genuchten, 1980)

    def set_vg(self, theta_s, theta_r, alpha, n):
        self.dry_se = self.vg_seh  # Se(h)
        self.dry_h = self.vg_h  # h(Se)
        self.dry_c = self.vg_c  # dSe/dh
        self.theta_s = theta_s
        self.theta_r = theta_r
        self.swrf_p = alpha, n
        self.cos_g0 = 1

    def vg_seh(self, h):  # Se(h)
        alpha, n = self.swrf_p  # VG parameter
        return (1 + (alpha * h)**n)**(1 / n - 1)

    def vg_h(self, se):  # inverse of Se(h): h(Se)
        alpha, n = self.swrf_p  # VG parameter
        h = (se**(n / (1 - n)) - 1)**(1 / n) / alpha
        return h

    def vg_c(self, h):  # derivative of Se(h): dSe/dh
        alpha, n = self.swrf_p
        if h == 0:
            return 0
        dsedh = (1 - n) / h * (1 + (alpha * h) **
                               n)**((1 - 2 * n) / n) * (alpha * h)**n
        return dsedh

    # FX model (Fredlund and Xing, 1994)

    def set_fx(self, theta_s, theta_r, a, m, n):
        self.dry_se = self.fx_seh  # Se(h)
        self.dry_h = self.fx_h  # h(Se)
        self.dry_c = self.fx_c  # dSe/dh
        self.theta_s = theta_s
        self.theta_r = theta_r
        self.swrf_p = a, m, n
        self.cos_g0 = 1

    def fx_seh(self, h):  # Se(h)
        a, m, n = self.swrf_p  # FX parameter
        return (np.log(np.e + (h / a)**n))**(-m)

    def fx_h(self, se):  # inverse of Se(h): h(Se)
        import warnings
        # supress RuntimeWarning: invalid value encountered in double_scalars
        warnings.simplefilter("ignore")
        a, m, n = self.swrf_p  # FX parameter
        return np.where(se >= 1, 0, a * (np.exp(se**(-1 / m)) - np.e)**(1 / n))

    def fx_c(self, h):  # derivative of Se(h): dSe/dh
        a, m, n = self.swrf_p  # FX parameter
        return -m * self.fx_seh(h)**(1 + 1 / m) * n / \
            a * (h / a)**(n - 1) / (np.e + (h / a)**n)

    # Test

    def test(self):
        f = Fit()
        # Test FX model
        f.set_fx(0.35, 0.02, 45, 1.25, 7.23)
        f.test_model()
        # Set parameters in Zhou (2013) and test VG model
        f.set_vg(0.33, 0.05, 1 / 180, 1.65)  # theta_s and theta_r is random
        p = (math.cos(math.radians(75)), 0.24)
        f.test_model()
        # Test h method
        se = np.array([1, 0.99, 0.8, 0.7, 0.58, 0.6, 0.62, 0.7, 0.8, 0.9])
        x = se * (f.theta_s - f.theta_r) + f.theta_r
        f.delta_theta = 0.001  # Test with low precision
        f.max_se = 1
        h = f.h(p, x)
        self.check(int(sum(h) * 100000), 92429737)
        # Test contact method
        self.check(int(f.contact(100, 0.2) * 100000), 56289)
        # Test smooth_theta method
        self.check(int(sum(self.smooth_theta(se) * 1000)), 124795)
        # Test opt method
        h = np.array([460, 100, 60, 40, 22])
        se = np.array([0.5, 0.6, 0.7, 0.8, 0.9])
        x = se * (f.theta_s - f.theta_r) + f.theta_r
        f.opt(h, x)
        assert f.r2 > 0.999, f'Precision error. R2 = {f.r2:.5f}'
        self.check(int(sum(f.hyst) * 1000000), 501368)
        if self.debug:
            print('Test complete without error.')

    def check(self, actual, expect):
        assert expect == actual, 'Assertion error. Expected = {0} Actual = {1}'.format(
            expect, actual)

    def test_model(self):
        split = 87
        for i in range(1, split):
            se = i / split
            h = self.dry_h(se)
            assert abs(self.dry_se(
                h) - se) < 10**(-15), 'Precision error of h(Se) at h = {0:.3f}'.format(h)
            dsedh = self.dry_c(h)
            delta = h * 10**(-8)
            d = (self.dry_se(h + delta) - se) / delta
            prec = abs(d / dsedh - 1)
            assert prec < 10**(-6), 'Precision error of C(h) at h = {0:.3f}'.format(
                h)

    # Calculate dh from h, theta, d_theta, (cos_ga, b)

    def dsedh(self, h, theta, d_theta, p):  # dSe/dh
        import sys
        if h == 0:
            return 0
        cos_ga, b = p  # hysteresis parameters: cos(theta_A) and b
        # Calculate hd = h at drying curve
        se = (theta - self.theta_r) / (self.theta_s - self.theta_r)
        # Fix Se > max_se
        if se > self.max_se:
            se = self.max_se
        hd = self.dry_h(se)
        if math.isnan(hd):
            print(f'Error: h was not calculated at Se = {se}')
            sys.exit()
        # Calculate cos_g = cos(theta)
        if hd == 0:
            cos_g = self.cos_gr
        else:
            cos_g = self.cos_gr * h / hd
        # Calculate k of eq. 11 in Zhao (2013)
        if d_theta < 0:  # when ds<0
            k = cos_g - self.cos_gr
        else:  # when ds>0
            k = cos_ga - cos_g
        k = k / (cos_ga - self.cos_gr)
        if k < 0:
            k = 0
        if k > 1:
            k = 1
        k = k ** b
        # Calculate dsedh = dSe/dh
        dsedh = self.dry_c(hd)
        if math.isnan(dsedh):
            print(f'Error: dSe/dh was not calculated at h = {hd}')
            sys.exit()
        dsedh *= hd / h * (1 - k)
        return dsedh

    def h(self, p, x, cont=True):
        """Calculate hysteresis

        input

            p = (cos(theta_A), b)
            x = (theta_0, theta_1, theta_2, ...)
            cont : if True, the last contact angle is remembered for the next initial value

            self.cos_g0 : cos of the initial contact angle

        returns (h1, h2, ...)
        """
        import sys
        assert not math.isnan(self.cos_g0)
        theta = x[0]
        assert self.dry_se(0), print(
            'Drying curve not set. Use set_vg or set_fx')
        if max(x) > self.theta_s * self.max_se and not self.no_warn:
            print(
                f'Effective saturation exceeding {self.max_se} is fixed to {self.max_se}.')
        if min(x) < self.theta_r:
            print('Water content below residual value is found.')
            sys.exit()

        def se(theta):
            return (theta - self.theta_r) / (self.theta_s - self.theta_r)
        h = self.dry_h(se(theta)) * self.cos_g0 / self.cos_gr
        ret = [h]
        max_t = self.max_se * (self.theta_s - self.theta_r) + self.theta_r
        for t in list(x)[1:]:
            if t > max_t:
                t = max_t
            while t != theta:
                dt = t - theta
                if self.dry_se(
                        h) * self.max_se < se(theta) and dt < 0 or h == 0:
                    h = self.dry_h(se(theta))
                    theta = t
                    continue
                if abs(dt) > self.delta_theta:
                    dt = self.delta_theta * dt / abs(dt)
                dse = dt / (self.theta_s - self.theta_r)
                dsedh = self.dsedh(h, theta, dt, p)
                if abs(dse) < self.delta_h * abs(dsedh):
                    dh = dse / dsedh
                else:
                    dh = -self.delta_h * dt / abs(dt)
                    dse = dh * dsedh
                    dt = dse * (self.theta_s - self.theta_r)
                h += dh
                if h < 0:
                    h = 0
                theta += dt
                if h > self.dry_h(se(theta)):
                    h = self.dry_h(se(theta))
            ret.append(h + 0)
        if cont:
            self.cos_g0 = self.contact(ret[-1], x[-1])
            assert self.cos_g0 >= 0
        return ret

    def contact(self, h, theta):
        """Get cosine of contact angle

        input

            h = pressure head
            theta = water content

        returns cos(contact angle)
        """
        se = theta / (self.theta_s - self.theta_r) + self.theta_r
        if se >= 1:
            return 1
        cos_g = h / self.dry_h(se) * self.cos_gr
        return cos_g

    def smooth_theta(self, theta, delta=0.005):
        """Get theta for drawing smooth curve

        input
            theta = (theta_0, theta_1, theta_2, ...)
            delta = increment (upper limit)

        returns (theta_0, theta_0+delta, ...., theta_1, ...)
        """
        if len(theta) < 2:
            return theta
        prev = theta[0]
        smooth = []
        for t in theta[1:]:
            num = math.floor(abs(t - prev) / delta) + 2
            smooth = np.concatenate((smooth, np.linspace(prev, t, num=num)))
            prev = t
        return smooth

    def opt(self, h_measured, theta):
        """Optimize hysteresis parameters

        input

            h_measured = (h_0, h_1, h_2, ...)
            theta = (theta_0, theta_1, theta_2, ...)

        returns (cos(gamma_A), b)
        """
        import copy
        from scipy import optimize
        import sys
        if min(h_measured) < 0:
            print('Input value error: h<0 is not allowed.')
            sys.exit()
        omit = 'It is recommended to omit the saturated point in the optimization, ' + \
            'as a very small error in the predicted h can cause a large error ' + \
            'in ln(h) in the cost function.'
        if min(h_measured) == 0:
            print('Input value error: h=0 is not allowed. ' + omit)
            sys.exit()
        theta = np.array(theta)
        se = (theta - self.theta_r) / (self.theta_s - self.theta_r)
        if max(se) > 1:
            print('Input value error: Water content exceeds saturated value.')
            sys.exit()
        if max(se) == 1:
            print(
                'Input value error: Water content at saturated value is not allowed. ' + omit)
            sys.exit()
        if min(se) < 0:
            print('Input value error: Water content is below residual value.')
            sys.exit()
        hd = self.dry_h(se)
        cos_g = np.where(hd > 0, self.cos_gr * h_measured / hd, self.cos_gr)
        ini_cos_g = min(cos_g)
        ini_b = 0.5
        ini = ini_cos_g, ini_b
        a = (h_measured, theta)
        b = (self.b_cos_g, self.b_b)
        b = tuple(zip(*b))
        cos_g0 = self.contact(h_measured[0], theta[0])
        if cos_g0 > 1:
            cos_g0 = 1

        def cost(p, h, theta):
            return np.log(self.h(p, theta, cont=False) / h)
        success = False
        for ftol in self.lsq_ftol:
            self.cos_g0 = cos_g0
            result = optimize.least_squares(
                cost, ini, jac=self.lsq_jac, method=self.lsq_method, loss=self.lsq_loss,
                ftol=ftol, max_nfev=self.lsq_max_nfev, bounds=b, verbose=self.lsq_verbose, args=a)
            if result.success:
                ini = result.x
                success = True
                prev_result = copy.deepcopy(result)
            else:
                if success:
                    result = copy.deepcopy(prev_result)
                break
        self.success = result.success
        self.hyst = result.x
        if not self.success:
            self.hyst = []
            self.message = result.message  # Verbal description of the termination reason
            return

        self.cos_g0 = cos_g0
        # Statistics
        n = result.fun.size  # sample size
        k = self.hyst.size  # number of paramteres
        self.mean_h = np.average(h_measured)
        self.var_h = np.average((h_measured - self.mean_h)**2)

        def residual(p, x, y):
            return self.h(p, x) - y
        self.mse = np.average(
            residual(self.hyst, theta, h_measured)**2)
        self.se = math.sqrt(self.mse)  # Standard error
        self.r2 = 1 - self.mse / self.var_h  # Coefficient of determination
        self.aic = n * np.log(self.mse) + 2 * k  # AIC
        if n - k - 1 > 0:
            self.aicc = self.aic + 2 * k * \
                (k + 1) / (n - k - 1)  # Corrected AIC
        self.message = 'cos(γA) = {0:.3f} b = {1:.2f}'.format(*self.hyst)
        self.cos_g0 = self.contact(h_measured[-1], theta[-1])
