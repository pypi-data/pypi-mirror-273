# AGI

Consider the Unix philosophy, as documented by Doug McIlroy in the Bell System Technical Journal from 1978:

"Make each program do one thing well. To do a new job, build afresh rather than complicate old programs by adding new features"

In that spirit, this library `agi` does one thing really well: calculate adjusted gross income. To use it:

```python
from agi import calculate_agi

gross_income = 100000
adjustments = 15000
agi = calculate_agi(gross_income, adjustments)
print(f'Adjusted Gross Income: {agi}')
```