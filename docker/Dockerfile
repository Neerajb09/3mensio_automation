# Use the official Miniconda3 image as the base image
FROM continuumio/miniconda3:latest

# Set the working directory in the container
WORKDIR /app

# Copy the environment.yml file to the container
COPY environment.yml .

# Create the conda environment from the environment.yml file
RUN conda env create -f environment.yml

# Activate the conda environment
SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]

# Set the default command to keep the container running
CMD ["bash"]