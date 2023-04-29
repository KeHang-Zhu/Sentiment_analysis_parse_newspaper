# Regional variation of negative sentiment during Great Depression through newspaper articles using NLP

## Motivation
The causes behind the severity and longevity of the Great Depression have been extensively studied by economists and historians. In comparison to the 2008 Great Financial Crisis, there is limited data availability on the Great Depression, making it challenging to obtain detailed and comprehensive information on the economic conditions of the time. The structured data that I create could provide a more complete picture of the sentiment and topics covered in newspaper articles during that era, and shed light on the economic and social conditions of the time. Understanding the factors that contributed to the Great Depression's severity and duration is crucial to gain a deeper understanding of its impact on people, institutions, and governments.


## Workflow
<p align="center">
  <img src="process.png" alt="Your Image" width="650" >
</p>


### Step1: Searching databases of newspapers from the 1930s.

Some relevant databases include:
- ProQuest Historical Newspapers
- Chronicling America
- Newspapers.com
- Gale Primary Sources
- NewspaperArchive.com

In this work, we use Chronicling America, operated by the Library of Congress, primarily as the data source since it is already in text format and allows for data scraping

### Step2: Image to Text

Use Optical Character Recognition (OCR) techniques to extract text from the identified regions. 
This will allow me to convert text in the newspaper articles from images to machine-readable text.

### Step3:  Data cleaning

Break the OCR into 100-200 word chunks, then drop chunks with <90% (or so) word rate. Perform text pre-processing techniques such as tokenization, stemming, and stop-word removal to prepare the text for analysis. This will clean and normalize the text data for sentiment analysis and topic modeling.

### Step4: Sentiment analysis

Here, we mainly use Roberta as out sentiment analysis tool. Roberta is a state-of-the-art natural language processing (NLP) model developed by Facebook AI that uses a modified training approach to achieve high performance on NLP tasks such as language understanding, text classification, and question answering. It can learn from large amounts of text data in an unsupervised manner and is available as a pre-trained model that can be fine-tuned on specific tasks with relatively small amounts of labeled data. Roberta has been used in a variety of applications and has achieved impressive results in several NLP benchmarks.

In order to show the negative sentiment more clearly, we define the panic score function:
$Panic \ score = log(sentiment \  socre + 1)$

### Step5: the single data analysis (New York v.s. Connecticut)

<p align="center">
  <img src="Comparison.png" alt="Your Image" width="650" >
</p>


### Step6: Data Visualization

<p align="center">
  <img src="Heatmap_1920.png" alt="Your Image" width="650" >
</p>


Unfortunately, GitHub doesn't support embedding videos directly in README files. However, you can find the "heatmap_evolution_597.mp4" in the repo and download it to watch.



## Future steps:
1. Fine tuning off-the-shelf Roberta. Pick out articles about economic news/bankrupcy/small business need loans
