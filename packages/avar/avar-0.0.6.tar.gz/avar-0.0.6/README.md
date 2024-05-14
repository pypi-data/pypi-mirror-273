# Allan Variance Tools

## Array of Windows

```python
avar.windows(K, density=64)
```

This will create an array `M` of integer window sizes. The averaging period
`tau` would equal `M*T`, where `T` is the sampling period. The `density` is the
target number of window sizes in the array per decade. Obviously, in the first
decade it is not possible to have more than 9 window sizes: 1 through 9.

## Signal Allan Variance

```python
avar.variance(y, M)
```

To get the actual Allan variance of a signal `y`, use this function. You must
supply the array of window sizes `M` for which to calculate the Allan variance
values. This function can take for `y` either a one-dimensional array or a
two-dimensional array in which each row will be treated as a data set.

## Ideal Allan Variance

```python
avar.ideal(tau, p)
```

The `ideal` function will calculate the ideal Allan variances over an array of
averaging periods `tau`. For any noise components you wish not to be included,
set their corresponding variances to zero.

This function make use of the `params` class. Objects of this type store the
five basic component noise variances (quantization, white, flicker, walk, and
ramp), `vc`, any first-order, Gauss-Markov (FOGM) noise variances, `vfogm`, and
the corresponding FOGM time constants, `tfogm`. The `p` parameter is one such
object. You can define it as shown in the following example:

```python
p = avar.params(
        vc=np.array([0.5, 1.0, 0, 0.5, 0.1]) * 1e-9,
        vfogm=[1e-8, 1e-7],
        tfogm=[0.1, 1.0])
```

The `ideal` function will return the total Allan variance curve, `va`, as well
as a matrix, `vac`, whose rows represent the component Allan variances over
`tau`.

## Fitting to Signal Allan Variance

```python
avar.fit(tau, va, mask=None, fogms=0, tol=0.007)
```

Given the Allan variance curve of some signal, `va`, at various averaging
periods `tau`, you can get the best fit using the five basic component noises
and `fogms` number of first-order, Gauss-Markov (FOGM) noises. By default, this
function will automatically attempt to determine if certain component noises are
even at play based on the tolerance value `tol`. However, you can directly
control which component noises you wish to include or exclude with the `mask`
array. For each element of `mask` that is `False` the corresponding component
noise will be excluded. This function will iterate through the various
permutations of component noises, starting with 0 FOGMs. If a fit satisfies the
specified `tol` tolerance, the search will end. Otherwise, the best fit will be
used.

The return values are the fitted Allan variance curve, `vf`, and a `params`
object, `p` (see the section on Ideal Allan Variance), containing the variances
of the basic component noise variances (quantization, white, flicker, walk, and
ramp), `vc`, any first-order, Gauss-Markov (FOGM) noise variances, `vfogm`, and
the corresponding FOGM time constants, `tfogm`.

## Noise Generation

```python
avar.noise(K, T, p)
```

Generate a noise signal of length `K`, sampling period `T`, and parameters `p`.
Parameter `p` is a `params` object (see the section on Ideal Allan Variance).

This function returns the noise signal `y`.
