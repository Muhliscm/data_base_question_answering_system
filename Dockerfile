FROM continuumio/miniconda3
WORKDIR /usr/src/app
COPY ./ ./
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "--no-capture-output", "-n", "myenv", "/bin/bash", "-c"]

EXPOSE 5003
# The code to run when container is started:
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "myenv", "python3", "src/app.py"]