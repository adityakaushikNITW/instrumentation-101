from setuptools import setup, find_packages

setup(
    name="parking-lot",
    version="0.1.0",
    packages=find_packages(where="."),
    package_dir={"": "."},
    install_requires=[
        "fastapi==0.109.2",
        "uvicorn==0.27.1",
        "sqlalchemy==2.0.27",
        "psycopg2-binary==2.9.9",
        "pydantic==2.6.1",
        "python-dotenv==1.0.1",
        "opentelemetry-api==1.22.0",
        "opentelemetry-sdk==1.22.0",
        "opentelemetry-instrumentation-fastapi==0.43b0",
        "opentelemetry-exporter-otlp==1.22.0",
        "opentelemetry-instrumentation-sqlalchemy==0.43b0",
        "opentelemetry-exporter-otlp-proto-grpc==1.22.0",
        "opentelemetry-instrumentation==0.43b0"
    ],
    python_requires=">=3.11",
) 