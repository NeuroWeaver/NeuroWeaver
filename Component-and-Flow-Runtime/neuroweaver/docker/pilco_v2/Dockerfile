FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


COPY . .

ENV PYTHONPATH=.:qfdfg:esa:runtime:compiler

RUN git clone https://github.com/nrontsis/PILCO && cd PILCO && \
    python setup.py develop && \
    cd ..

RUN apt-get update
RUN apt-get install vim -y
CMD ["python", "run_app.py", "cnf/pilco_v2.py"]
