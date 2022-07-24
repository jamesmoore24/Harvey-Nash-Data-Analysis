# Harvey Nash Group Digital Leadership Report 2021: A Formal Analysis

The Harvey Nash Group Digital Leadership Report, carried out by the MIT Center for Information Systems Research, surveyed 1,996 company executives (CIOs, heads of tech, CTOs, CDOs, CEOs, CMOs, COOs, CFOs) on topics that include but are not limited to business strategy, leadership, carbon footprint, performance relative to competitors, impact of COVID, skills shortages, talent retention, staff diversity/inclusion, budgeting, company organization, cyber-security, and innovation in the workplace. 

## About:

Uses popular python data manipulation packages such as ```pandas```, ```numpy``` and ```mathplotlib``` through the ```scipy``` distribution to carry out data cleaning, analysis and visualization. Uses ```selenium``` and the [Chromium webdriver](https://chromedriver.chromium.org/) to parse through public and private companies. Uses ```fmpsdk``` (Python SDK provided by [Financial Modeling Prep (FMP)](https://site.financialmodelingprep.com/)) and [Wharton WRDS](https://wrds-www.wharton.upenn.edu/) to obtain public company financial data. 

---

## Documentation

### Getting Started:

- This program can run on Windows, Mac and Linux operating system by using valid python text editors with the python version 3.x
- This program is developed by python 3.x.
- Must download ```pandas```, ```numpy```, and ```mathplotlib``` using pip if not using [Anaconda Environment](https://docs.continuum.io/anaconda/), alternative ways to obtain packages are [here](https://scipy.org/install/).
- It is more secure which means you may not enter other anything except the numerical values.
- It is more relevant and easy to use for an user.

### Problem Statement: 

Need to perform data analysis and visualization on the results of the Harvey Nash Group Digital Leadership Report 2021 to find trends between answers in the survey and companies financial performance.

### Approach:

COMPLETED:
1. Parse through companies listed on the survey to determine whether public or not.
2. Obtain key performance indicators (kpi's) through financial data repositories (WRDS and FMP)
3. Clean data (5% trimmed mean) and relate relative to industry data standard for that period 
4. Compare data to [GICS](https://www.msci.com/our-solutions/indexes/gics)industry sector averages (from WRDS, GICS sectors information from fidelity.com) and obtain % ratio information

HERE:
5. Perform regressions on data to determine relationships between survey answers and financial performance for publicly listed companies (r>0.4).
6. Visualize regressions using available packages (listed above)
7. Create company briefing using kpi, visual and quantitative information including case-study of at least one "standout" company

### Takeaways:
TBD
