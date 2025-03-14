- Col: Fecha
- Primera col: Ticker

- Segunda col: análisis sentimiento (-1 a -0.25)

- Tercera col (y n col): guardar valor de la EMA como variable
- Columna n+1: Varianza
- Columna : Subasta apertura, Subasta cierre, Precio Cierre
- Columna : Volumen

---

Variable a predecir: Varianza y un binario (1: sube 0: baja)

Variable a predecir: Precio Cierre

------
Modelo: XGBOOST
Estudio de la explicabilidad

Guardar los ficheros como .parquet




