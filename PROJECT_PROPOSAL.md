# Project Proposal: Carbon Footprint AI Microservice

**Student Name**: Natasha Silvestre
**Bootcamp**: Ironhack Data Science & ML
**Date**: November 2025

## Project Overview

I propose to develop an AI-powered microservice designed to help building managers monitor and reduce their carbon footprint. The system will leverage historical energy data to predict future emissions and provide actionable sustainability recommendations.

The core functionality will include:
1.  **Predictive Analysis**: Using Machine Learning to forecast energy consumption and carbon emissions based on building characteristics and weather conditions.
2.  **Efficiency Classification**: A model to rate buildings on a sustainability scale (e.g., A to F), allowing for quick identification of inefficient structures.
3.  **Intelligent Assistance**: A Generative AI component (RAG-based chatbot) that can answer specific questions about energy efficiency and offer tailored reduction strategies.

## Dataset Selection

For this project, I have selected the **ASHRAE - Great Energy Predictor III** dataset from Kaggle.

**Dataset Description:**
This dataset provides a comprehensive view of energy usage in the built environment, consisting of:
*   **Scale**: Hourly meter readings from 1,448 buildings across various sites over a one-year period.
*   **Building Metadata**: Key characteristics such as square footage, primary use (e.g., Education, Office, Lodging), year built, and floor count.
*   **Energy Metrics**: Readings for four types of meters: Electricity, Chilled Water, Steam, and Hot Water.
*   **Weather Data**: Hourly observations including air temperature, dew point, wind speed, and cloud coverage.

**Relevance:**
This dataset is ideal for this project because it offers the granularity required to train robust regression and classification models. The combination of building metadata and weather patterns allows for complex feature engineering and deep analysis of factors contributing to energy inefficiency.

## Project Goal

The primary objective is to build an end-to-end data science solution. This involves the entire lifecycle: cleaning and preprocessing raw data, training and evaluating Machine Learning and Deep Learning models, and finally, deploying these models via a functional API to demonstrate real-world applicability.
