This repo is made for real-time tracking of virus 2019-nCoV.

Show the report on a [web page](http://47.100.88.239:8080/).

![image](https://github.com/1813927768/virus-report/blob/master/web/image/2019-nConv_report_national_01-28%2013h.jpg)

## StartUp

1. Edit the `config.json` file to make your own setting.
2. `nohup python3 spider/scheduler.py`
3. `nohup http-server ./web`


> Requirements: Need some preparations for this program.
>
> 1. [`http-server`](https://blog.csdn.net/qq_37928350/article/details/81166873) in Node
> 2. some python requirements for spider

## Code 

### ./spider

The entrance of spider program is in `scheduler.py`. You can schedule your plot for any region at any interval by calling `schedulePlot()`.

### ./web

We use `http-server` in Node to show the output image in `index.html`.