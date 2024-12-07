FROM nginx:alpine

# install dependencies
RUN pip install pandas \
	&& pip install numpy \
	&& pip install ipywidgets \
	&& pip install matplotlib \
	&& echo "Installed the necessary dependencies"

COPY . /usr/share/nginx/html