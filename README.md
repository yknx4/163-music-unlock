163-music-unlock
----------------
163-music-unlock is a reversed proxy for NetEase Music mobile app(Android & IOS),
which unlocks regional limitations, limited and paid songs.

网易云音乐客户端(安卓和IOS)的反代，解除海外限制，并且可播放下架歌曲和付费歌曲（暂不能收藏）。

更新[qq316107934](https://github.com/qq316107934)分享的收藏歌曲的方法：

> 点击下载，然后选择一个歌单，再把下载文件删除，就躺在歌单里了。亲测有效。

2016.4.4 迁移API服务器，加快版权歌曲的加载速度

Usage
-----
On your device, add a custom DNS rule to the `hosts` file:

    103.27.77.201 music.163.com

This can also be done in many ways. On a non-jailbroken IOS device, it's recommended
to use `Surge` to create configuration with custom DNS maps.
