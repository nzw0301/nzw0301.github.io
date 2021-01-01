---
layout: post
title: chi square divergence between two 1D Gaussians
comments: True
abstract: Calculation
lang: english
---

[Pearson $$\chi^2$$-divergence](https://en.wikipedia.org/wiki/F-divergence)[[^1]] is a divergence between two distributions. The $$\chi^2$$-divergence is defined as

$$
\begin{align}
    \chi^2(Q || P) &= \mathbb{E}_{h \sim P} \left( \frac{Q(h)}{P(h)} \right)^2 - 1 \tag{1} \\\\
    &= \int \frac{Q(h)^ 2}{P(h)} dh  - 1 \tag{2}.
\end{align} 
$$

In this post, I try to write an explicit form of $\chi^2$-divergence when $$Q$$ and $$P$$ are 1D normal distribution. More specifically, I assume that $$P$$ is the standard normal distribution $$P = \mathcal{N}(0, 1)$$, and $$Q$$ is a normal distribution $$Q = \mathcal{N}(\mu, \sigma)$$, where $$\sigma$$ is a variance parameter.

$$
\begin{align}
    \chi^2(Q || P) + 1 
        &= \int \frac{Q(h)^2}{P(h)} dx \tag{3} \\\\
        &= \int \frac{\mathcal{Q}(x; \mu, \sigma)^2}{\mathcal{N}(x; 0, 1) } dx \\\\
        &= \int \frac{ \left(
            \frac{1}{\sqrt{2 \pi \sigma}} \exp \left( - \frac{(x-\mu)^2}{2 \sigma} \right)
            \right) ^2}{ 
            \frac{1}{\sqrt{2 \pi}} \exp \left( - \frac{x^2}{2} \right)
         } dx \\\\
         &= \frac{\sqrt{2 \pi}}{2 \pi \sigma} \int 
            \exp \left(- \frac{(x-\mu)^2}{\sigma} + \frac{x^2}{2}\right)
            dx \\\\
        &= \frac{\sqrt{2 \pi}}{2 \pi \sigma} \int 
            \exp \left(- \frac{1}{\sigma} \left(x^2- 2 x \mu + \mu^2 \right)  + \frac{x^2}{2}\right)
            dx \\\\            
\end{align} 
$$



[^1]: This divergence can be derived from $$f$$-divergence, which is a more general divergence.