FROM mcr.microsoft.com/devcontainers/python:3.11

# Used by Geopandas's subdependency fiona
RUN sudo apt update && sudo apt-get install libgdal-dev