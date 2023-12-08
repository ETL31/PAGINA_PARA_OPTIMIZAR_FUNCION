from flask import Flask, request, jsonify
from sympy import symbols, diff, solve, Matrix, sympify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)



class CoefficientsInput:
    coefficients: list

@app.route('/', methods=['POST'])
def find_critical_points():
    try:
        data = request.get_json()
        expresion_usuario = data.get('funcion')
        
        print(expresion_usuario)
        cubic_function_string = expresion_usuario
        x, y = symbols('x y')
        partial_derivative_x = diff(expresion_usuario, x)
        partial_derivative_y = diff(expresion_usuario, y)

        critical_points = solve([partial_derivative_x, partial_derivative_y], [x, y])


        hessian_matrix = Matrix([[diff(partial_derivative_x, x), diff(partial_derivative_x, y)],
                                 [diff(partial_derivative_y, x), diff(partial_derivative_y, y)]])

        relative_extremes = []


        for point in critical_points:

            hessian_at_point = hessian_matrix.subs({x: point[0], y: point[1]})


            determinant = hessian_at_point.det()
            minor1 = hessian_at_point[0, 0]
            minor2 = hessian_at_point[1, 1]

            # Clasificar el punto crítico como máximo, mínimo o punto de silla
            if determinant > 0 and minor1 > 0:
                classification = "Mínimo"
            elif determinant > 0 and minor1 < 0:
                classification = "Máximo"
            else:
                classification = "Punto de silla"

            # Agregar la información del punto crítico clasificado a la lista
            relative_extremes.append({
                'point': (float(point[0]), float(point[1])),
                'classification': classification
            })

        response = {
            'critical_points': [],
            'cubic_function': cubic_function_string,
            'relative_extremes': relative_extremes
        }

        for point in critical_points:
            x_value, y_value = point
            if isinstance(x_value, int) and isinstance(y_value, int):
                response['critical_points'].append((float(x_value), float(y_value)))
            else:
                response['critical_points'].append((str(x_value), str(y_value)))

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/pregunta', methods=['POST'])
def pregunta():
    try:
        data = request.get_json()
        x, y, l= symbols('x y lambda')
        efe = data.get('efe')
        ge = data.get('ge')
        print("f: ", efe)
        print("g: ", ge)
        # Definir variables
        efe=eval(efe)
        ge=eval(ge)

        # Definir la función objetivo y la restricción

        # Construir la función Lagrangiana
        L = efe - l * ge

        print("L: ",L)
        print("g: ",ge)
        # Calcular la matriz hessiana de la Lagrangiana

        # Calcular el gradiente de la Lagrangiana
        grad_L = [diff(L, var) for var in (x, y, l)]

        # Calcular la matriz hessiana orlada
        hessian_orlada = Matrix([
            [0, -diff(ge, x), -diff(ge, y)],
            [-diff(ge, x), diff(diff(L,x), x), diff(diff(L,x), y)],
            [-diff(ge, y), diff(diff(L,y), x), diff(diff(L,y), y)]
        ])
        print("hessian_orlada",hessian_orlada)

        # Encontrar puntos críticos
        soluciones = solve(grad_L, (x, y, l))
        print("soluciones", soluciones)

        relative_extremes = []
        for point in soluciones:
            hessian_at_point = hessian_orlada.subs({x: point[0], y: point[1], l: point[2]})
            determinant = hessian_at_point.det()
            minor1 = hessian_at_point[0,  0]
            minor2 = hessian_at_point[1, 1]
            # Clasificar el punto crítico como máximo, mínimo o punto de silla
            if determinant > 0 and minor1 > 0:
                classification = "Mínimo"
            elif determinant > 0 and minor1 < 0:
                classification = "Máximo"
            else:
                classification = "Punto de silla"
            # Agregar la información del punto crítico clasificado a la lista
            relative_extremes.append({
                'point': (float(point[0]), float(point[1]),float(point[2])),
                'classification': classification
            })

        response = {
            'critical_points': [],
            'relative_extremes': relative_extremes
        }
        for point in soluciones:
            x_value, y_value, l_value = point
            if isinstance(x_value, int) and isinstance(y_value, int) and isinstance(l_value,int):
                response['critical_points'].append((float(x_value), float(y_value),float(l_value)))
            else:
                response['critical_points'].append((str(x_value), str(y_value),float(l_value)))

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8001)
