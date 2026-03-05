# 00 — Problem Statement

We model a 2D atrial tissue patch under over-stretch with coupled:
1. Quasi-static mechanics,
2. Fibroblast/myofibroblast agent motion,
3. Collagen deposition/remodelling,
4. Fibre reorientation.

## MVP goals
- Reproduce expected mechanobiology trend: sustained stretch increases alignment and collagen accumulation.
- Produce reproducible simulation outputs and animation from one command.
- Keep architecture extensible to 3D, nonlinear constitutive laws, and richer mixture theory.

## Domain and scales
- Spatial: rectangular 2D patch \(\Omega=[0,L_x]\times[0,L_y]\).
- Time: macro-steps \(t_n=n\Delta t\).
- Agents: fibroblasts (points) moving on \(\Omega\).
- Fields: displacement \(u\), collagen density \(c\), myofibre direction \(a\), collagen preferred direction \(a_c\), growth proxy \(g\).

## Coupling concept
At each macro step:
1. Build material state from \(c,a\) and growth proxy.
2. Solve mechanics under displacement BCs.
3. Move cells using persistent motion + taxis to mechanical cue.
4. Deposit collagen near cell positions; degrade globally.
5. Update fibre orientation toward principal stretch direction.
6. Update growth proxy from collagen/stress and proceed.
