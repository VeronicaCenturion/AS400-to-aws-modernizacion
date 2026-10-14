# Glue Job que reemplaza proceso batch RPG de AS400
# Proceso original RPG: LEER CLIENTES -> FILTRAR ACTIVOS -> CALCULAR SALDO -> ESCRIBIR REPORTE
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Inicializacion Glue
glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session

# 1. Leer datos que trajo DMS desde AS400 (S3 raw)
df_clientes = spark.read.parquet("s3://tu-bucket-as400/raw/ventas/clientes/")

# 2. Logica que antes estaba en RPG - ahora en PySpark
# RPG: IF ESTCLI = 'A'
df_activos = df_clientes.filter(df_clientes["estado"] == "A")

# RPG: EVAL SALDO = SALDO - PAGOS
df_con_saldo = df_activos.withColumn("saldo_final", df_activos["saldo"] - df_activos["pagos"])

# 3. Guardar resultado curado para Athena
df_con_saldo.write.mode("overwrite").parquet("s3://tu-bucket-as400/curated/clientes_activos/")

print("Proceso batch AS400 modernizado a Glue completado")
