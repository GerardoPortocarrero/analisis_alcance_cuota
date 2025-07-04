import pandas as pd
import polars as pl
import os

# Obtener datos de locaciones especificas
def get_specific_year(df: pl.DataFrame, year: int) -> pl.DataFrame:
    return df.filter(pl.col("AÑO") == year)

# Obtener datos de locaciones especificas
def get_specific_location(df: pl.DataFrame, locaciones: list[str]) -> pl.DataFrame:
    df = df.with_columns(
        pl.col("SEDE").str.strip_chars().alias("SEDE")
    )
    return df.filter(pl.col("SEDE").is_in(locaciones))

# Leer csv con polars
def read_csv_with_pl(csv_file):
    df = pl.read_csv(csv_file)
    return df

# Convertir dataframe a csv
def create_csv(df, csv_file):
    # Guardar el contenido modificado en un nuevo archivo CSV
    df.to_csv(csv_file, index=False, encoding="utf-8")

# Eliminar columnas innecesarias
def get_relevant_columns(df, document):
    return df[document['relevant_columns']]

# Filtrar ruido (obtener la tabla principal)
def filter_noise(df):
    # Tomar la fila 1 como nombres de columns
    df.columns = df.iloc[0]
    df.columns = df.columns.str.strip()

    # Eliminar filas innecesarias
    df = df.iloc[1:].reset_index(drop=True)

    return df

# Funcion principal
def get_clean_data(document):
    # Leer excel
    df = pd.read_excel(document['file_name'], sheet_name=document['sheet_name'], header=None)

    # Filtrar ruido
    df = filter_noise(df)

    # Eliminar columnas innecesarias
    df = get_relevant_columns(df, document)

    # Crear csv a partir del df
    create_csv(df, document['csv_file_name'])

    # Leer csv con polars
    df = read_csv_with_pl(document['csv_file_name'])

    return df