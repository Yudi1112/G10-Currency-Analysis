# Use Miniconda as the base image
FROM continuumio/miniconda3:latest

# Copy the project files to the container
COPY . .

# Create and activate the conda environment
RUN conda env create -f environment.yaml

# Ensure Conda environment is activated for all subsequent RUN commands
SHELL ["conda", "run", "-n", "G10_Currencies_3.13", "/bin/bash", "-c"]

# Install JupyterLab and additional dependencies
RUN conda install -n G10_Currencies_3.13 -c conda-forge jupyterlab notebook nbconvert nbclient
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt



# Expose JupyterLab's default port
EXPOSE 8888

# Command to run JupyterLab when the container starts
CMD ["conda", "run", "--no-capture-output", "-n", "G10_Currencies_3.13", "jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--NotebookApp.token=''","--NotebookApp.password=''"]

