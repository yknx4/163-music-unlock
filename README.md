163-music-unlock
----------------
163-music-unlock is a reversed proxy for NetEase Music clients,
which unlocks regional limitations, limited and paid songs.

网易云音乐客户端的反代，解除海外限制，并且可播放下架歌曲和付费歌曲（暂不能收藏）。

更新 [@qq316107934](https://github.com/qq316107934) 分享的收藏歌曲的方法：

> 点击下载，然后选择一个歌单，再把下载文件删除，就躺在歌单里了。亲测有效。

2016.4.5 增加一台分流服务器  
2016.4.4 迁移API服务器，加快版权歌曲的加载速度  

目前测试可用的网易云音乐客户端：  
* 安卓客户端   
* IOS客户端  
* OSX客户端  

当前可用host列表如下，如果加载速度缓慢可尝试换一个服务器:  

> 108.61.201.11  Vultr Tokyo  
> 103.27.77.201  香港SLHK  

Usage
-----
On your device, add a custom DNS rule to the `hosts` file:

    103.27.77.201 music.163.com

This can also be done in many ways. On a non-jailbroken IOS device, it's recommended
to use `Surge` to create configuration with custom DNS maps.

自行部署方法
----------
* 安装Python依赖  
```
# pip install flask requests
```

* 编译安装nginx，需要添加 [ngx_http_substitutions_filter_module](https://github.com/yaoweibin/ngx_http_substitutions_filter_module) 模块

* 将`server/nginx_conf.conf`复制到nginx配置目录中，并应用该配置文件

* 直接运行`python server/runapi.py`即可运行开发服务器

* 建议在生产环境中使用简单的`gunicorn`容器提高性能：  
首先安装gunicorn:  
```
# pip install gunicorn
```
写一个启动脚本（或者你可以写一个gunicorn配置文件）：  
```
#!/bin/sh
cd /root/163-music-unlock/server	#替换为本项目下的server目录
/usr/local/bin/gunicorn -w 16 runapi:app -b 0.0.0.0:5001 --access-logfile /var/log/gunicorn.access.log --error-logfile /var/log/gunicorn.error.log --log-file /var/log/gunicorn.log
```

* 解决无法查看用户信息和用户歌单的问题（原因是这部分API使用https而非http，因此需要转发https请求）：    
首先在`/etc/sysctl.conf`中，设置`net.ipv4.ip_forward=1`，然后运行`sysctl -p`  
然后在`iptables`中增加转发规则：  
```
# iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination 223.252.199.7:443
# iptables -t nat -A POSTROUTING -j MASQUERADE
```
