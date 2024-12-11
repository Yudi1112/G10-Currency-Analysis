# G10 Currencies - Tane Frei, Yudi, Migjen

## Question: Which of the G10 currencies is the riskiest to hold for a Swiss resident?

### G10 Currencies:

- United States Dollar (USD)

- Euro (EUR)

- Pound Sterling (GBP)

- Japanese Yen (JPY)

- Australian Dollar (AUD)

- New Zealand Dollar (NZD)

- Canadian Dollar (CAD)

- Swiss Franc (CHF)

- Norwegian Krone (NOK)

- Swedish Krona (SEK)

### Overview

This project seeks to answer the question: "Which of the G10 currencies is the riskiest to hold for a Swiss resident?"

In pursuit of answering this question, we were able to determine multiple financial metrics. In our Jupyter Lab we created an interactive app where you are able to look at different charts that demonstrate these financial metrics over the years. In addition to this we were able to determine a few other non-financial metrics that are explained in our paper written in Latex.

The Instructions to use both of these appliances you will find below:

#### Docker

To open our interactive jupyter app follow these steps:

1. Download and Install Docker Desktop
2. Make sure Docker Desktop is running
3. In your Terminal, navigate to "it-research-project"
4. Enter Code: "docker build -t G10_Currencies ." --> this creates the docker image
5. Enter Code: "docker run -p 8888:8888 g10_currencies" --> this runs the container and also starts the jupyter lab app
6. Open your local host or click on the link given in the terminal to view the App
7. Make sure to run the code in the jupyter notebook so you are able to see the figures and graphs

To open the Paper written for this project, you need to copy it from the container to your local environment (make sure you have built the image and are running the container as shown above):

1. Open a Terminal
2. Enter Code: "docker ps" --> this will show you what the container id is of the running container
3. Enter Code: "docker cp 90963f0b3aba:/G10_Currencies/reports/text/paper/report.pdf ."
   --> This will copy the pdf to your local environment
4. Open the pdf with your prefered pdf viewer
   --> With windows: "start ./report.pdf"

#### Conclusion

In conclusion it seems the Japanese Yen was the riskiest to hold based on historical performance. However it very much depends on the definition of risk. If you include geopolitical and other non-financial metrics this answer might change. However this project should give a first overview as well as a few insights in regards to this question. Further analysis can be done using this project as a starting point.
