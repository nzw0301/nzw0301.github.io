---
layout: post
title: Derivation of KL divergence by Bregman divergence
comments: True
abstract: Calculation
lang: english
---

[Bregman divergence](https://en.wikipedia.org/wiki/Bregman_divergence) is a general class to measure "difference" between two data points.
For instance, Euclidean distance and Kullback Leibler (KL) divergence are instances of Bregman divergence.
In this post, I derive KL divergence from Bregman divergence formulation (for myself).

Bregman divergence is defined by the equation below:

$$
    \mathfrak{B}_{F}(x, y) = F(x) - F(y) - \langle F'(y), x-y \rangle,
$$

where $$\langle \cdot, \cdot \rangle$$ means inner product. When $$F(p) = \sum_i p_i \log(p_i)$$, this Bregman divergence is equivalent to KL divergence.

$$
\begin{aligned}
\mathfrak{B}_{F}(p, q)
                &= \sum_i (p_i \log(p_i)) - \sum_i (q_i \log(q_i)) - \langle  \log(q) + \mathbf{1} ,  p-q \rangle \\
                &= \sum_i (p_i \log(p_i))
                      - \sum_i p_i \log (q_i) - \sum_i p_i + \sum_i q_i \\
                &= \sum_i p_i \log \frac{p_i}{q_i} \\
                &= \mathrm{KL}[p || q].
\end{aligned}
$$

From Line 2 to Line 3, $$\sum_i p_i = \sum_i q_i = 1$$ since $$p$$ is a probability distribution.

### Reference

[This blog post](http://mark.reid.name/blog/meet-the-bregman-divergences.html) explains Bregman divergence in detail and gives useful links.
