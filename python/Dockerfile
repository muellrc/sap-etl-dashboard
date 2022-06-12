FROM prefecthq/prefect:latest-python3.9
RUN mkdir etl
COPY . etl/
RUN pip install psycopg2-binary
RUN pip install pandas
RUN pip install pyodata
RUN pip install sqlalchemy
CMD python etl/etl.py