# K-Anonymity Mobile Location Privacy

A tool that implements the algorithm presented in the paper [Location Privacy in Mobile Systems: A Personalized Anonymization Model](http://ieeexplore.ieee.org/document/1437123) to achieve k-anonymity on location data. Link to our own paper: [Implementing & Comparing Noise Addition by Satisfying Geo-indistinguishability & Aggregating Data for k-Anonymity]

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for testing and analysis of location data.

## Pre-setup

Clone the repository
Navigate to the project directory
Run the following command to install the required packages:

```bash
pip3 install -r requirements.txt
```

Then the project is ready to be run.

Example:

```bash
python3 main.py data.csv 3 0.5 0.5
```

## Algorithm Details

The algorithm takes in a CSV file with Latitude, Longitude, Name, and OBJECTID attributes and performs the following steps:

- Creates grid cells of size dx x dy and hashes their centers to form a grid map
- Maps each data point to its corresponding grid cell and calculates its anonymity set size
- If a data point's anonymity set size is less than the specified k-value, the grid cell size is increased and the process is repeated
- If increasing the grid cell size does not increase the anonymity set size to the required k-value, the data point is considered untreatable
- Prints all bounding boxes with their hashed IDs and the number of untreatable instances
