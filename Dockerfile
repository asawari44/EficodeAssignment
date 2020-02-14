FROM python
COPY . /tmp/
RUN pip install requests
RUN pip install Flask==0.10.1
RUN pip install geopandas
RUN pip install geopy
CMD ["python", "/tmp/server.py"]
