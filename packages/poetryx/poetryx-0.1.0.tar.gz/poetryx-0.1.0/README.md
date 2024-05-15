# Poetry Extended (Poetryx)

<p align="center">
  <img src="https://raw.githubusercontent.com/nachatz/poetryx/master/docs/img/poetryx.jpg">
</p>

<p align="center">
Augmenting the flow of functionality for Poetry projects, setup, and debugging. Enabling streamlined user experience within specific IDEs, scaffolding projects, and generic utilities.
</p>

<div align="center">

[![v0.1.0](https://img.shields.io/badge/version-v0.0.2-blue.svg)](https://github.com/nachatz/poetryx)
[![Test](https://github.com/nachatz/poetryx/actions/workflows/validate.yaml/badge.svg)](https://github.com/nachatz/poetryx/actions/workflows/validate.yaml)
[![License](https://img.shields.io/badge/license-Apache%202-brightgreen.svg)](https://github.com/nachatz/poetryx/blob/master/LICENSE.txt)

</div>

---

&nbsp; 
## Getting started

This CLI is built on-top of Poetry, so likely you have already downloaded Poetry. If not, you can install [here](https://python-poetry.org/docs/):

1. Install Poetryx

```shell 
pip install poetryx
```
2. Configure Poetryx for your IDE

```shell
poetryx configure
```

&nbsp; 
## Provided utilities 

### IDE configuration (**currently only VSCode**) - `poetryx configure`

Configure VScode to use the current poetry environments for debugging and interpreting. Enabling immediate debugging through the `Testing` extension