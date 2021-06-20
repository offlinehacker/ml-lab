FROM mcr.microsoft.com/vscode/devcontainers/miniconda:0-3

# Copy environment.yml to a temp location so we update the environment.
COPY environment.yml /tmp/conda-tmp/
RUN if [ -f "/tmp/conda-tmp/environment.yml" ]; then /opt/conda/bin/conda env update -n base -f /tmp/conda-tmp/environment.yml; fi \
    && rm -rf /tmp/conda-tmp

RUN mkdir /home/vscode/.kaggle && chown vscode /home/vscode/.kaggle
VOLUME /home/vscode/.kaggle