# mkdocs-index-plugin

一个mkdocs插件：为你的每个页面的标题（h1~h6）自动编号。这只影响你的html渲染结果，并不影响mkdown文档！

有两种模块可选：

1. 非严格模式（默认）。顺序地为你的html页面的标题编号。
2. 严格模式。顺序地为你的html页面的标题编号。必须从h1开始撰写文档，且不能有跳级（比如`# title1\n### title2\n`，*title2*不会被编号，可以选用非严格模式为其编号），但是可以不必用到所有级数。

## 效果

非严格模式效果：

![](img/none_strict_mode.png)

严格模式效果：

![](img/strict_mode.png)

**注意**：两种模式的标题级数都不能有倒序出现。比如`### title1\n# title2\n`，这会导致编号异常。

## 安装

克隆此项目到你的计算机上，然后执行以下命令：

```shell
cd mkdocs-index-plugin
mkdir wheels
cd wheels
# if you have installed the plugin
# pip uninstall mkdocs-index-plugin -y
pip wheel ..
pip install mkdocs_index_plugin-1.0.0-py2-none-any.whl
```

## 使用

在`mkdocs.yml`文件中的`plugins`选项添加此插件：

```yaml
plugins: 
    - search
    - mkdocs-index-plugin:
        strict_mode: False # 模式选项，True或False
```



--------------------------------The following is an English description that using Google Translate----------------------------

# mkdocs-index-plugin

A mkdocs plugin: Automatically number the title (h1~h6) of each page you have.This only affects your html rendering results and does not affect the mkdown documentation!

There are two modes available:

1. Non-strict mode (default). Order the title number of your html page sequentially.
2. Strict mode. Order the title number of your html page sequentially. You must start writing documents from h1, and you can't have skipping (such as `# title1\n### title2\n`, *title2* will not be numbered, you can use non-strict mode to number them), but you don't have to use all series.

## The effect

Non-strict mode effect:

![](img/none_strict_mode.png)

Strict mode effect:

![](img/strict_mode.png)

**Note**: The title levels of both modes cannot be reversed. For example `### title1\n# title2\n`, this will cause the number to be abnormal.

## installation

Clone this project to your computer and execute the following command:

```shell
cd mkdocs-index-plugin
mkdir wheels
cd wheels
# if you have installed the plugin，execute this：
# pip uninstall mkdocs-index-plugin -y
pip wheel ..
pip install mkdocs_index_plugin-1.0.0-py2-none-any.whl
```

## Instructions

Add this plugin to the `plugins` option in the `mkdocs.yml` file:

```yml
plugins: 
    - search
    - mkdocs-index-plugin:
        strict_mode: False # mode，True or False
```

