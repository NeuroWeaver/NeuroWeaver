FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=.:qfdfg:esa:runtime:compiler

RUN pip install -e GPflow-0.5.0 && \
    pip install -e GPflowOpt

#CMD ["python", "MeanFieldModel_multithreading_BO_for_Neuroweaver.py"]
CMD ["./run.sh", "cnf/cnf_meanfield.py"]
