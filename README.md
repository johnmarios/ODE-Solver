# ODE Solver using Euler and Runge-Kutta Methods

A Python application for numerically solving Ordinary Differential Equations (ODEs) using classical numerical methods, including Euler, Runge-Kutta 2nd Order (RK2), and Runge-Kutta 4th Order (RK4).

The project also includes a graphical user interface built with Tkinter and symbolic expression parsing using SymPy.

---

## Features

* Numerical solution of first-order differential equations
* Euler Method implementation
* Runge-Kutta 2nd Order (RK2) implementation
* Runge-Kutta 4th Order (RK4) implementation
* User-defined differential equations
* Symbolic mathematical expression parsing
* GUI-based method selection
* Step-size comparison and basic error control
* Support for predefined test problems

---

## Technologies Used

* Python
* Tkinter
* SymPy
* Numerical Methods
* Scientific Computing

---

## Example Differential Equation

```python
-100*y + 5*(x**(3/2))*(1 + 40*x)
```

---

## How It Works

The user can:

1. Enter a differential equation
2. Define the step size `h`
3. Set initial conditions
4. Select a numerical method from the GUI

The application then computes approximate numerical solutions and prints the results.

---

## Implemented Numerical Methods

### Euler Method

A first-order numerical procedure for solving ordinary differential equations.

### Runge-Kutta 2nd Order (RK2)

Improved accuracy compared to Euler by evaluating intermediate slopes.

### Runge-Kutta 4th Order (RK4)

A widely used higher-order numerical method providing significantly better precision.

---

## Running the Project

Install dependencies:

```bash
pip install sympy
```

Run the application:

```bash
python main.py
```

---

## Educational Purpose

This project was developed for educational purposes as part of coursework related to numerical analysis and scientific computing.

It demonstrates:

* numerical approximation techniques,
* algorithm implementation,
* symbolic computation,
* and GUI development in Python.
