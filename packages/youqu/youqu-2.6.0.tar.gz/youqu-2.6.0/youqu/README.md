<p align="center">
  <a href="https://linuxdeepin.github.io/youqu">
    <img src="./docs/assets/logo.png" width="520" alt="YouQu">
  </a>
</p>
<p align="center">
    <em>YouQu（有趣），一个使用简单且功能强大的自动化测试基础框架。</em>
</p>




[![GitHub issues](https://img.shields.io/github/issues/linuxdeepin/youqu?color=%23F79431)](https://github.com/linuxdeepin/youqu/issues)
[![PyPI](https://img.shields.io/pypi/v/youqu?style=flat&logo=github&link=https%3A%2F%2Fpypi.org%2Fproject%2Fyouqu%2F&color=%23F79431)](https://pypi.org/project/youqu/)
![Static Badge](https://img.shields.io/badge/UOS%2FDeepin/openEuler-Platform?style=flat&label=OS&color=%23F79431)

[![Downloads](https://static.pepy.tech/badge/youqu)](https://pepy.tech/project/youqu)
[![Hits](https://hits.sh/github.com/linuxdeepin/youqu.svg?style=flat&label=visitors&color=blue)](https://github.com/linuxdeepin/youqu)

---

<a href="https://github.com/linuxdeepin/youqu" target="_blank">GitHub</a> | <a href="https://gitee.com/deepin-community/youqu" target="_blank">Gitee</a>

<a href="https://linuxdeepin.github.io/youqu" target="_blank">在线文档</a>

---

YouQu(有趣)是统信公司(Deepin/UOS)开源的一个用于 Linux 操作系统的自动化测试框架，支持多元化元素定位和断言、用例标签化管理和执行、强大的日志和报告输出等特色功能，同时完美兼容 X11、Wayland 显示协议，环境部署简单，操作易上手。🔥

## YouQu（有趣）能做什么

- [x] 💻 Linux 桌面应用 UI 自动化测试
- [x] 🌏 Web UI 自动化测试
- [x] 🚌 Linux DBus 接口自动化测试
- [x] 🚀 命令行自动化测试
- [x] 🕷️ HTTP 接口自动化测试
- [ ] ⏲️ Linux 桌面应用性能自动化测试
- [ ]    💥 Fuzzy Desktop 桌面模糊测试

## 安装

从 PyPI 安装:


```shell
$ sudo pip3 install youqu
```

<details> 
<summary>不加 sudo ?</summary> 
<pre>
其实不加 sudo 也是可以的：<br>
  pip3 install youqu<br>
但某些情况下可能出现 youqu-startproject 命令无法使用，这是因为不加 sudo 时，安装包路径是在 $HOME/.local/lib/pythonX.X/site-packages，而此路径可能不在环境变量（PATH）中，您可以通过添加环境变量的方式使用 youqu-startproject 命令：<br>
  export PATH=$PATH:$HOME/.local/lib/pythonX.X/site-packages<br>
</pre>
</details>

## 创建项目

您可以在任意目录下，使用 `youqu-startproject` 命令创建一个项目：

```shell
$ youqu-startproject my_project
```

如果 `youqu-startproject` 后面不加参数，默认的项目名称为：`youqu` ；

![](./docs/assets/install.gif)

## 安装依赖

安装部署 YouQu 执行所需环境： 

```shell
$ cd my_project
$ bash env.sh
```

## 创建 APP 工程

使用 `startapp` 命令自动创建 APP 工程：

```shell
$ youqu manage.py startapp autotest_deepin_some
```

自动创建的 APP 工程遵循完整的 PO 设计模式，让你可以专注于用例和方法的编写维护。

在 `apps` 目录下会自动创建一个 APP 工程：`autotest_deepin_some`，同时新建好工程模板目录和模板文件：

```shell
my_project
├── apps
│   ├── autotest_deepin_some  # <-- APP 工程
...     ├── ...
```

在你的远程 Git 仓库中，只需要保存 APP 工程这部分代码即可。

`autotest_deepin_some` 是你的  APP 工程名称，在此基础上，你可以快速的开始你的 AT 项目，更重要的是确保创建工程的规范性。

`apps` 目录下可以存在任意多个 APP 工程。

运行
-------

### 1. 执行管理器

在项目根目录下有一个 `manage.py` ，它是一个执行器入口，提供了本地执行、远程执行等的功能。

### 2. 本地执行


```shell
$ youqu manage.py run
```

#### 2.1. 命令行参数

在一些 CI 环境下使用命令行参数会更加方便：


```shell
$ youqu manage.py run -a apps/autotest_deepin_some -k "xxx" -t "yyy"
```

更多用法可以使用 `-h` 或 `--help` 查看。

#### 2.2. 配置文件

通过配置文件配置参数

在配置文件 [setting/globalconfig.ini](https://github.com/linuxdeepin/youqu/blob/master/setting/globalconfig.ini)  里面支持配置对执行的一些参数进行配置。

### 3. 远程执行

远程执行就是用本地作为服务端控制远程机器执行，远程机器执行的用例相同。

使用 `remote` 命令：


```shell
$ youqu manage.py remote
```

## 贡献

[贡献文档](https://github.com/linuxdeepin/youqu/blob/master/CONTRIBUTING.md) 


## 开源许可证

YouQu 在 [GPL-2.0](https://github.com/linuxdeepin/youqu/blob/master/LICENSE) 下发布。
