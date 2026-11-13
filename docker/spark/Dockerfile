# Spark image of the project: Jupyter PySpark stack (pinned by date tag) plus the
# Kafka connector and the Python tooling used by the jobs and the tests.
#
# Tag 2026-09-07 ships Spark 4.2.0 / Scala 2.13 / Python 3.13 / OpenJDK 21.
ARG PYSPARK_NOTEBOOK_TAG=2026-09-07
FROM quay.io/jupyter/pyspark-notebook:${PYSPARK_NOTEBOOK_TAG}

USER root

# Bake the Structured Streaming Kafka connector into ${SPARK_HOME}/jars so that
# spark-submit needs neither --packages nor network access at run time. The
# connector version is derived from the Spark jars of the base image, which
# keeps both in sync when the base tag is changed.
RUN set -eux; \
    spark_sql_jar="$(basename "$(ls "${SPARK_HOME}"/jars/spark-sql_*.jar)" .jar)"; \
    scala_binary="$(echo "${spark_sql_jar}" | sed -E 's/^spark-sql_([0-9.]+)-.*$/\1/')"; \
    spark_version="$(echo "${spark_sql_jar}" | sed -E 's/^spark-sql_[0-9.]+-(.*)$/\1/')"; \
    package="org.apache.spark:spark-sql-kafka-0-10_${scala_binary}:${spark_version}"; \
    echo "Resolving ${package}"; \
    echo 'print("resolved")' > /tmp/resolve.py; \
    spark-submit --packages "${package}" --conf spark.jars.ivy=/tmp/ivy /tmp/resolve.py; \
    for artifact in spark-sql-kafka-0-10 spark-token-provider-kafka-0-10 kafka-clients commons-pool2; do \
        cp /tmp/ivy/jars/*"${artifact}"*.jar "${SPARK_HOME}/jars/"; \
    done; \
    ls "${SPARK_HOME}/jars" | grep -E 'kafka|commons-pool2'; \
    rm -rf /tmp/ivy /tmp/resolve.py

# Quieter Spark logs (WARN) for batch jobs.
COPY docker/spark/log4j2.properties ${SPARK_HOME}/conf/log4j2.properties

# Make `import pyspark` and `import imdb_project` work from plain `python` and
# `pytest` (spark-submit sets its own PYTHONPATH). Paths listed in a .pth file
# are resolved at interpreter start-up, so the bind-mounted source is found.
RUN set -eux; \
    site_dir="$(python -c 'import site; print(site.getsitepackages()[0])')"; \
    { \
        echo "${SPARK_HOME}/python"; \
        ls "${SPARK_HOME}"/python/lib/py4j-*-src.zip; \
        echo "/home/jovyan/project/src"; \
    } > "${site_dir}/imdb_project.pth"; \
    cat "${site_dir}/imdb_project.pth"

USER ${NB_UID}

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && \
    python -c "import pyspark, yaml, requests, confluent_kafka; print('pyspark', pyspark.__version__)"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYSPARK_PYTHON=python \
    PYSPARK_DRIVER_PYTHON=python

WORKDIR /home/jovyan/project
