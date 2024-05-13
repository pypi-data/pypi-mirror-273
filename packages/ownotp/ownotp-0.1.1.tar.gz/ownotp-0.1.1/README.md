# OTP Generator
Generate a time-based OTP using SHA-256 hashing algorithm. 

### Installation
You can install the package using pip:
```shell
pip install ownotp
```

### Usage
Create 6 digits otp. OTP will change 2 minutes once based on `your_own_secrent`.
```python
from ownotp.otp import generate_otp

otp = generate_otp('your_own_secret')
print(otp)
```
To change interval time pass the value in seconds.
```python
from ownotp.otp import generate_otp
otp = generate_otp('your_own_secret', interval=120)
```

To generate different length OTP.

Note: Minium 4 and Maximum 8 length will support. If condition not satisfied default length will take to generate OTP.
```python
from ownotp.otp import generate_otp
otp = generate_otp('your_own_secret', length=7)
```
To get hashed OTP. Mixed of char and numbers
```python
from ownotp.otp import generate_otp
otp = generate_otp('your_own_secret', only_digits=False)
```