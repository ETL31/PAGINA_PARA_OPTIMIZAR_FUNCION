import sympy as sp
from scipy.optimize import minimize

# Definir variables simbólicas
x, y, lambda_ = sp.symbols('x y lambda')

# Pedir al usuario que ingrese la función objetivo f(x, y)
expression_str = input("Ingrese la función objetivo f(x, y): ")
expression = sp.sympify(expression_str)

# Pedir al usuario que ingrese la función de restricción g(x, y)
constraint_str = input("Ingrese la función de restricción g(x, y): ")
constraint = sp.sympify(constraint_str)

# Construir la función Lagrangiana
lagrangian = expression - lambda_ * constraint

# Calcular las derivadas parciales con respecto a x, y y lambda
derivative_x = sp.diff(lagrangian, x)
derivative_y = sp.diff(lagrangian, y)
derivative_lambda = sp.diff(lagrangian, lambda_)

# Resolver el sistema de ecuaciones para encontrar los puntos críticos
critical_points = sp.solve([derivative_x, derivative_y, derivative_lambda], (x, y, lambda_))

# Filtrar los puntos que satisfacen la restricción g(x, y) = 0
valid_points = [point for point in critical_points if constraint.subs({x: point[0], y: point[1]}) == 0]

# Construir la matriz Hessiana orlada
hessian_orlada = sp.Matrix([
    [0, -sp.diff(constraint, x), -sp.diff(constraint, y)],
    [-sp.diff(constraint, x), sp.diff(derivative_x, x), sp.diff(derivative_x, y)],
    [-sp.diff(constraint, y), sp.diff(derivative_y, x), sp.diff(derivative_y, y)]
])

# Evaluar cada punto crítico en la matriz Hessiana Orlada
hessian_values = {}
for point in valid_points:
    hessian_value = hessian_orlada.subs({x: point[0], y: point[1], lambda_: point[2]})
    hessian_values[point] = hessian_value

# Evaluar la determinante de cada matriz Hessiana Orlada en los puntos críticos
determinant_values = {}
for point in valid_points:
    determinant_value = hessian_orlada.det().subs({x: point[0], y: point[1], lambda_: point[2]})
    determinant_values[point] = determinant_value
    
function_values = {}
for point in valid_points:
    function_value = expression.subs({x: point[0], y: point[1]})
    function_values[point] = function_value

# Mostrar los resultados

print("\nResultados:")

print(f"Puntos críticos válidos: {valid_points}")

print("\nMatriz Hessiana Orlada:")

print(hessian_orlada)

print("\nValores de la Matriz Hessiana Orlada en Puntos Críticos:")
for point, value in hessian_values.items():
    print(f"Punto Crítico: {point}, Valor de la Matriz Hessiana Orlada:\n{value}")

print("\nValores de la Determinante de la Matriz Hessiana Orlada en Puntos Críticos:")
for point, value in determinant_values.items():
    print(f"Punto Crítico: {point}, Determinante de la Matriz Hessiana Orlada: {value}")

print("\nValores de la Función y Determinante de la Matriz Hessiana Orlada en Puntos Críticos:")
for point in valid_points:
    determinant_value = determinant_values[point]
    function_value = function_values[point]
    print(f"Punto Crítico: {point}, Valor de la Función: {function_value}, Determinante de la Matriz Hessiana Orlada: {determinant_value}")

print("\nResultados sobre Mínimo y Máximo Relativo:")
for point in valid_points:
    determinant_value = determinant_values[point]
    function_value = function_values[point]

    if determinant_value < 0:
        print(f"En el punto {point}, la función tiene un Mínimo Relativo con un valor de {function_value}.")
    elif determinant_value > 0:
        print(f"En el punto {point}, la función tiene un Máximo Relativo con un valor de {function_value}.")
    else:
        print(f"En el punto {point}, la determinante de la Matriz Hessiana Orlada es cero, no se puede determinar si es un mínimo o máximo relativo.")

