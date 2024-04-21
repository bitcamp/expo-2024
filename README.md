# Expo App 2024
This is the repository for the Expo App for Bitcamp 2024. 

The purpose of expo is to automate the reading and loading of Bitcamp hack submissions in order to create the judging schedule during the hack judging period. For Bitcamp 2023, we used Technica's stack 
with React, Mongo, Docker, and Flask; however, given our pivot to Vue + AWS, we felt that the recreation of the project was necessary. 

Old repo: https://github.com/bitcamp/hackathon-expo-app

# Process
Our goal is to read the `.csv` Devpost submission file, scrape the projects + their prize categories, and create a schedule table for ecah team according to their chosen prize categories, the
judging pool, and the allotted judging time (normally 2.5-3 hours). 

This algorithm is nontrivial and quite complicated. We will document the methodology we use when we get to it.

# Tech Stack
Our tech stack mimics the [portal](https://github.com/bitcamp/portal) registration app, but modernized to use the latest versions of Vue + AWS. We will be using Nuxt3 + Vue3 for the frontend and 
Lambda API functions + DynamoDB for the backend (all controlled using https://serverless.com). 

This project is a complete redesign and reconstruction of previous years and will hopefully be adopted in the upcoming years. 

