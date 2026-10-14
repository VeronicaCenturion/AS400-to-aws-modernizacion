# Modernización de AS400 a AWS - DMS + Glue

## Objetivo del proyecto
Modernizar procesos batch de AS/400 (IBM i) llevando datos de DB2 for i a un Data Lake en AWS de forma continua para usarlos con Glue y Athena.

## Arquitectura
AS/400 (DB2 for i con Journaling) -> AWS DMS Serverless (Full Load + CDC) -> S3 (raw/parquet) -> Glue Crawler -> Glue Job (PySpark) -> S3 (curated) -> Athena

## Tecnologías
- AWS DMS: Replica continua con CDC usando journal de DB2
- S3: Data Lake en formato Parquet
- AWS Glue: Transformación de lógica RPG a PySpark
- Athena: Consultas SQL

## Archivos
- table-mappings.json: Reglas de selección de tablas para DMS

## Próximos pasos
- Crear Glue Job que reemplaza lógica RPG
- Consultas en Athena para análisis de clientes

Autora: Veronica Centurion - Proyecto de portfolio AS400 modernization
