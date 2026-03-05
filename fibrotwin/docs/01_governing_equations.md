# 01 — Governing Equations

## 1) Mechanics
For MVP, small-strain quasi-static linear elasticity on \(\Omega\):
\[
\nabla\cdot\sigma = 0
\]
with prescribed displacement BCs (left clamped, right stretched in \(x\), top/bottom traction-free).

Kinematics:
\[
\varepsilon(u)=\frac{1}{2}(\nabla u + \nabla u^T)
\]

Constitutive law (plane stress/strain):
\[
\sigma = C(c,a) : \varepsilon
\]
Base isotropic matrix: \(C_0(E,\nu)\). We modulate stiffness by collagen fraction:
\[
E_{\text{eff}}(x,t)=E_0\,(1+\alpha_c\,c(x,t))
\]
and add weak fibre anisotropy via directional projector term:
\[
\sigma_{aniso} = k_f\,c\,(a\otimes a):\varepsilon\;(a\otimes a)
\]
(implemented as a simplified additive term in element stiffness evaluation).

## 2) Fibre reorientation law
Let \(m(x,t)\) be principal stretch/eigenvector proxy from local strain tensor.
Discrete-time update:
\[
\tilde a^{n+1}=a^n + \frac{\Delta t}{\tau_a}(m^n-a^n),\qquad
a^{n+1}=\frac{\tilde a^{n+1}}{\|\tilde a^{n+1}\|+\epsilon}
\]
Similarly for collagen orientation \(a_c\) with optional slower time constant.

## 3) Cell motion model
For agent \(i\) at \(x_i\):
\[
v_i^{n+1}=\rho v_i^n + (1-\rho)\,\eta_i^n + \chi\nabla S(x_i^n)
\]
\[
x_i^{n+1}=x_i^n + \Delta t\,v_i^{n+1}
\]
where:
- \(\eta_i^n\sim\mathcal N(0,\sigma_v^2 I)\),
- \(S\): mechanical cue (strain energy proxy),
- \(\chi\): taxis gain,
- reflective boundaries enforce \(x_i\in\Omega\).

## 4) Collagen deposition and degradation
Field equation (operator-split discrete form):
\[
c^{n+1}(x)=c^n(x)+\Delta t\sum_{i=1}^{N_a}k_{dep}\,G_\sigma(x-x_i^n)-\Delta t\,k_{deg}\,c^n(x)
\]
with Gaussian kernel
\[
G_\sigma(r)=\exp\left(-\frac{\|r\|^2}{2\sigma^2}\right)
\]
(normalized numerically in code).

## 5) Mixture/growth-inspired evolution
Use a simplified growth proxy \(g(x,t)\) representing stress-free adaptation:
\[
g^{n+1}=g^n+\Delta t\left(k_g c^n - k_r g^n\right)
\]
Mechanically, \(g\) softens effective strain load or modifies effective stiffness map (MVP implementation uses stiffness modulation):
\[
E_{\text{eff}} \leftarrow E_{\text{eff}}\,(1+\beta_g g)
\]

This approximates multiplicative growth ideas (\(F=F_eF_g\)) while keeping linear FEM MVP stable.
