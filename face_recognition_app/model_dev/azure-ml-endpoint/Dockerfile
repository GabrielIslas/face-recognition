FROM mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04

WORKDIR /

ENV CONDA_PREFIX=/azureml-envs/face-recog
ENV CONDA_DEFAULT_ENV=$CONDA_PREFIX
ENV PATH=$CONDA_PREFIX/bin:$PATH

# Create conda environment
COPY environment.yaml .
RUN conda env create -p $CONDA_PREFIX -f environment.yaml -q && \
    rm environment.yaml && \
    conda run -p $CONDA_PREFIX pip cache purge && \
    conda clean -a -y

RUN pip install azureml-inference-server-http

RUN pip install azureml-mlflow