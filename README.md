# Post-Pages-to-IPFS

一个可以实时将 Markdown 渲染生成 Html 并上传到 IPFS 网络的 Web 服务。

![图片](https://user-images.githubusercontent.com/72449367/141116469-e7badb06-4094-4774-bd9d-99d51802d03c.png)

### 功能
1、实时在线编辑预览 Markdown 

2、渲染 Markdown 并上传到 IPFS 网络

-----

### 使用说明
#### 预览
顶部有三个选项卡，依次为**预览**、**编辑**与**发布**。`预览`界面会自动将`编辑选项卡`内的内容渲染成 HTML 。

#### 编辑
该界面是一个**编辑器**。你可以在这里输入文本、MD 格式文本和 HTML 源码。如果你觉得默认样式不好看，可以插入 css 自己美化页面甚至可以插入 js。

这些都会实时刷新并呈现在**预览选项卡内**。

你可能用得到的: [Markdown 基本语法](https://gateway.ipfs.lc/ipfs/QmaSM2eTCtJ3o6cn6XSnt9EqhwJcLw9KUriLoL3DvbV6Bu)



#### 发布
发布选项卡，确认发布后点击 **Post it!** 即可发布你编辑好的文本到 IPFS 网络。
由于 IPFS 网络的特殊性，一旦发布，即不可更改，并且理论上永久储存在互联网中。所以请确认没有错别字或敏感信息哦。

-----

### 如何工作？
后端使用 IPFS + Flask + Nginx，前端使用 Bootstrap + easy-markdown。如果哪里用的问题，欢迎提 issues 或 PR。

### 安装教程

```
git clone https://github.com/SaltyLeo/Post-Pages-to-IPFS
cd Post-Page-to-IPFS
python3 web.py
```

-----

### 其他
为了保证服务可持续性，发布功能每分钟仅限2次，如超出将会被封禁1分钟。请勿滥用资源。
如果觉得还不错，不妨 [**捐赠**](https://gateway.ipfs.lc/ipfs/QmQ6pzGftyCJNYXvAVWatj1Y36TQB8ptiDaRxdE7xRmtYS) 支持下~
