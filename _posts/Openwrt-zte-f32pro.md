# openwrt-zte-f32pro
openwrt通过usb使用zxic随身wifi

## 安装依赖包
```shell
opkg update
opkg install usb-modeswitch kmod-usb-serial kmod-usb-serial-option kmod-usb-net-cdc-ether usbutils  kmod-usb-net-rndis
```
## 获取usb设备标识
以我手上的随身wifi为例子，在未进行任何改动的情况下，将其插入usb口后，在openwrt输入命令`lsusb`得到的是:
```
Bus 001 Device 007: ID 19d2:0548 DEMO,Incorporated DEMO Mobile Boardband
```
且ip addr show 没有usb eth* 对应，dmesg 显示 unsigned rndis device 
这时候是一个usb模式配置错误的设备，识别符为`19d2:0548`。

但是如果将其插入到linux电脑的usb口，在以太网端口出现后，输入`lsusb`得到的是:
```
Bus 001 Device 046: ID 19d2:0536 ZTE WCDMA Technologies MSM ALK Mobile Boardband
```
或者随便插到一台Windows电脑，设备管理器通过驱动安装时间、插拔定位到设备，然后查看其硬件id VID_19d2&PID_0581

所以对于这个设备，初始识别符为`19d2:0548`，目标识别符为`19d2:0581`。
## 写临时配置文件，测试
根据openwrt的文档:https://openwrt.org/docs/guide-user/network/wan/wwan/usb-modeswitching
，我们可以临时写一个usb-modeswitch的配置文件来测试能否正常切换模式，这里的messages是负责弹出当前usb模式的，因为不同设备对应messages不同，所以多列举了几个

在写配置文件的时候，要将目标识别符的冒号两端分别由16进制转换为10进制，同样以我手上的设备为例：  
`19d2:0581`:  

`0x19d2`->`6610`  

`0x0581`->`1409`  

我们就可以写一个测试用的json文件：
```json
{
        "messages" : [
                "55534243123456780000000000000011062000000100000000000000000000",
                "5553424312345678000000000000061e000000000000000000000000000000",
                "5553424312345678000000000000061b000000020000000000000000000000"
        ],
        "devices" : {
                "19d2:0548": {
                        "*": {
                                "t_vendor": 6610,
                                "t_product": [ 1409 ],
                                "msg": [ 0 , 1 , 2]
                        }
                },
        },
}

```
我将这个文件放在`/root`目录，文件名为`usb-mode-custom.json`。
然后就来试一下这个文件:
```
usbmode -s -v -c /root/usb-mode-custom.json
```
这个时候我们再看`lsusb`的输出内容:
```
Bus 001 Device 007: ID 19d2:0581 DEMO,Incorporated DEMO Mobile Boardband
```
已经成功切换为以太网设备了，然后在看`ip addr show`，可以看到一个新增`eth1`，这个时候就可以通过luci来添加一个新的以太网设备，使用dhcp，防火墙为wan，使用随身wifi的数据了。

## 写入usb-modeswitch系统配置
打开`/etc/usb-mode.json`，将临时配置文件中`devices`里面的内容写到系统配置里面的`devices`里面，我的就是：
```json
#/etc/usb-mode.json
...
  "devices":{
#这里开始粘贴
  		"19d2:0548": {
  			"*": {
  				"t_vendor": 6610,
  				"t_product": [ 1409 ],
  				"msg": [ 0 , 1 , 2 ]
  			}
  		},
#这里结束粘贴，注意msg是usb-mode的message消息队列的对应消息序号，如果有一天失效了，可能是meg写入别的消息导致对应序号发送消息不是原本那几条了，需要根据上面的发送消息记录查找回对应的消息序号进行更新
#或者直接再查看/root/usb-mode-custom.json
  }

...


```

这时候就可以自动切换usb模式了。

## 贡献：
https://github.com/fengjiongmax/openwrt-zxic-dongle
https://openwrt.org/docs/guide-user/network/wan/wwan/usb-modeswitching
https://openwrt.org/docs/guide-user/network/wan/wwan/ethernetoverusb_rndis
