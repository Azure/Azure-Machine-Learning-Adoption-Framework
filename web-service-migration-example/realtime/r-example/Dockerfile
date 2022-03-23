FROM rstudio/plumber

# install the dependent R packages
RUN R -e "install.packages('caret', dependencies=TRUE, repos='http://cloud.r-project.org')"
RUN R -e "install.packages('elasticnet', dependencies=TRUE, repos='http://cloud.r-project.org')"
# code
COPY scripts /var/azureml-app/scripts

# set working directory to root folder of scripts
WORKDIR /var/azureml-app/scripts
CMD ["/var/azureml-app/scripts/plumber.R"]

