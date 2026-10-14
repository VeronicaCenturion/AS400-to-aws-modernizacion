# Documentación - Pipeline CI/CD AS400 a AWS

**Autora:** Verito Centurion  
**Fecha:** 14 de Octubre de 2026  
**Proyecto:** RPG Migración AS400 -> S3  
**Bucket:** rpg-migracion-vcenturion-2026/pf-migrados/

## 🎯 Objetivo
Automatizar el despliegue de artefactos de modernización (mapeos, jobs de Glue, CSVs) desde GitHub hacia AWS S3 sin hacer cargas manuales.

## 🏗️ Arquitectura Implementada
GitHub (rama principal) -> GitHub Actions (.yml) -> AWS S3 (pf-migrados/)

## ✅ Pasos Realizados

### 1. Configuración de Seguridad en AWS (IAM)
- Usuario creado: `github-deployer`
- Permiso: Acceso solo a `s3://rpg-migracion-vcenturion-2026/pf-migrados/*`
- Archivo de claves descargado: `accessKeys.csv`
    - **Fila 1:** Encabezados (User Name, Access key ID, Secret...)
    - **Fila 2:** Valores reales
        - Columna 1: AKIA... (Access Key ID)
        - Columna 2: wJalr... (Secret Access Key)

### 2. Configuración de Seguridad en GitHub
Ruta: `Repositorio > Settings > Secrets and variables > Actions > New repository secret`

Se crearon 2 secretos:
- `AWS_ACCESS_KEY_ID` -> Valor AKIA... (Fila 2, Columna 1)
- `AWS_SECRET_ACCESS_KEY` -> Valor largo secreto (Fila 2, Columna 2)

> Importante: Nunca subir las claves al código. Usar siempre secrets.

### 3. Automatización con GitHub Actions
Archivo creado: `.github/workflows/deploy-to-s3.yml`

```yaml
name: Deploy PF a S3
on:
  push:
    branches: [ principal, main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
            - uses: actions/checkout@v4
            - name: Configurar AWS
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
            - name: Subir archivos a S3
        run: |
          aws s3 cp table-mappings.json s3://rpg-migracion-vcenturion-2026/pf-migrados/ --region us-east-1 || echo "no existe table-mappings.json"
          aws s3 cp glue_job_clientes.py s3://rpg-migracion-vcenturion-2026/pf-migrados/ --region us-east-1 || echo "no existe glue_job_clientes.py"
          aws s3 sync . s3://rpg-migracion-vcenturion-2026/pf-migrados/ --exclude ".git/*" --exclude ".github/*" --region us-east-1
          echo "✅ Deploy completado"
