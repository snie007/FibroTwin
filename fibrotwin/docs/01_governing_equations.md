# 01 — Governing Equations (Updated)

## 1) Large-deformation mechanics (Ogden myocardium)
We solve quasi-static equilibrium on \(\Omega_0\):
\[
\nabla_0 \cdot \mathbf P = \mathbf 0
\]
with displacement BCs (left edge fixed, right edge stretched).

Kinematics:
\[
\mathbf F = \frac{\partial \mathbf x}{\partial \mathbf X},\quad J=\det\mathbf F,\quad \mathbf C=\mathbf F^T\mathbf F
\]

For MVP large deformation, myocardium uses compressible Ogden energy (single term):
\[
W(\mathbf F)=\frac{\mu}{\alpha}\left(\lambda_1^{\alpha}+\lambda_2^{\alpha}+\lambda_3^{\alpha}-3\right)+\frac{\kappa}{2}(J-1)^2
\]
with principal stretches \(\lambda_i\). In current 2D implementation, \(\lambda_3=1\) (plane-strain proxy).

Total potential (no body-force term in MVP):
\[
\Pi(\mathbf u)=\int_{\Omega_0}W(\mathbf F(\mathbf u))\,dV
\]
Numerical solve minimizes \(\Pi\) with Dirichlet constraints.

## Weak form (summary)
Find \(\mathbf u\in\mathcal V\) such that:
\[
\delta \Pi = \int_{\Omega_0}\mathbf P: \delta \mathbf F\,dV = 0\quad \forall\,\delta\mathbf u\in\mathcal V_0
\]
where \(\mathbf P=\partial W/\partial \mathbf F\).

## 2) Fibre reorientation law
Let \(m(x,t)\) be principal direction proxy from local strain:
\[
\tilde a^{n+1}=a^n + \frac{\Delta t}{\tau_a}(m^n-a^n),\qquad
a^{n+1}=\frac{\tilde a^{n+1}}{\|\tilde a^{n+1}\|+\epsilon}
\]

## 3) Cell motion model
For agent \(i\):
\[
v_i^{n+1}=\rho v_i^n + (1-\rho)\eta_i^n + \chi\nabla S(x_i^n),\qquad
x_i^{n+1}=x_i^n + \Delta t\,v_i^{n+1}
\]
with reflective boundaries.

## 4) Collagen deposition and degradation
\[
c^{n+1}(x)=c^n(x)+\Delta t\sum_{i=1}^{N_a}k_{dep}G_\sigma(x-x_i^n)-\Delta t\,k_{deg}c^n(x)
\]
\[
G_\sigma(r)=\exp\left(-\frac{\|r\|^2}{2\sigma^2}\right)
\]

## 5) Mixture/growth-inspired evolution
\[
g^{n+1}=g^n+\Delta t\left(k_g c^n-k_r g^n\right),\qquad g\ge 0
\]
This is constrained-mixture inspired (stress-free adaptation proxy), not yet a full constituent-specific turnover model.
