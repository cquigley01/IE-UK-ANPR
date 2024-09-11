# Irish/UK Automatic Number Plate Recognition
- [@cquigley01](https://www.github.com/cquigley01)
- [@Colm McCarthy]


## Information

Configure main\entry.py & main\exit.py to use ether Windows or Linux (Raspberry Pi) by changing line 6.

Running the main files will, find the region of interest using the Russian Haarcascade Pre-Trained model, once a region of interest is found, the cropped image will be processed using different techniques available in the openCV library. Lighting conditions will strongly affect the results of this program. The Irish and UK lincese plate standards contain characters which look very similar such as 1 and I for example. The use of regular expressions enforce certain formats. I.E 131-D-36617 & 08-D-1273 are deemed valid. Refer to this test case in the test folder for testing the regular expression. A sucessfull text extraction is determined by detected a string atleast 5 times in 10 attempts, this is configurable. 
```
irish_plate_pattern = re.compile(r'^(\d{2,3})(1|2)?[A-Z]{1,2}\d{1,6}$', re.IGNORECASE)
uk_plate_pattern = re.compile(r'^([A-Z]{2}\d{2}[A-Z]{3})|([A-Z]{3}\d{1,4})$', re.IGNORECASE)

```
This repo is 1 of 2 parts of this project, where part 2 is the Flutter based frontend which contains a stripe API allowing the customer to pay via app and exit the car park. 

I have no further plans to maintain or re-visit this project. 




## Features

- Find a registration plate in a photo
- Extract text from the region of interest
- Image manipulation
- REST 

