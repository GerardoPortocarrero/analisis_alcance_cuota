import os
import pandas as pd
import matplotlib.pyplot as plt

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

def draw_by_non_alcoholic_drink_for_actual_month(df, date, bar_width, bar_height, color, font_size):
    try:        
        # Filtrar solo las filas con CONCEPTO = 'BEBIDA'
        concepto = 'BEBIDA'
        df = df[df['CONCEPTO'] == concepto]

        # Agrupar y ordenar
        cf_bebida = df.groupby('SEDE')['CF'].sum().sort_values(ascending=False)

        # Crear figura y eje
        fig, ax = plt.subplots()

        # Graficar
        cf_bebida.plot(
            kind='bar',
            title=f'{concepto}S NO ALCOHOLICAS',
            ax=ax,
            figsize=(bar_width, bar_height),
            color=color
        )

        total_cf_bebida = 0
        # Agregar valores exactos encima de cada barra
        for i, value in enumerate(cf_bebida.values):
            total_cf_bebida = total_cf_bebida + value
            ax.text(
                i, value + (value * 0.01),       # posición Y: ligeramente arriba de la barra
                f'{value:,.1f} CF',               # formato: separador de miles, sin decimales
                ha='center', va='bottom',
                fontsize=font_size, color='black'
            )

        # Agregar nota dentro del gráfico (opcional)
        ax.text(
            0.98, 0.96,
            ('MES: ' + str(date) + '\n\nTotal: ' + str(f'{total_cf_bebida:,.1f} CF')), # texto a mostrar
            transform=ax.transAxes,
            ha='right', va='top',
            fontsize=font_size-2,
            color='gray',
            bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3')
        )

        # Cambiar el titulo del eje x
        ax.set_xlabel("")

        # Rotar etiquetas del eje X
        plt.xticks(rotation=45, ha='right', fontsize=font_size)

        plt.tight_layout()
        plt.savefig(f'{concepto}S NO ALCOHOLICAS-{date}.png')
    except:
        print(f'Cantidad de datos: {len(df)}')
        print('No hay datos (Probablemente un domingo o festivo o no hubo rechazos)')

def draw_by_alcoholic_drink_for_actual_month(df, date, bar_width, bar_height, color, font_size):
    try:        
        # Filtrar solo las filas con CONCEPTO = 'BEBIDA'
        concepto = 'BEBIDAS ALCOHOLICAS'
        df = df[df['CONCEPTO'] == concepto]

        # Agrupar y ordenar
        cf_bebida = df.groupby('SEDE')['CF'].sum().sort_values(ascending=False)

        # Crear figura y eje
        fig, ax = plt.subplots()

        # Graficar
        cf_bebida.plot(
            kind='bar',
            title=f'{concepto}',
            ax=ax,
            figsize=(bar_width, bar_height),
            color=color
        )

        total_cf_bebida = 0
        # Agregar valores exactos encima de cada barra
        for i, value in enumerate(cf_bebida.values):
            total_cf_bebida = total_cf_bebida + value
            ax.text(
                i, value + (value * 0.01),       # posición Y: ligeramente arriba de la barra
                f'{value:,.1f} CF',               # formato: separador de miles, sin decimales
                ha='center', va='bottom',
                fontsize=font_size, color='black'
            )

        # Agregar nota dentro del gráfico (opcional)
        ax.text(
            0.98, 0.96,
            ('MES: ' + str(date) + '\n\nTotal: ' + str(f'{total_cf_bebida:,.1f} CF')), # texto a mostrar
            transform=ax.transAxes,
            ha='right', va='top',
            fontsize=font_size-2,
            color='gray',
            bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3')
        )

        # Cambiar el titulo del eje x
        ax.set_xlabel("")

        # Rotar etiquetas del eje X
        plt.xticks(rotation=45, ha='right', fontsize=font_size)

        plt.tight_layout()
        plt.savefig(f'{concepto}-{date}.png')
    except:
        print(f'Cantidad de datos: {len(df)}')
        print('No hay datos (Probablemente un domingo o festivo o no hubo rechazos)')

def draw_by_non_alcoholic_drink_for_year(df, date, bar_width, bar_height, color, font_size):
    try:        
        # Filtrar solo las filas con CONCEPTO = 'BEBIDA'
        concepto = 'BEBIDA'
        df = df[df['CONCEPTO'] == concepto]

        # Agrupar y ordenar
        cf_bebida = df.groupby('SEDE')['CF'].sum().sort_values(ascending=False)

        # Crear figura y eje
        fig, ax = plt.subplots()

        # Graficar
        cf_bebida.plot(
            kind='bar',
            title=f'{concepto}S NO ALCOHOLICAS',
            ax=ax,
            figsize=(bar_width, bar_height),
            color=color
        )

        total_cf_bebida = 0
        # Agregar valores exactos encima de cada barra
        for i, value in enumerate(cf_bebida.values):
            total_cf_bebida = total_cf_bebida + value
            ax.text(
                i, value + (value * 0.01),       # posición Y: ligeramente arriba de la barra
                f'{value:,.1f} CF',               # formato: separador de miles, sin decimales
                ha='center', va='bottom',
                fontsize=font_size, color='black'
            )

        # Agregar nota dentro del gráfico (opcional)
        ax.text(
            0.98, 0.96,
            ('AÑO: ' + str(date) + '\n\nTotal: ' + str(f'{total_cf_bebida:,.1f} CF')), # texto a mostrar
            transform=ax.transAxes,
            ha='right', va='top',
            fontsize=font_size-2,
            color='gray',
            bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3')
        )

        # Cambiar el titulo del eje x
        ax.set_xlabel("")

        # Rotar etiquetas del eje X
        plt.xticks(rotation=45, ha='right', fontsize=font_size)

        plt.tight_layout()
        plt.savefig(f'{concepto}S NO ALCOHOLICAS-{date}.png')
    except:
        print(f'Cantidad de datos: {len(df)}')
        print('No hay datos (Probablemente un domingo o festivo o no hubo rechazos)')

def draw_by_alcoholic_drink_for_year(df, date, bar_width, bar_height, color, font_size):
    try:        
        # Filtrar solo las filas con CONCEPTO = 'BEBIDA'
        concepto = 'BEBIDAS ALCOHOLICAS'
        df = df[df['CONCEPTO'] == concepto]

        # Agrupar y ordenar
        cf_bebida = df.groupby('SEDE')['CF'].sum().sort_values(ascending=False)

        # Crear figura y eje
        fig, ax = plt.subplots()

        # Graficar
        cf_bebida.plot(
            kind='bar',
            title=f'{concepto}',
            ax=ax,
            figsize=(bar_width, bar_height),
            color=color
        )

        total_cf_bebida = 0
        # Agregar valores exactos encima de cada barra
        for i, value in enumerate(cf_bebida.values):
            total_cf_bebida = total_cf_bebida + value
            ax.text(
                i, value + (value * 0.01),       # posición Y: ligeramente arriba de la barra
                f'{value:,.1f} CF',               # formato: separador de miles, sin decimales
                ha='center', va='bottom',
                fontsize=font_size, color='black'
            )

        # Agregar nota dentro del gráfico (opcional)
        ax.text(
            0.98, 0.96,
            ('AÑO: ' + str(date) + '\n\nTotal: ' + str(f'{total_cf_bebida:,.1f} CF')), # texto a mostrar
            transform=ax.transAxes,
            ha='right', va='top',
            fontsize=font_size-2,
            color='gray',
            bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3')
        )

        # Cambiar el titulo del eje x
        ax.set_xlabel("")

        # Rotar etiquetas del eje X
        plt.xticks(rotation=45, ha='right', fontsize=font_size)

        plt.tight_layout()
        plt.savefig(f'{concepto}-{date}.png')
    except:
        print(f'Cantidad de datos: {len(df)}')
        print('No hay datos (Probablemente un domingo o festivo o no hubo rechazos)')

# --- Main Settings ---
if __name__ == "__main__":
    # Variables de configuracion
    year = 2025 # Año de la cuota
    month = 5 # Mes de la cuota
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
    color_1 = "#FFF59D"
    color_2 = "#F4A460"

    # Leer excel
    df = read_excel_file(local_file_address, file_sheet_name)
    df = clean_excel_file(df)
    
    # Filtrar por año
    df_year = filter_by_year(df, year)

    # Filtrar por mes
    df_month = filter_by_month(df, month, year)

    # Reportes
    draw_by_non_alcoholic_drink_for_actual_month(df_month, str(months[month]+'-'+str(year)), bar_width, bar_height, color_1, font_size)
    draw_by_alcoholic_drink_for_actual_month(df_month, str(months[month]+'-'+str(year)), bar_width, bar_height, color_1, font_size)

    draw_by_non_alcoholic_drink_for_year(df_year, year, bar_width, bar_height, color_2, font_size)
    draw_by_alcoholic_drink_for_year(df_year, year, bar_width, bar_height, color_2, font_size)