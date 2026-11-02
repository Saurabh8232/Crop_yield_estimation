# Project overview

## Objective

Provide a transparent web application that estimates the dataset's historical
crop Yield from location, crop, season, environmental, soil, fertilizer, and
pesticide features.

## Problem statement

Agricultural records contain mixed numeric and categorical variables. The
project demonstrates a reproducible tabular ANN workflow and exposes the
result through a usable API and dashboard without inventing live measurements
or changing the source data.

## Approved model inputs

`Year`, `State`, `District`, `Crop`, `Season`, `Temperature`, `Rainfall`,
`Humidity`, `Soil Type`, `pH`, `Nitrogen`, `Phosphorus`, `Potassium`,
`Fertilizer`, and `Pesticide`.

The target is `Yield`. Its physical unit and precise definition are not
specified by the dataset.

## Scope boundary

The system performs retrospective, season-level historical crop yield
estimation. It is not an operational pre-season or during-season forecasting
system and does not claim real-time IoT functionality.
