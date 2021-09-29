## NOTE!
Results may vary A LOT when attacking! It might peak at 40k rq/s and drop down to 2k rq/s or peak at 169 requests per second, just so you know!

--- 

### about
Current version: 5.0.
This script is for volumetric layer 7 attacks, not for stealthy and powerfull attacks!

---

### features
1. Ability to attack HTTPS sites

---

### known bugs/problems
1. Timing is a bit egh, because thread 1 is already busy attacking when thread 70 just started (for example)
2. Proxies get obliterated when attacking (need to fix)
4. Sometimes script gives "Fatal Python" errors, just ignore them and restart the tool if neccesary

---

### to do list
1. Better exception handling
2. ....

---

### usage
All options:
```
python3 amyntas.py -h
```

Basic usage:
```
python3 amyntas.py -t https://target.com
```

Brute power, 700 threads hammering for 40 seconds:
```
python3 amyntas.py -t https://target.com -w 700 -d 40
```

---

### images
Note, these are a bit old because i am too lazy to make new screenshots lmao

23k requests per second
![23k](https://github.com/Switch1024/amyntas/blob/main/images/23k_dstat.png?raw=true)

30k requests per second
![30k](https://github.com/Switch1024/amyntas/blob/main/images/30k_dstat.png?raw=true)

507k requests per second
![507k](https://github.com/Switch1024/amyntas/blob/main/images/507k_dstat.png?raw=true)
