FROM bitnami/spark:3.5.0

USER root

# Install curl for downloading drivers
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Create directory for JDBC drivers
RUN mkdir -p /opt/bitnami/spark/jars

# Download PostgreSQL and ClickHouse JDBC drivers
RUN curl -L https://jdbc.postgresql.org/download/postgresql-42.7.1.jar -o /opt/bitnami/spark/jars/postgresql-42.7.1.jar && \
    curl -L https://github.com/ClickHouse/clickhouse-jdbc/releases/download/v0.4.6/clickhouse-jdbc-0.4.6.jar -o /opt/bitnami/spark/jars/clickhouse-jdbc-0.4.6.jar

# Set permissions
RUN chown -R 1001:1001 /opt/bitnami/spark/jars

USER 1001 