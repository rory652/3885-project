# About

## Project Description

This is our Group Design Project for ELEC3885. The aim of our project is to be able to track the spread of Covid-19 within a care home. To do this, we have split this project into 4 stages:

 - Wearables: worn by the residents, featuring Bluetooth technology.
 - Detection Modules: to detect the positions of the wearables. Uses Bluetooth 5.1 AoA (Angle of Arrival) and AoD (Angle of Departure).
 - Back-end: Takes data from Detection Modules and processes it, detect contact between residents and make that accessible through a REST API.
 - Front-end: App and Website allowing care home workers to see who needs to be tested and report cases

### Project Diagram

``` mermaid
graph LR
    W1[Wearable 1]
    W2[Wearable 2]
    W3[Wearable n]

    DM1[Detection Module 1]
    DM2[Detection Module 2]
    DM3[Detection Module n]

    BE[Back-end]
    FE[Front-end]

    W1 & W2 & W3 --> DM1 & DM2 & DM3
    DM1 & DM2 & DM3 --> BE
    BE --> FE
```

## API Description

This documentation focuses on the back-end REST API, containing detailed information on the various endpoints and how to access them.