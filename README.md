# Data engineer project

JDK is required to run Spark
Requirements are installed by running `pip install -r requirements.txt`

Data extraction and preparation is done by running / modifying `extract_files.py`

Data processing and visualization is done in `data_processing.ipynb` notebook


In points 4 & 5 lowest value of timestamp are seconds. Provided amount of events
don't suffice using greater granulation and anything lower than that only makes
the chart unnecessarily expanded. Since we are tracking human data we are mainly
interested what was happening in given second.