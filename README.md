# Reddit Genealogy

This repository provides a quick visualization of the genealogy graph of a few Reddit communities. Please refer to our papers for details. If you have any questions, please contact <jasonzhang@colorado.edu>.


## Notes:
Python 3.7+ is required.

The `requirements.txt` file should list all Python libraries that your scripts depend on, and they will be installed using:
```
pip install -r requirements.txt
```

## How to run the codes?
There is an example in main.py, you can run "python main.py" to download data from from [Pushshift API](https://ojs.aaai.org/index.php/ICWSM/article/view/7347) and then draw the genealogy graph. 

![alt text](http://jasondarkblue.com/images/genealogy.png)
The genealogy graph of a sample of COVID-related communities.

## Reference
If you find the code helpful, please consider citing the paper:

> \[1\] Jason Shuo Zhang, Brian Keegan, Qin Lv, and Chenhao Tan. “Understanding the Diverging User Trajectories in Highly-related Online Communities during the COVID-19 Pandemic.” The International Conference on Web and Social Media (ICWSM 2021).

> \[2\] Chenhao Tan. “Tracing Community Genealogy: How New Communities Emerge from the Old.” The International Conference on Web and Social Media (ICWSM 2018).
