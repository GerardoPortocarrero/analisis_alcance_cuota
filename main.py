import os
import pandas as pd
import matplotlib.pyplot as plt
import non_alcoholic as nonal
import alcoholic as al
import join_images as ji

def read_excel_file(local_file_address, file_sheet_name):
    # Leer datos del archivo de correo
    return pd.read_excel(local_file_address, sheet_name=file_sheet_name, header=None)

def clean_excel_file(df):
    # Identificar columnas donde la primera fila (índice 0) es NaN
    columns_to_delete = df.columns[df.iloc[0].isna()]    

    # Eliminar esas columnas
    df = df.drop(columns=columns_to_delete)

    # Tomar la fila 1 como nombres de columnas
    df.columns = df.iloc[0]

    # Reiniciar el índice si quieres
    df = df.iloc[1:].reset_index(drop=True)

    return df

def filter_by_year(df, year):
    # Filtrar el DataFrame por el año especificado
    df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y')
    year_inicio = pd.to_datetime('01/01/'+str(year), format='%d/%m/%Y')
    year_fin = pd.to_datetime('31/12/'+str(year), format='%d/%m/%Y')
    return df[(df['FECHA'] >= year_inicio) & (df['FECHA'] <= year_fin)]

def filter_by_month(df, month, year):
    # Filtrar el DataFrame por el año especificado
    fecha_inicio = pd.to_datetime('01/'+str(month)+'/'+str(year), format='%d/%m/%Y')
    fecha_fin = pd.to_datetime('01/'+str(int(month)+1)+'/'+str(year), format='%d/%m/%Y')
    return df[(df['FECHA'] >= fecha_inicio) & (df['FECHA'] < fecha_fin)]


# --- Main Settings ---
if __name__ == "__main__":
    # Variables de configuracion
    year = int(input("AÑO (2025): "))
    month = int(input("MES (1-12): "))
    months = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
              7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 
              11: 'Noviembre', 12: 'Diciembre'} # Diccionario de meses
    root_address = r'C:\Informacion\Alcance de Cuota' # Direcccion de carpeta raiz
    file_name = 'ALCANCE DE CUOTA 2025.xlsx' # Nombre del archivo de Excel
    file_sheet_name = 'AC TAB' # Nombre de la hoja de Excel
    local_file_address = os.path.join(root_address, file_name) # Direccion del archivo de Excel
    bar_width = 12
    bar_height = 9
    font_size = 16
    color_1 = "#FFED50"
    color_2 = "#9E9C1A"
    color_3 = "#FC6060"
    color_4 = "#992121"

    # Leer excel
    df = read_excel_file(local_file_address, file_sheet_name)
    df = clean_excel_file(df)
    
    # Filtrar por año
    df_year = filter_by_year(df, year)

    # Filtrar por mes
    df_month = filter_by_month(df, month, year)

    # Reportes
    a = nonal.cf_draw_by_non_alcoholic_drink_for_year(df_year, year, bar_width, bar_height, color_2, font_size)
    b = nonal.cu_draw_by_non_alcoholic_drink_for_year(df_year, year, bar_width, bar_height, color_4, font_size)
    c = nonal.cf_draw_by_non_alcoholic_drink_for_actual_month(df_month, str(months[month]+' de '+str(year)), bar_width, bar_height, color_1, font_size)    
    d = nonal.cu_draw_by_non_alcoholic_drink_for_actual_month(df_month, str(months[month]+' de '+str(year)), bar_width, bar_height, color_3, font_size)    
    ji.join_images_by_concepto([a, b, c, d], "nonalcoholic_report")
 
    e = al.cf_draw_by_alcoholic_drink_for_year(df_year, year, bar_width, bar_height, color_2, font_size)
    f = al.cu_draw_by_alcoholic_drink_for_year(df_year, year, bar_width, bar_height, color_4, font_size)
    g = al.cf_draw_by_alcoholic_drink_for_actual_month(df_month, str(months[month]+' de '+str(year)), bar_width, bar_height, color_1, font_size)
    h = al.cu_draw_by_alcoholic_drink_for_actual_month(df_month, str(months[month]+' de '+str(year)), bar_width, bar_height, color_3, font_size)    
    ji.join_images_by_concepto([e, f, g, h], "alcoholic_report")