import numpy as np
import scipy.odr as odr
from scipy.optimize import curve_fit
import scipy.stats as st
import matplotlib.pyplot as plt

"""
Model

"""


def model_unpaired(cyt, wd, wm):
    ka = np.exp(wd)
    km = np.exp(wm)
    c1 = cyt
    m1 = c1 * km * (c1 * ka * km * (2 * c1 * ka + np.sqrt(4 * c1 * ka + 1) + 1) + np.sqrt(
        4 * c1 ** 3 * ka ** 3 + 6 * c1 ** 2 * ka ** 2 * np.sqrt(
            4 * c1 * ka + 1) + 18 * c1 ** 2 * ka ** 2 + 8 * c1 * ka * np.sqrt(
            4 * c1 * ka + 1) + 12 * c1 * ka + 2 * np.sqrt(4 * c1 * ka + 1) + 2)) / (
                 2 * c1 ** 2 * ka ** 2 + 2 * c1 * ka * np.sqrt(4 * c1 * ka + 1) + 4 * c1 * ka + np.sqrt(
             4 * c1 * ka + 1) + 1)
    return m1


def model_unpaired_log(logcyt, wd, wm):
    ka = np.exp(wd)
    km = np.exp(wm)
    c1 = 10 ** logcyt
    m1 = c1 * km * (c1 * ka * km * (2 * c1 * ka + np.sqrt(4 * c1 * ka + 1) + 1) + np.sqrt(
        4 * c1 ** 3 * ka ** 3 + 6 * c1 ** 2 * ka ** 2 * np.sqrt(
            4 * c1 * ka + 1) + 18 * c1 ** 2 * ka ** 2 + 8 * c1 * ka * np.sqrt(
            4 * c1 * ka + 1) + 12 * c1 * ka + 2 * np.sqrt(4 * c1 * ka + 1) + 2)) / (
                 2 * c1 ** 2 * ka ** 2 + 2 * c1 * ka * np.sqrt(4 * c1 * ka + 1) + 4 * c1 * ka + np.sqrt(
             4 * c1 * ka + 1) + 1)
    return np.log10(m1)


def model_paired(cyt_l109r, wd1, wd2, wm):
    ka1 = np.exp(wd1)
    ka2 = np.exp(wd2)
    km = np.exp(wm)
    cyt, l109r = cyt_l109r
    ka = (ka1 * np.array([l109r == 0])).flatten() + (ka2 * np.array([l109r == 1])).flatten()
    c1 = cyt
    m1 = c1 * km * (c1 * ka * km * (2 * c1 * ka + np.sqrt(4 * c1 * ka + 1) + 1) + np.sqrt(
        4 * c1 ** 3 * ka ** 3 + 6 * c1 ** 2 * ka ** 2 * np.sqrt(
            4 * c1 * ka + 1) + 18 * c1 ** 2 * ka ** 2 + 8 * c1 * ka * np.sqrt(
            4 * c1 * ka + 1) + 12 * c1 * ka + 2 * np.sqrt(4 * c1 * ka + 1) + 2)) / (
                 2 * c1 ** 2 * ka ** 2 + 2 * c1 * ka * np.sqrt(4 * c1 * ka + 1) + 4 * c1 * ka + np.sqrt(
             4 * c1 * ka + 1) + 1)
    return m1


def model_log_paired(logcyt_l109r, wd1, wd2, wm):
    ka1 = np.exp(wd1)
    ka2 = np.exp(wd2)
    km = np.exp(wm)
    logcyt, l109r = logcyt_l109r
    cyt = 10 ** logcyt
    c1 = cyt
    ka = (ka1 * np.array([l109r == 0])).flatten() + (ka2 * np.array([l109r == 1])).flatten()
    m1 = c1 * km * (c1 * ka * km * (2 * c1 * ka + np.sqrt(4 * c1 * ka + 1) + 1) + np.sqrt(
        4 * c1 ** 3 * ka ** 3 + 6 * c1 ** 2 * ka ** 2 * np.sqrt(
            4 * c1 * ka + 1) + 18 * c1 ** 2 * ka ** 2 + 8 * c1 * ka * np.sqrt(
            4 * c1 * ka + 1) + 12 * c1 * ka + 2 * np.sqrt(4 * c1 * ka + 1) + 2)) / (
                 2 * c1 ** 2 * ka ** 2 + 2 * c1 * ka * np.sqrt(4 * c1 * ka + 1) + 4 * c1 * ka + np.sqrt(
             4 * c1 * ka + 1) + 1)
    return np.log10(m1)


def model_log_paired_D(logcyt_l109r, wd1, wd2, wm, D):
    ka1 = np.exp(wd1)
    ka2 = np.exp(wd2)
    km = np.exp(wm)
    logcyt, l109r = logcyt_l109r
    cyt = 10 ** logcyt
    c1 = cyt
    ka = (ka1 * np.array([l109r == 0])).flatten() + (ka2 * np.array([l109r == 1])).flatten()
    m1 = c1 * km * (c1 * ka * km * (2 * c1 * ka + np.sqrt(4 * c1 * ka + 1) + 1) + np.sqrt(
        4 * c1 ** 3 * ka ** 3 + 6 * c1 ** 2 * ka ** 2 * np.sqrt(
            4 * c1 * ka + 1) + 18 * c1 ** 2 * ka ** 2 + 8 * c1 * ka * np.sqrt(
            4 * c1 * ka + 1) + 12 * c1 * ka + 2 * np.sqrt(4 * c1 * ka + 1) + 2)) / (
                 2 * c1 ** 2 * ka ** 2 + 2 * c1 * ka * np.sqrt(4 * c1 * ka + 1) + 4 * c1 * ka + np.sqrt(
             4 * c1 * ka + 1) + 1)
    return np.log10(m1) * (10 ** D)


def monomer_fraction(conc, wd):
    return ((np.sqrt(4 * conc * np.exp(wd) + 1) - 1) * np.exp(-wd) / 2) / conc


def dimer_fraction(conc, wd):
    return 1 - (((np.sqrt(4 * conc * np.exp(wd) + 1) - 1) * np.exp(-wd) / 2) / conc)


"""
Fitting

"""


class EnergiesConfidenceIntervalUnpaired:
    def __init__(self, df, whole_embryo=False, log=False, fix_wd=False, p0=(15, 5)):
        # Input
        self.log = log
        if self.log:
            self.cyts = np.log10(df.Cyt.to_numpy())
        else:
            self.cyts = df.Cyt.to_numpy()
        if not whole_embryo:
            if self.log:
                self.mems = np.log10(df.Mem_post.to_numpy())
            else:
                self.mems = df.Mem_post.to_numpy()
        else:
            if self.log:
                self.mems = np.log10(df.Mem_tot.to_numpy())
            else:
                self.mems = df.Mem_tot.to_numpy()
        self.unipol = df.UniPol.tolist()

        # Model
        if self.log:
            self.model = model_unpaired_log
        else:
            self.model = model_unpaired
        self.fix_wd = fix_wd
        self.p0 = p0

        # Output
        self.res_x = None
        self.res_y = None
        self.wd_full = None
        self.wm_full = None
        self.wds = None
        self.wms = None
        self.all_fits_lower = None
        self.all_fits_upper = None
        self.cyt_dim = None
        self.mem_dim = None
        self.cyt_dim_lower = None
        self.cyt_dim_upper = None
        self.mem_dim_lower = None
        self.mem_dim_upper = None

        # Run
        self.run()

    def run(self, n_bootstrap=1000, n_x=100, interval=95):
        self.res_x = np.linspace(0, max(self.cyts), n_x)

        # Analysing full dataset
        popt_full = self.single_fit(self.cyts, self.mems)
        self.res_y = self.model(self.res_x, *popt_full)
        self.wd_full = popt_full[0]
        self.wm_full = popt_full[1]
        if self.log:
            self.cyt_dim = 100 * dimer_fraction(10 ** self.res_x, self.wd_full)
            self.mem_dim = 100 * dimer_fraction(10 ** self.res_y, self.wd_full)
        else:
            self.cyt_dim = 100 * dimer_fraction(self.res_x, self.wd_full)
            self.mem_dim = 100 * dimer_fraction(self.res_y, self.wd_full)

        # Bootstrapping
        params = self.bootstrap_fitting(self.cyts, self.mems)
        self.wds = params[:, 0]
        self.wms = params[:, 1]

        # Confidence interval
        all_fits = np.zeros([n_bootstrap, n_x])
        all_cyt_dim = np.zeros([n_bootstrap, n_x])
        all_mem_dim = np.zeros([n_bootstrap, n_x])
        for i, p in enumerate(params):
            all_fits[i, :] = self.model(self.res_x, *p)
            if self.log:
                all_cyt_dim[i, :] = 100 * dimer_fraction(10 ** self.res_x, p[0])
                all_mem_dim[i, :] = 100 * dimer_fraction(10 ** self.res_y, p[0])
            else:
                all_cyt_dim[i, :] = 100 * dimer_fraction(self.res_x, p[0])
                all_mem_dim[i, :] = 100 * dimer_fraction(self.res_y, p[0])
        self.all_fits_lower = np.percentile(all_fits, (100 - interval) / 2, axis=0)
        self.all_fits_upper = np.percentile(all_fits, 50 + (interval / 2), axis=0)
        self.cyt_dim_lower = np.percentile(all_cyt_dim, (100 - interval) / 2, axis=0)
        self.cyt_dim_upper = np.percentile(all_cyt_dim, 50 + (interval / 2), axis=0)
        self.mem_dim_lower = np.percentile(all_mem_dim, (100 - interval) / 2, axis=0)
        self.mem_dim_upper = np.percentile(all_mem_dim, 50 + (interval / 2), axis=0)

    def single_fit(self, cyt, mem):
        bounds = [[-np.inf, -np.inf], [np.inf, np.inf]]
        epsilon = 0.00000001
        if self.fix_wd:
            bounds[0][0], bounds[1][0] = self.p0[0] - epsilon, self.p0[0] + epsilon
        p0 = self.p0

        popt, pcov = curve_fit(self.model, cyt, mem, maxfev=1000000, p0=p0, bounds=bounds)
        params = popt
        return params

    def bootstrap_fitting(self, cyts, mems, n=1000):
        params = np.zeros([n, 2])
        for i in range(n):
            inds = np.random.choice(range(len(cyts)), len(cyts))
            params[i, :] = self.single_fit(cyts[inds], mems[inds])
        return params


class EnergiesConfidenceIntervalPaired:
    def __init__(self, df, region='post', log=False, p0=(15, 15, 5), fix_wt=False, fix_mut=False, fit_D=False):
        # Import data
        self.log = log
        if region == 'post':
            if self.log:
                mems = np.log10(df.Mem_post.to_numpy())
            else:
                mems = df.Mem_post.to_numpy()
        elif region == 'whole':
            if self.log:
                mems = np.log10(df.Mem_tot.to_numpy())
            else:
                mems = df.Mem_tot.to_numpy()
        else:
            mems = None
        self.mems = mems
        if self.log:
            self.cyts = np.log10(df.Cyt.to_numpy())
        else:
            self.cyts = df.Cyt.to_numpy()
        self.l109r = (df.Genotype == 'L109R').to_numpy() * 1
        self.unipol = df.UniPol.tolist()
        self.p0 = p0
        self.fix_wt = fix_wt
        self.fix_mut = fix_mut
        self.fit_D = fit_D

        # Model
        if self.log:
            if self.fit_D:
                self.model = model_log_paired_D
            else:
                self.model = model_log_paired
        else:
            self.model = model_paired

        # Output
        self.res_x = [None, None]
        self.res_y = [None, None]
        self.wd_full = [None, None]
        self.wm_full = None
        self.wds = [None, None]
        self.wms = None
        self.all_fits_lower = [None, None]
        self.all_fits_upper = [None, None]
        self.cyt_dim = [None, None]
        self.mem_dim = [None, None]
        self.cyt_dim_lower = [None, None]
        self.cyt_dim_upper = [None, None]
        self.mem_dim_lower = [None, None]
        self.mem_dim_upper = [None, None]

        # Run
        self.run()

    def run(self, n_bootstrap=1000, n_x=100, interval=95):

        # Analysing full dataset
        popt_full = self.single_fit([self.cyts, self.l109r], self.mems)
        self.res_x = [np.linspace(np.min(self.cyts[self.l109r == 0]), np.max(self.cyts[self.l109r == 0]), n_x),
                      np.linspace(np.min(self.cyts[self.l109r == 1]), np.max(self.cyts[self.l109r == 1]), n_x)]
        self.res_y[0] = self.model([self.res_x[0], np.zeros(len(self.res_x[0]))], *popt_full)
        self.res_y[1] = self.model([self.res_x[1], np.ones(len(self.res_x[1]))], *popt_full)
        self.wd_full = [popt_full[0], popt_full[1]]
        self.wm_full = popt_full[2]
        if self.fit_D:
            print(popt_full[3])
        if self.log:
            self.cyt_dim[0] = 100 * dimer_fraction(10 ** self.res_x[0], self.wd_full[0])
            self.mem_dim[0] = 100 * dimer_fraction(10 ** self.res_y[0], self.wd_full[0])
            self.cyt_dim[1] = 100 * dimer_fraction(10 ** self.res_x[1], self.wd_full[1])
            self.mem_dim[1] = 100 * dimer_fraction(10 ** self.res_y[1], self.wd_full[1])
        else:
            self.cyt_dim[0] = 100 * dimer_fraction(self.res_x[0], self.wd_full[0])
            self.mem_dim[0] = 100 * dimer_fraction(self.res_y[0], self.wd_full[0])
            self.cyt_dim[1] = 100 * dimer_fraction(self.res_x[1], self.wd_full[1])
            self.mem_dim[1] = 100 * dimer_fraction(self.res_y[1], self.wd_full[1])

        # Bootstrapping
        params = self.bootstrap_fitting([self.cyts, self.l109r], self.mems)
        self.wds = [params[:, 0], params[:, 1]]
        self.wms = params[:, 2]

        # Confidence interval
        all_fits0 = np.zeros([n_bootstrap, n_x])
        all_cyt_dim0 = np.zeros([n_bootstrap, n_x])
        all_mem_dim0 = np.zeros([n_bootstrap, n_x])
        for i, p in enumerate(params):
            all_fits0[i, :] = self.model([self.res_x[0], np.zeros(len(self.res_x[0]))], *p)
            if self.log:
                all_cyt_dim0[i, :] = 100 * dimer_fraction(10 ** self.res_x[0], p[0])
                all_mem_dim0[i, :] = 100 * dimer_fraction(10 ** self.res_y[0], p[0])
            else:
                all_cyt_dim0[i, :] = 100 * dimer_fraction(self.res_x[0], p[0])
                all_mem_dim0[i, :] = 100 * dimer_fraction(self.res_y[0], p[0])
        self.all_fits_lower[0] = np.percentile(all_fits0, (100 - interval) / 2, axis=0)
        self.all_fits_upper[0] = np.percentile(all_fits0, 50 + (interval / 2), axis=0)
        self.cyt_dim_lower[0] = np.percentile(all_cyt_dim0, (100 - interval) / 2, axis=0)
        self.cyt_dim_upper[0] = np.percentile(all_cyt_dim0, 50 + (interval / 2), axis=0)
        self.mem_dim_lower[0] = np.percentile(all_mem_dim0, (100 - interval) / 2, axis=0)
        self.mem_dim_upper[0] = np.percentile(all_mem_dim0, 50 + (interval / 2), axis=0)

        all_fits1 = np.zeros([n_bootstrap, n_x])
        all_cyt_dim1 = np.zeros([n_bootstrap, n_x])
        all_mem_dim1 = np.zeros([n_bootstrap, n_x])
        for i, p in enumerate(params):
            all_fits1[i, :] = self.model([self.res_x[1], np.ones(len(self.res_x[1]))], *p)
            if self.log:
                all_cyt_dim1[i, :] = 100 * dimer_fraction(10 ** self.res_x[1], p[1])
                all_mem_dim1[i, :] = 100 * dimer_fraction(10 ** self.res_y[1], p[1])
            else:
                all_cyt_dim1[i, :] = 100 * dimer_fraction(self.res_x[1], p[1])
                all_mem_dim1[i, :] = 100 * dimer_fraction(self.res_y[1], p[1])
        self.all_fits_lower[1] = np.percentile(all_fits1, (100 - interval) / 2, axis=0)
        self.all_fits_upper[1] = np.percentile(all_fits1, 50 + (interval / 2), axis=0)
        self.cyt_dim_lower[1] = np.percentile(all_cyt_dim1, (100 - interval) / 2, axis=0)
        self.cyt_dim_upper[1] = np.percentile(all_cyt_dim1, 50 + (interval / 2), axis=0)
        self.mem_dim_lower[1] = np.percentile(all_mem_dim1, (100 - interval) / 2, axis=0)
        self.mem_dim_upper[1] = np.percentile(all_mem_dim1, 50 + (interval / 2), axis=0)

    def single_fit(self, cyt_l109r, mem):

        if not self.fit_D:
            bounds = [[-np.inf, -np.inf, -np.inf], [np.inf, np.inf, np.inf]]
            epsilon = 0.00000001
            if self.fix_wt:
                bounds[0][0], bounds[1][0] = self.p0[0] - epsilon, self.p0[0] + epsilon
            if self.fix_mut:
                bounds[0][1], bounds[1][1] = self.p0[1] - epsilon, self.p0[1] + epsilon
            p0 = self.p0
        else:
            bounds = [[-np.inf, -np.inf, -np.inf, -np.inf], [np.inf, np.inf, np.inf, np.inf]]
            epsilon = 0.00000001
            if self.fix_wt:
                bounds[0][0], bounds[1][0] = self.p0[0] - epsilon, self.p0[0] + epsilon
            if self.fix_mut:
                bounds[0][1], bounds[1][1] = self.p0[1] - epsilon, self.p0[1] + epsilon
            p0 = list(self.p0)
            p0.append(0)

        popt, pcov = curve_fit(self.model, np.array(cyt_l109r), mem, maxfev=10000000, p0=p0, bounds=bounds)
        params = popt
        return params

    def bootstrap_fitting(self, cyts_l109r, mems, n=1000):
        cyts, l109r = cyts_l109r
        if not self.fit_D:
            params = np.zeros([n, 3])
        else:
            params = np.zeros([n, 4])
        for i in range(n):
            # Bootstrap 1
            __cyts = cyts[l109r == 0]
            __mems = mems[l109r == 0]
            inds = np.random.choice(range(len(__cyts)), len(__cyts))
            _cyts1 = __cyts[inds]
            _mems1 = __mems[inds]

            # Bootstrap 2
            __cyts = cyts[l109r == 1]
            __mems = mems[l109r == 1]
            inds = np.random.choice(range(len(__cyts)), len(__cyts))
            _cyts2 = __cyts[inds]
            _mems2 = __mems[inds]

            # Compile
            _cyts = np.r_[_cyts1, _cyts2]
            _mems = np.r_[_mems1, _mems2]
            _l109r = np.r_[np.zeros(len(_cyts1)), np.ones(len(_cyts2))]

            # Fitting
            params[i, :] = self.single_fit([_cyts, _l109r], _mems)
        return params