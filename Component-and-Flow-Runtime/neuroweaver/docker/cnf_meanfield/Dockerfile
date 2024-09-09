FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


COPY . .

ENV PYTHONPATH=.:qfdfg:esa:runtime:compiler

RUN wget -c https://github.com/GPflow/GPflow/archive/refs/tags/0.5.0.tar.gz
RUN tar -xf 0.5.0.tar.gz 
RUN git clone https://github.com/GPflow/GPflowOpt
RUN pip install -e GPflow-0.5.0 && \
    pip install -e GPflowOpt

CMD ["python", "run_app.py", "cnf/cnf_meanfield.py", "--infinite"]
