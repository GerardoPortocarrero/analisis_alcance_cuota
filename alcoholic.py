import matplotlib.pyplot as plt

# POR AÑO -------------------------------------------------------------------------------------------
def cf_draw_by_alcoholic_drink_for_year(df, date, bar_width, bar_height, color, font_size):
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
            ax=ax,
            figsize=(bar_width, bar_height),
            color=color
        )

        # Título personalizado con tamaño de fuente
        ax.set_title(f'Cajas Fisicas - {concepto} - {date}', fontsize=font_size)

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
            ('Total: ' + str(f'{total_cf_bebida:,.1f} CF')), # texto a mostrar
            transform=ax.transAxes,
            ha='right', va='top',
            fontsize=font_size,
            color='black',
            bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3')
        )

        # Cambiar el titulo del eje x
        ax.set_xlabel("")

        # Rotar etiquetas del eje X
        plt.xticks(rotation=45, ha='right', fontsize=font_size)

        plt.tight_layout()
        fig_name = f'cf_{concepto}-{date}.png'
        plt.savefig(fig_name)

        return fig_name
    except:
        print(f'Cantidad de datos: {len(df)}')
        print('No hay datos (Probablemente un domingo o festivo o no hubo rechazos) 3')

def cu_draw_by_alcoholic_drink_for_year(df, date, bar_width, bar_height, color, font_size):
    try:        
        # Filtrar solo las filas con CONCEPTO = 'BEBIDA'
        concepto = 'BEBIDAS ALCOHOLICAS'
        df = df[df['CONCEPTO'] == concepto]

        # Agrupar y ordenar
        cf_bebida = df.groupby('SEDE')['CU'].sum().sort_values(ascending=False)

        # Crear figura y eje
        fig, ax = plt.subplots()

        # Graficar
        cf_bebida.plot(
            kind='bar',
            ax=ax,
            figsize=(bar_width, bar_height),
            color=color
        )

        # Título personalizado con tamaño de fuente
        ax.set_title(f'Cajas Unitarias - {concepto} - {date}', fontsize=font_size)

        total_cf_bebida = 0
        # Agregar valores exactos encima de cada barra
        for i, value in enumerate(cf_bebida.values):
            total_cf_bebida = total_cf_bebida + value
            ax.text(
                i, value + (value * 0.01),       # posición Y: ligeramente arriba de la barra
                f'{value:,.1f} CU',               # formato: separador de miles, sin decimales
                ha='center', va='bottom',
                fontsize=font_size, color='black'
            )

        # Agregar nota dentro del gráfico (opcional)
        ax.text(
            0.98, 0.96,
            ('Total: ' + str(f'{total_cf_bebida:,.1f} CU')), # texto a mostrar
            transform=ax.transAxes,
            ha='right', va='top',
            fontsize=font_size,
            color='black',
            bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3')
        )

        # Cambiar el titulo del eje x
        ax.set_xlabel("")

        # Rotar etiquetas del eje X
        plt.xticks(rotation=45, ha='right', fontsize=font_size)

        plt.tight_layout()
        fig_name = f'cu_{concepto}-{date}.png'
        plt.savefig(fig_name)

        return fig_name
    except:
        print(f'Cantidad de datos: {len(df)}')
        print('No hay datos (Probablemente un domingo o festivo o no hubo rechazos) 3.5')

# POR MES -------------------------------------------------------------------------------------------
def cf_draw_by_alcoholic_drink_for_actual_month(df, date, bar_width, bar_height, color, font_size):
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
            ax=ax,
            figsize=(bar_width, bar_height),
            color=color
        )

        # Título personalizado con tamaño de fuente
        ax.set_title(f'Cajas Fisicas - {concepto} - {date}', fontsize=font_size)

        total_cf_bebida = 0
        # Agregar valores exactos encima de cada barra
        for i, value in enumerate(cf_bebida.values):
            total_cf_bebida = total_cf_bebida + value
            ax.text(
                i, value + (value * 0.01),        # posición Y: ligeramente arriba de la barra
                f'{value:,.1f} CF',               # formato: separador de miles, sin decimales
                ha='center', va='bottom',
                fontsize=font_size, color='black'
            )

        # Agregar nota dentro del gráfico (opcional)
        ax.text(
            0.98, 0.96,
            ('Total: ' + str(f'{total_cf_bebida:,.1f} CF')), # texto a mostrar
            transform=ax.transAxes,
            ha='right', va='top',
            fontsize=font_size,
            color='black',
            bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3')
        )

        # Cambiar el titulo del eje x
        ax.set_xlabel("")

        # Rotar etiquetas del eje X
        plt.xticks(rotation=45, ha='right', fontsize=font_size)

        plt.tight_layout()
        fig_name = f'cf_{concepto}-{date}.png'
        plt.savefig(fig_name)

        return fig_name
    except:
        print(f'Cantidad de datos: {len(df)}')
        print('No hay datos (Probablemente un domingo o festivo o no hubo rechazos) 4')

def cu_draw_by_alcoholic_drink_for_actual_month(df, date, bar_width, bar_height, color, font_size):
    try:        
        # Filtrar solo las filas con CONCEPTO = 'BEBIDA'
        concepto = 'BEBIDAS ALCOHOLICAS'
        df = df[df['CONCEPTO'] == concepto]

        # Agrupar y ordenar
        cf_bebida = df.groupby('SEDE')['CU'].sum().sort_values(ascending=False)

        # Crear figura y eje
        fig, ax = plt.subplots()

        # Graficar
        cf_bebida.plot(
            kind='bar',
            ax=ax,
            figsize=(bar_width, bar_height),
            color=color
        )

        # Título personalizado con tamaño de fuente
        ax.set_title(f'Cajas Unitarias - {concepto} - {date}', fontsize=font_size)

        total_cf_bebida = 0
        # Agregar valores exactos encima de cada barra
        for i, value in enumerate(cf_bebida.values):
            total_cf_bebida = total_cf_bebida + value
            ax.text(
                i, value + (value * 0.01),        # posición Y: ligeramente arriba de la barra
                f'{value:,.1f} CU',               # formato: separador de miles, sin decimales
                ha='center', va='bottom',
                fontsize=font_size, color='black'
            )

        # Agregar nota dentro del gráfico (opcional)
        ax.text(
            0.98, 0.96,
            ('Total: ' + str(f'{total_cf_bebida:,.1f} CU')), # texto a mostrar
            transform=ax.transAxes,
            ha='right', va='top',
            fontsize=font_size,
            color='black',
            bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3')
        )

        # Cambiar el titulo del eje x
        ax.set_xlabel("")

        # Rotar etiquetas del eje X
        plt.xticks(rotation=45, ha='right', fontsize=font_size)

        plt.tight_layout()
        fig_name = f'cu_{concepto}-{date}.png'
        plt.savefig(fig_name)

        return fig_name
    except:
        print(f'Cantidad de datos: {len(df)}')
        print('No hay datos (Probablemente un domingo o festivo o no hubo rechazos) 4')