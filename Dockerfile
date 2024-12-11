# Use Miniconda as the base image
FROM continuumio/miniconda3:latest

# Set the working directory in the container
WORKDIR /G10_Currencies

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

# Install TeX Live for LaTeX compilation
RUN apt-get update && apt-get install -y texlive-full --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Compile the LaTeX file to PDF and save it in the same folder as the .tex file
RUN cd "it-research-project/G10_Currencies/reports/text/paper" && pdflatex report.tex

# Expose JupyterLab's default port
EXPOSE 8888

# Command to run JupyterLab when the container starts
CMD ["conda", "run", "--no-capture-output", "-n", "G10_Currencies_3.13", "jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--NotebookApp.token=my_fixed_token"]

