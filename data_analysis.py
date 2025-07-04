import polars as pl
import matplotlib.pyplot as plt
import numpy as np

# Transformar la columna 'Fecha' a datetime
def parse_date(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.with_columns([
            pl.col("FECHA").str.strptime(pl.Date, "%Y-%m-%d %H:%M:%S").alias("FECHA_DATE"),
            pl.col("FECHA").str.strptime(pl.Date, "%Y-%m-%d %H:%M:%S").dt.strftime("%Y-%m").alias("PERIODO")
        ])
    )

# ANALISIS -----------------------------------------------------------------

# 1. ANALISIS TEMPORAL
def analisis_temporal_graphic(df):
    # Convertimos a pandas solo para graficar
    df_pd = df.to_pandas()

    # Colores representativos
    color_coca = "#D60000"     # CU - Rojo Coca-Cola
    color_fanta = "#FF6F00"    # CF - Naranja Fanta
    color_inca = "#FFD700"     # Eficiencia - Amarillo Inca Kola

    # Aumentar tamaño para evitar que las etiquetas choquen
    plt.figure(figsize=(14, 7))
    plt.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)

    # Eliminar bordes
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Graficar CU
    plt.plot(df_pd["PERIODO"], df_pd["CU_TOTAL"], 
             marker='o', markersize=7, linewidth=2.5, label="CU (Líquido)", color=color_coca)
    for x, y in zip(df_pd["PERIODO"], df_pd["CU_TOTAL"]):
        plt.text(x, y + max(df_pd["CU_TOTAL"]) * 0.03, f"{y:,.0f}", 
                 color=color_coca, fontsize=9, ha='center')

    # Graficar CF
    plt.plot(df_pd["PERIODO"], df_pd["CF_TOTAL"], 
             marker='s', markersize=6, linewidth=2.5, label="CF (Cajas)", color=color_fanta)
    for x, y in zip(df_pd["PERIODO"], df_pd["CF_TOTAL"]):
        plt.text(x, y - max(df_pd["CF_TOTAL"]) * 0.05, f"{y:,.0f}", 
                 color=color_fanta, fontsize=9, ha='center')

    # Graficar EFICIENCIA si existe
    if "EFICIENCIA_CU_POR_CF" in df_pd.columns:
        plt.plot(df_pd["PERIODO"], df_pd["EFICIENCIA_CU_POR_CF"], 
                 marker='D', markersize=6, linewidth=2.5, label="Eficiencia (CU/CF)", color=color_inca)
        for x, y in zip(df_pd["PERIODO"], df_pd["EFICIENCIA_CU_POR_CF"]):
            plt.text(x, y + 0.05, f"{y:.2f}", color=color_inca, fontsize=9, ha='center')

    # Títulos y ejes
    plt.title("Evolución Temporal de CU y CF", fontsize=16, fontweight='bold', color="#333333", pad=20)
    plt.xlabel("Periodo", fontsize=13)
    plt.ylabel("Cantidad", fontsize=13)
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)

    # Leyenda con fondo suave
    plt.legend(frameon=True, framealpha=0.9, facecolor="#f9f9f9", fontsize=10)

    plt.tight_layout()
    plt.show()

def analisis_temporal(df):
    # Parsear la fecha (con nueva columna)
    df = parse_date(df)

    # Agrupar por periodo
    df_mes = (
        df.group_by("PERIODO").agg([
            pl.col("CU").sum().alias("CU_TOTAL"),
            pl.col("CF").sum().alias("CF_TOTAL")
        ])
        .sort("PERIODO")
    )

    # Graficar
    analisis_temporal_graphic(df_mes)

# 2. ANALISIS ESTADISTICO
def analisis_estadistico_graphic(df: pl.DataFrame):
    df_stats_pd = df.to_pandas()
    periodos = df_stats_pd["PERIODO"]
    x = np.arange(len(periodos))
    width = 0.35  # Ancho de las barras

    # Colores personalizados
    color_coca = "#D60000"     # CU Media
    color_coca_std = "#FF4C4C" # CU STD

    color_fanta = "#FF6F00"    # CF Media
    color_fanta_std = "#FFA04C" # CF STD

    fig, ax = plt.subplots(figsize=(14, 7))

    # Eliminar bordes del gráfico
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Graficar CU (Media y STD apilado)
    bars_cu_media = ax.bar(x - width/2, df_stats_pd["CU_MEDIA"], width, label='CU Media', color=color_coca)
    bars_cu_std = ax.bar(x - width/2, df_stats_pd["CU_STD"], width, 
                         bottom=df_stats_pd["CU_MEDIA"], label='CU Desv. Estándar', color=color_coca_std, alpha=0.85)

    # Graficar CF (Media y STD apilado)
    bars_cf_media = ax.bar(x + width/2, df_stats_pd["CF_MEDIA"], width, label='CF Media', color=color_fanta)
    bars_cf_std = ax.bar(x + width/2, df_stats_pd["CF_STD"], width, 
                         bottom=df_stats_pd["CF_MEDIA"], label='CF Desv. Estándar', color=color_fanta_std, alpha=0.85)

    # Añadir etiquetas encima de cada barra (solo media)
    for bars in [bars_cu_media, bars_cf_media]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:,.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 5),  # desplazamiento vertical
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)

    # Ejes y títulos
    ax.set_title('Media y Desviación Estándar por Mes (CU y CF)', fontsize=16, fontweight='bold', color="#333333", pad=20)
    ax.set_ylabel('Valor Promedio + STD', fontsize=13)
    ax.set_xticks(x)
    ax.set_xticklabels(periodos, rotation=45, fontsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(True, axis='y', linestyle='--', linewidth=0.5, alpha=0.6)

    # Leyenda estilizada
    ax.legend(frameon=True, framealpha=0.9, facecolor="#f9f9f9", fontsize=10)

    plt.tight_layout()
    plt.show()

def analisis_estadistico(df: pl.DataFrame):
    '''
    Analizar la distribución y variabilidad de CU y CF:
    - Media
    - Desviación estándar
    - Máximo / Mínimo
    - Coeficiente de variación (CV = std / media)
    '''
    # Agrupar por periodo
    df = parse_date(df)

    df_stats = (
        df.group_by("PERIODO")
        .agg([
            pl.col("CU").mean().alias("CU_MEDIA"),
            pl.col("CU").std().alias("CU_STD"),
            pl.col("CU").min().alias("CU_MIN"),
            pl.col("CU").max().alias("CU_MAX"),
            (pl.col("CU").std() / pl.col("CU").mean()).alias("CU_CV"),

            pl.col("CF").mean().alias("CF_MEDIA"),
            pl.col("CF").std().alias("CF_STD"),
            pl.col("CF").min().alias("CF_MIN"),
            pl.col("CF").max().alias("CF_MAX"),
            (pl.col("CF").std() / pl.col("CF").mean()).alias("CF_CV"),
        ])
    ).sort("PERIODO")

    # Graficar
    analisis_estadistico_graphic(df_stats)

# 3. ANALISIS COMPARATIVO
def analisis_comparativo_graphic(df: pl.DataFrame):
    df_sede_pd = df.to_pandas().sort_values("CU_TOTAL", ascending=False)

    # Colores
    color_coca = "#D60000"    # CU
    color_fanta = "#FF6F00"   # CF
    color_text_cf = "#222222" # Texto sobre barra naranja

    fig, ax = plt.subplots(figsize=(14, 7))

    for spine in ax.spines.values():
        spine.set_visible(False)

    # Barras CU
    bars_cu = ax.bar(df_sede_pd["SEDE"], df_sede_pd["CU_TOTAL"], label="CU (Líquido)", color=color_coca)

    # Barras CF (apilado)
    bars_cf = ax.bar(df_sede_pd["SEDE"], df_sede_pd["CF_TOTAL"], 
                     bottom=0, label="CF (Cajas)", color=color_fanta, alpha=0.75)

    # Etiquetas CU
    for bar in bars_cu:
        height = bar.get_height()
        ax.annotate(f'{height:,.0f}', 
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, color=color_coca)

    # Etiquetas CF con mejor contraste
    for bar in bars_cf:
        height = bar.get_height()
        ax.annotate(f'{height:,.0f}', 
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, -14), textcoords="offset points",
                    ha='center', va='top', fontsize=9, color=color_text_cf)

    # Estética general
    ax.set_title("Volumen Total por Sede", fontsize=16, fontweight='bold', color="#333333", pad=20)
    ax.set_xticks(range(len(df_sede_pd)))
    ax.set_xticklabels(df_sede_pd["SEDE"], rotation=45, ha="right", fontsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    ax.legend(frameon=True, framealpha=0.9, facecolor="#f9f9f9", fontsize=10)
    plt.tight_layout()
    plt.show()

def analisis_comparativo(df: pl.DataFrame):
    # Agrupar por periodo
    df = parse_date(df)

    df_sede = (
        df.group_by("SEDE")
        .agg([
            pl.col("CU").sum().alias("CU_TOTAL"),
            pl.col("CF").sum().alias("CF_TOTAL"),
            pl.col("CU").mean().alias("CU_PROM"),
            pl.col("CF").mean().alias("CF_PROM")
        ])
        .sort("CU_TOTAL", descending=True)
    )

    total_cu = df_sede.select(pl.col("CU_TOTAL").sum()).item()
    total_cf = df_sede.select(pl.col("CF_TOTAL").sum()).item()

    df_sede = df_sede.with_columns([
        (pl.col("CU_TOTAL") / total_cu * 100).round(2).alias("CU_PARTICIPACION_PORC"),
        (pl.col("CF_TOTAL") / total_cf * 100).round(2).alias("CF_PARTICIPACION_PORC")
    ])

    # Graficar
    analisis_comparativo_graphic(df_sede)

# 4. TENDENCIAS Y ESTACIONALIDAD
def analisis_tendencia_estacionalidad_graphic(df: pl.DataFrame):
    df_pd = df.to_pandas()
    df_pd = df_pd.set_index("PERIODO")

    # Colores estilo Coca-Cola y Fanta
    color_coca = "#D60000"
    color_coca_smooth = "#D60000"
    color_fanta = "#FF6F00"
    color_fanta_smooth = "#FF6F00"

    # Suavizado de 3 periodos centrado
    df_pd["CU_SMOOTH"] = df_pd["CU_TOTAL"].rolling(3, center=True).mean()
    df_pd["CF_SMOOTH"] = df_pd["CF_TOTAL"].rolling(3, center=True).mean()

    # === Gráfico CU ===
    fig, ax = plt.subplots(figsize=(14, 6))

    # Bordes fuera
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.plot(df_pd.index, df_pd["CU_TOTAL"], label="CU Total", color=color_coca, linewidth=2.0, linestyle='--', marker='o')
    ax.plot(df_pd.index, df_pd["CU_SMOOTH"], label="CU Suavizado", color=color_coca_smooth, linewidth=3.0, marker='')

    # Etiqueta en último punto de CU suavizado
    if not df_pd["CU_SMOOTH"].isna().all():
        last_idx = df_pd["CU_SMOOTH"].last_valid_index()
        last_val = df_pd.loc[last_idx, "CU_SMOOTH"]
        ax.annotate(f"{last_val:,.0f}", xy=(last_idx, last_val), xytext=(5, 5),
                    textcoords="offset points", color=color_coca_smooth, fontsize=9)

    ax.set_title("Tendencia - CU", fontsize=16, fontweight='bold', color="#333333", pad=20)
    ax.set_ylabel("CU Total", fontsize=13)
    ax.set_xticks(df_pd.index)
    ax.set_xticklabels(df_pd.index, rotation=45, fontsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(frameon=True, framealpha=0.9, facecolor="#f9f9f9", fontsize=10)
    plt.tight_layout()
    plt.show()

    # === Gráfico CF ===
    fig, ax = plt.subplots(figsize=(14, 6))

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.plot(df_pd.index, df_pd["CF_TOTAL"], label="CF Total", color=color_fanta, linewidth=2.0, linestyle='--', marker='s')
    ax.plot(df_pd.index, df_pd["CF_SMOOTH"], label="CF Suavizado", color=color_fanta_smooth, linewidth=3.0, marker='')

    # Etiqueta en último punto de CF suavizado
    if not df_pd["CF_SMOOTH"].isna().all():
        last_idx = df_pd["CF_SMOOTH"].last_valid_index()
        last_val = df_pd.loc[last_idx, "CF_SMOOTH"]
        ax.annotate(f"{last_val:,.0f}", xy=(last_idx, last_val), xytext=(5, 5),
                    textcoords="offset points", color=color_fanta_smooth, fontsize=9)

    ax.set_title("Tendencia - CF", fontsize=16, fontweight='bold', color="#333333", pad=20)
    ax.set_ylabel("CF Total", fontsize=13)
    ax.set_xticks(df_pd.index)
    ax.set_xticklabels(df_pd.index, rotation=45, fontsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(frameon=True, framealpha=0.9, facecolor="#f9f9f9", fontsize=10)
    plt.tight_layout()
    plt.show()

def analisis_tendencia_estacionalidad(df: pl.DataFrame):
    # Agrupar por periodo
    df = parse_date(df)

    df_mes = (
        df.group_by("PERIODO")
        .agg([
            pl.col("CU").sum().alias("CU_TOTAL"),
            pl.col("CF").sum().alias("CF_TOTAL")
        ])
        .sort("PERIODO")
    )

    # Graficar
    analisis_tendencia_estacionalidad_graphic(df_mes)