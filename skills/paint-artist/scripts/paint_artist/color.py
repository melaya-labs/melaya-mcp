"""Colour maths: sRGB <-> CIELAB (D65), weighted k-means in Lab, palette helpers, prefilters.
All images are float arrays in 0..1, shape (..., 3)."""
import numpy as np

_M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
_WP = np.array([0.95047, 1.0, 1.08883])


def srgb_to_linear(c):
    return np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)


def linear_to_srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c > 0.0031308, 1.055 * c ** (1 / 2.4) - 0.055, 12.92 * c)


def rgb2lab(im):
    im = np.asarray(im, float)
    xyz = srgb_to_linear(im) @ _M.T / _WP
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def lab2rgb(lab):
    lab = np.asarray(lab, float)
    fy = (lab[..., 0] + 16) / 116
    fx, fz = fy + lab[..., 1] / 500, fy - lab[..., 2] / 200
    f = np.stack([fx, fy, fz], -1)
    xyz = np.where(f > 0.206893, f ** 3, (f - 16 / 116) / 7.787) * _WP
    return np.clip(linear_to_srgb(xyz @ np.linalg.inv(_M).T), 0, 1)


def delta_e(a, b):
    """Mean CIE76 dE between two RGB images (0..1)."""
    return float(np.mean(np.linalg.norm(rgb2lab(a) - rgb2lab(b), axis=-1)))


def kmeans_lab(lab, k, weights=None, iters=25, seed=0, sample=60000):
    """Weighted k-means (k-means++ init) on Lab points (N,3). Returns centres (k,3) and labels (N,)."""
    rng = np.random.default_rng(seed)
    X = lab.reshape(-1, 3)
    w = np.ones(len(X)) if weights is None else np.asarray(weights, float).reshape(-1)
    if len(X) > sample:
        idx = rng.choice(len(X), sample, replace=False, p=w / w.sum())
        Xs, ws = X[idx], np.ones(sample)
    else:
        Xs, ws = X, w
    k = min(k, len(Xs))
    C = [Xs[rng.choice(len(Xs), p=ws / ws.sum())]]
    d2 = ((Xs - C[0]) ** 2).sum(1)
    for _ in range(1, k):
        p = d2 * ws
        C.append(Xs[rng.choice(len(Xs), p=p / p.sum())] if p.sum() > 0 else Xs[rng.integers(len(Xs))])
        d2 = np.minimum(d2, ((Xs - C[-1]) ** 2).sum(1))
    C = np.array(C)
    for _ in range(iters):
        lbl = assign(Xs, C)
        newC = C.copy()
        for j in range(k):
            m = lbl == j
            if m.any():
                newC[j] = np.average(Xs[m], axis=0, weights=ws[m])
        if np.allclose(newC, C, atol=1e-3):
            C = newC
            break
        C = newC
    return C, assign(X, C)


def assign(X, C, chunk=200000):
    out = np.empty(len(X), int)
    for i in range(0, len(X), chunk):
        out[i:i + chunk] = ((X[i:i + chunk, None, :] - C[None]) ** 2).sum(-1).argmin(1)
    return out


def nearest(lab, pal_lab):
    """Index of the nearest palette colour for Lab values of any leading shape."""
    lab = np.asarray(lab, float)
    return assign(lab.reshape(-1, 3), pal_lab).reshape(lab.shape[:-1])


def adjust(im, saturation=1.0, contrast=1.0, gamma=1.0, brightness=0.0):
    """Prefilter in Lab: chroma scale, L contrast around 50, gamma on L, brightness offset (L units)."""
    if saturation == 1 and contrast == 1 and gamma == 1 and brightness == 0:
        return im
    lab = rgb2lab(im)
    L = lab[..., 0] / 100
    L = L ** gamma
    L = (L - 0.5) * contrast + 0.5
    lab[..., 0] = np.clip(L * 100 + brightness, 0, 100)
    lab[..., 1:] *= saturation
    return lab2rgb(lab)


def reinhard_transfer(src, ref):
    """Match Lab mean and std of src to ref (colour mood transfer for style reproduction)."""
    a, b = rgb2lab(src), rgb2lab(ref).reshape(-1, 3)
    mu_a, sd_a = a.reshape(-1, 3).mean(0), a.reshape(-1, 3).std(0) + 1e-6
    mu_b, sd_b = b.mean(0), b.std(0) + 1e-6
    return lab2rgb((a - mu_a) / sd_a * sd_b + mu_b)


def snap_palette(pal, targets, amount=0.7):
    """Pull each palette colour toward its nearest colour in `targets` (Lab mix), e.g. a period palette."""
    pl, tl = rgb2lab(pal), rgb2lab(np.asarray(targets, float))
    j = nearest(pl, tl)
    return lab2rgb((1 - amount) * pl + amount * tl[j])


def hex2rgb(h):
    h = h.lstrip('#')
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def as_rgb(c):
    """Accept '#rrggbb', [r,g,b] in 0..255 or 0..1."""
    if isinstance(c, str):
        return np.array(hex2rgb(c))
    c = np.asarray(c, float)
    return c / 255 if c.max() > 1 else c
