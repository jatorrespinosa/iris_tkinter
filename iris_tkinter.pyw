# --- Ejercicio GUI con ML - via ATOM - TorresEspinosa,JoseAntonio ---
import tkinter as tk
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,\
                                              NavigationToolbar2Tk
from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# ----------------------------------
# --- PREDICCION y ALGORIRTMO ML ---
# ----------------------------------
# Lectura datos
ml_df = pd.read_csv("iris.csv", sep=',', decimal='.')
# Mapeo de species en valores númericos
ml_df.species = ml_df.species.map({"setosa": 0,
                                   "versicolor": 1, "virginica": 2})
# Obtención de las matrices X e y
X = ml_df.drop("species", axis=1)
y = ml_df["species"]
# Predicción RandomForestClassifier, Train 75% y Test 25%
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
clf = RandomForestClassifier()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
# Obtención de la efectividad
acc = accuracy_score(y_test, y_pred)


# ----------------------------------
# ----- FUNCIONES DE VENTANAS ------
# ----------------------------------

# ---------------------------- CLOSERS ---------------------------------------
def closedata():
    datawin.destroy()  # Cierra ventana
    dataButton['state'] = tk.NORMAL  # Reactiva botón


def closesepal():
    sepalwin.destroy()  # Cierra ventana
    sepalButton['state'] = tk.NORMAL  # Reactiva botón


def closepetal():
    petalwin.destroy()  # Cierra ventana
    petalButton['state'] = tk.NORMAL  # Reactiva botón


# ------------------------------- DATA ---------------------------------------
def DataWindow():
    dataButton['state'] = tk.DISABLED  # Deshabilita botón para no crear más
    df = pd.read_csv("iris.csv", sep=',', decimal='.')
    global datawin  # Declaración global para poder cerrarla
    datawin = tk.Toplevel(root)  # Toplevel crea ventana extra
    datawin.resizable(0, 1)  # Redimensionable solo en vertical
    datawin.geometry("600x500")
    datawin.title("Iris Data")
    scroll = tk.Scrollbar(datawin, orient=tk.VERTICAL)
    scroll.pack(side="right", fill="y")  # Scrollbar a la drch. incluido
    table = tk.Text(datawin, bg="alice blue", padx=10, pady=5,
                    yscrollcommand=scroll.set)
    table.insert(tk.INSERT, df.to_string())  # Inserta datos en cuadro de texto
    table.configure(state="disabled")  # Deshabilita edición de texto
    table.pack(side="left", fill="both")
    scroll.config(command=table.yview)  # Habilita mover tabla con el scroll
    datawin.protocol("WM_DELETE_WINDOW", closedata)  # Al cerrar ventana llama
    datawin.mainloop()                               # a la función close


# -------------------------- SEPAL GRAPHIC -----------------------------------
def SepalWindow():
    sepalButton['state'] = tk.DISABLED
    global sepalwin
    sepalwin = tk.Toplevel(root)
    sepalwin.resizable(0, 0)
    sepalwin.title("Species based on their Sepal 'Length-Width'")
    df = pd.read_csv("iris.csv", sep=',', decimal='.')
    # Crea gráfica, sns.scatterplot es parecido a plr.scatter
    fig = sns.FacetGrid(df, hue="species", height=6.4)
    fig.map(sns.scatterplot, "sepal_length", "sepal_width").add_legend()
    figura = fig.fig  # Obtiene figura para canvas

    canvas = FigureCanvasTkAgg(figura, sepalwin)
    canvas.draw()
    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas, sepalwin)
    toolbar.update()
    canvas.get_tk_widget().pack()
    sepalwin.protocol("WM_DELETE_WINDOW", closesepal)  # Igual que anterior
    sepalwin.mainloop()


# -------------------------- PETAL GRAPHIC -----------------------------------
def PetalWindow():  # Igual que SepalWindow
    petalButton['state'] = tk.DISABLED
    global petalwin
    petalwin = tk.Toplevel(root)
    petalwin.resizable(0, 0)
    petalwin.title("Species based on their Petal 'Length-Width'")
    df = pd.read_csv("iris.csv", sep=',', decimal='.')
    # Crea gráfica
    fig = sns.FacetGrid(df, hue="species", height=6.4)
    fig.map(sns.scatterplot, "petal_length", "petal_width").add_legend()
    figura = fig.fig

    canvas = FigureCanvasTkAgg(figura, petalwin)
    canvas.draw()
    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas, petalwin)
    toolbar.update()
    canvas.get_tk_widget().pack()
    petalwin.protocol("WM_DELETE_WINDOW", closepetal)
    petalwin.mainloop()


# -------------------------- FUNC. EXTRA -----------------------------------
# Válida datos escritos en los entry, solo números y '.'
def validate_entry(text):
    if (text == '.') or text.isdecimal():
        return True
    return False


# Función para predecir specie, llamada por botón
def predecir():
    p1.config(text="")  # Limpia el label para no sobreponerse las letras
    # el valor species será predicho
    # Contrucción de los valores en lista para pasarlos por el algoritmo
    valores = [[e1.get(), e2.get(), e3.get(), e4.get()], ]
    sp_pred = clf.predict(valores)  # Valor predicho de species
    # Convierte el valor de specie de númerico al string correspondiente
    specie = None
    if sp_pred[0] == 0:
        specie = "setosa"
    elif sp_pred[0] == 1:
        specie = "versicolor"
    elif sp_pred[0] == 2:
        specie = "virginica"

    tk.Label(root, text="is a", font="bold").place(x=360, y=330)
    # tk.Label(root, text=f"{specie}", fg="blue", font=("Verdana", 18)).place(x=330, y=360)
    p1.config(text=f"{specie}")  # Añade lo predicho al label


# --------------------------
# ---------- MAIN ----------
# --------------------------
root = tk.Tk()  # Ventana principal
root.title("Iris Tkinter App with ML")
root.resizable(0, 0)
root.geometry("540x470")
# Botones para abrir distintas funciones, datos y gráficas
dataButton = tk.Button(root, text="Iris Data", bg="white smoke",
                       command=DataWindow)
dataButton.place(x=20, y=10)
sepalButton = tk.Button(root, text="Sepal Graphic", bg="white smoke",
                        command=SepalWindow)
sepalButton.place(x=80, y=10)
petalButton = tk.Button(root, text="Petal Graphic", bg="white smoke",
                        command=PetalWindow)
petalButton.place(x=170, y=10)

tk.Label(root, text=f"Algorithm with {(acc*100):.3f} % efficiency",
         fg="blue").place(x=310, y=10)  # Eficiencia del algoritmo

df = pd.read_csv("iris.csv", sep=',', decimal='.')
describe = df.describe()  # Obtiene una descripción de los datos
# Se insertan la descripción en la ventana principal
table = tk.Text(root, bg="ghost white", height=9, width=59, padx=10, pady=5)
table.insert(tk.INSERT, describe.to_string())
table.configure(state="disabled")  # Deshabilita edición
table.place(x=20, y=50)

# --- Segunda parte de la ventana ---
tk.Label(root, text="Enter the values ​​of the specie to be predicted:",
         font="bold").place(x=20, y=240)
# Labels y cuadros para obtener los valores necesarios
tk.Label(root, text="Sepal Length: ").place(x=20, y=280)
tk.Label(root, text="Sepal Width: ").place(x=20, y=320)
tk.Label(root, text="Petal Length: ").place(x=20, y=360)
tk.Label(root, text="Petal Width: ").place(x=20, y=400)
e1 = tk.Entry(root, justify=tk.CENTER, validate="key",
              validatecommand=(root.register(validate_entry), "%S"))
e1.place(x=100, y=280)
e2 = tk.Entry(root, justify=tk.CENTER, validate="key",
              validatecommand=(root.register(validate_entry), "%S"))
e2.place(x=100, y=320)
e3 = tk.Entry(root, justify=tk.CENTER, validate="key",
              validatecommand=(root.register(validate_entry), "%S"))
e3.place(x=100, y=360)
e4 = tk.Entry(root, justify=tk.CENTER, validate="key",
              validatecommand=(root.register(validate_entry), "%S"))
e4.place(x=100, y=400)
# Botón para predecir la specie correspondiente a los datos dados
predButton = tk.Button(root, text="Predict!", activebackground="DarkSeaGreen1",
                       bg="PaleGreen1", command=predecir, font="bold")
predButton.place(x=340, y=280)
'''p1 = tk.Label(root, text="").place(x=340, y=320)
   p2 = tk.Label(root, text="", font="bold").place(x=330, y=360)'''
# Label que contendrá la predicción, declaración y posicionamiento
p1 = tk.Label(root, text="", fg="blue", font=("Verdana", 18))
p1.place(x=330, y=360)

root.mainloop()
