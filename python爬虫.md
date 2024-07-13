## http请求方式

- get：直接从服务器请求内容

  ```python
  import request
  url = 'https://www.sogou.com/web?query=周杰伦'
  dic = {
      'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36 Edg/126.0.0.0'
  }
  response = request.get(url, header=dic)
  print(response)
  ```

- post：发送一些数据，并请求内容

  ```python
  import request
  url = 'https://fanyi.baidu.com/sug'
  dic = {
      'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36 Edg/126.0.0.0'
  }
  dat = {
      'kw':'dog'
  }
  response = request.post(url, header=dic, data=dat)
  print(response.json)
  ```

## 封装参数

```python
url = 'https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start=0&limit=20'
response = request.post(url)
```

url中?后的都是参数，可以对这些参数进行封装。

```python
url = 'https://movie.douban.com/j/chart/top_list'
param = {
	type：11,
    interval_id:100%3A90,
    action:'',
    start:0,
    limit:20
}
response = request.post(url, params=param)
```

