# ByteGG python!
This project allows you to:
- Easily bypass certain Roblox services, such as executors and scripts.
- Bypass ad links, including Linkvertise and Lootlinks.

### Installation Instructions
```bash
pip install bytegg
```

### Usage Examples

There is only one premium version available, and it requires an API key. For more information, send a direct message to "icmecodes" to obtain and purchase the key.

```python
import bytegg, asyncio

async def bypass(url):
    xd = await bytegg.bypass(url=url, api_key='XXXXXXXXXXXXXXXXXX-rlow')
    print(xd)

asyncio.run(bypass("https://linkvertise.com/377810/193.37974090560883/dynamic?_r=0bbeb5347ff0758f7854ee3e6b308ac1a9d1520fb7b1cb6c4faf6c6b24a9d33d&r=aHR0cHM6Ly9wYW5kYWRldmVsb3BtZW50Lm5ldC9nZXRrZXk%2Fc2VydmljZT10cmlnb24tZXZvJmh3aWQ9YWExODM4NTYtNmYwZS00M2U5LWE0NzktMmI2ODA5YmJkOGM1JnByb3ZpZGVyPWxpbmt2ZXJ0aXNlJnNlc3Npb250b2tlbj1mOTQzZTY1MzljYTAyMzYyYWYyZGY1NGU4ZDdiNmRhZGUyZTM5MWRkNWI1ODNlNzc4ZmQ5MDIxNzdjNjkzMzU4&o=sharing"))
```

### License
Distributed under the MIT License. See `LICENSE` for more information.

### Credits and Acknowledgments
Special thanks to icmecodes for the initial concept and to all beta testers who provided essential feedback.

### Contact
Contact me, rlow._. on discord
