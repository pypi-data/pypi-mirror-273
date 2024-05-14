import time
import numpy as np
import avar
import itrm

# Build time.
T = 0.01
t_dur = 200.0
t = np.arange(0, t_dur, T)
K = len(t)

# Constants
J = 100
p = avar.params(
        vc=np.zeros(5), # np.array([0.5, 1.0, 0, 0.5, 0.1]) * 1e-9,
        vfogm=[1e-8, 1e-7], # 7.85e-9
        tfogm=[0.1, 1.0]) # 0.5305

# Get mean Allan variance from Monte-Carlo noise.
M = avar.windows(K)
tau = M*T
va_real = np.zeros(len(M))
tic = time.perf_counter()
for j in range(J):
    y = avar.noise(K, T, p)
    va_real += avar.variance(y, M)/J
    itrm.progress(j, J, tic)

# Get the ideal and fitted Allan variances.
va_ideal, _ = avar.ideal(tau, p)
va_fit, p_fit = avar.fit(tau, va_ideal, fogms=2)

print("vc:", p.vc)
print("vc fit:", p_fit.vc)
print("v FOGM:", p.vfogm)
print("v FOGM fit:", p_fit.vfogm)
print("tau FOGM:", p.tfogm)
print("tau FOGM fit:", p_fit.tfogm)

# Show the results.
y = np.array([va_ideal, va_fit, va_real])
itrm.iplot(tau, y, label="Allan variance", rows=0.5, lg="xy")
y = np.array([
        avar.fit_metrics.nmae,
        avar.fit_metrics.mask,
        avar.fit_metrics.fogm])
itrm.iplot(y, rows=0.5, label="metrics")
