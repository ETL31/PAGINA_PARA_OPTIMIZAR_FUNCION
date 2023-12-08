#NOMBRE: ERNESTO MIHAEL TOLENTINO LEÓN - 16140258

import sympy as sp
from scipy.optimize import minimize

# Definir variables simbólicas
x, y = sp.symbols('x y')

# Pedir al usuario que ingrese la función
expression_str = input("Ingrese la función f(x, y): ")
expression = sp.sympify(expression_str)

# Derivar la función con respecto a x e y
derivative_x = sp.diff(expression, x)
derivative_y = sp.diff(expression, y)

# Mostrar las derivadas
print(f"Derivada con respecto a x: {derivative_x}")
print(f"Derivada con respecto a y: {derivative_y}")

# Encontrar los puntos críticos (donde las derivadas son cero)
critical_points = sp.solve([derivative_x, derivative_y], (x, y))

# Mostrar las derivadas y los puntos críticos
print(f"Derivada con respecto a x: {derivative_x}")
print(f"Derivada con respecto a y: {derivative_y}")
print(f"Puntos Críticos: {critical_points}")

# Calcular las segundas derivadas (Hessiana)
second_derivative_xx = sp.diff(derivative_x, x)
second_derivative_xy = sp.diff(derivative_x, y)
second_derivative_yy = sp.diff(derivative_y, y)

# Construir la matriz Hessiana
hessian_matrix = sp.Matrix([[second_derivative_xx, second_derivative_xy],
                            [second_derivative_xy, second_derivative_yy]])

# Calcular el determinante de la matriz Hessiana
determinant_hessian = hessian_matrix.det()

# Evaluar cada punto crítico en el determinante de la Hessiana y mostrar el valor numérico
evaluations = {}
for point in critical_points:
    x_val, y_val = point
    determinant_value_numeric = determinant_hessian.subs({x: x_val, y: y_val})
    
    # Redondear solo si es necesario
    if '.' in str(determinant_value_numeric):
        determinant_value_numeric = round(determinant_value_numeric, 3)
    
    evaluations[point] = determinant_value_numeric

# Clasificar los puntos críticos
classification = {}
for point in critical_points:
    x_val, y_val = point
    hessian_eval = hessian_matrix.subs({x: x_val, y: y_val})
    eigenvalues = hessian_eval.eigenvals()
    
    determinant_value = determinant_hessian.subs({x: x_val, y: y_val})
    f_xx_value = second_derivative_xx.subs({x: x_val, y: y_val})
    
    if determinant_value > 0:
        if f_xx_value > 0:
            classification[point] = "Mínimo Relativo"
        elif f_xx_value < 0:
            classification[point] = "Máximo Relativo"
        else:
            classification[point] = "Indeterminado"
    elif determinant_value < 0:
        classification[point] = "Punto de Silla"
    else:
        classification[point] = "Indeterminado"

# Encontrar los puntos de máximo y mínimo relativos
max_min_points = {point: classification[point] for point in classification if classification[point] in ["Máximo Relativo", "Mínimo Relativo"]}

# Evaluar la función en los puntos de máximo y mínimo relativos
function_values = {}
for point, value in max_min_points.items():
    x_val, y_val = point
    function_value = expression.subs({x: x_val, y: y_val})
    function_values[point] = function_value



# Mostrar los resultados

print(f"Matriz Hessiana:\n{hessian_matrix}")

print(f"Determinante de la Hessiana (por cálculo directo): {determinant_hessian}")

print("\nEvaluaciones Numéricas en los Puntos Críticos:")
for point, value in evaluations.items():
    print(f"Punto Crítico: {point}, Valor Numérico del Determinante: {value}")

print("\nClasificación de Puntos Críticos:")
for point, value in classification.items():
    print(f"Punto Crítico: {point}, Clasificación: {value}")

# Encontrar el mínimo y máximo relativo
min_point = min(function_values, key=function_values.get)
max_point = max(function_values, key=function_values.get)

print("\nDetalles de Mínimo y Máximo Relativo:")
if min_point:
    print(f"La función alcanza su mínimo relativo en el punto {min_point} con un valor de {function_values[min_point]}")
else:
    print("La función no tiene mínimo relativo.")

if max_point:
    print(f"La función alcanza su máximo relativo en el punto {max_point} con un valor de {function_values[max_point]}")
else:
    print("La función no tiene máximo relativo.")