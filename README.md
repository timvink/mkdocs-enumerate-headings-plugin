![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkdocs-add-number-plugin)
![PyPI](https://img.shields.io/pypi/v/mkdocs-add-number-plugin)
![PyPI - Downloads](https://img.shields.io/pypi/dm/mkdocs-add-number-plugin)
![GitHub contributors](https://img.shields.io/github/contributors/timvink/mkdocs-add-number-plugin)
![PyPI - License](https://img.shields.io/pypi/l/mkdocs-add-number-plugin)

# mkdocs-add-number-plugin

[MkDocs](https://www.mkdocs.org/) plugin to automatically number the headings (h1-h6) in each markdown page. This only affects your rendered HTML and does not affect the markdown files.

## Setup

Install the plugin using pip:

```bash
pip install mkdocs-add-number-plugin
```

Next, add the following lines to your `mkdocs.yml`:

```yml
plugins:
  - search
  - mkdocs-add-number-plugin
```

> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set.

## Usage

Example of multiple options set in the `mkdocs.yml` file:

```yml
plugins:
    - search
    - mkdocs-add-number-plugin:
        increment_pages: True
        strict_mode: False
        order: 1
        excludes: 
        	- sql/
        	- command/rsync
        includes:
        	- sql/MySQL
```

> Note that each title in your markdown page must be contain a space after the heading tag: `# title` is correct, but `#title` will cause an error.

## Options

- `increment_pages`: When set to `True` (default), will increment the chapter number of each page sequentially.
- `strict_mode`:
   - When set to `False` (default), orders the title numbers in your HTML page sequentially
   - When set to `True` it will follow the headings order strictly. You must start writing documents from h1, and cannot skip headings (such as `# title1\n### title2\n`).
- `order`: Heading level to start counting (number). Default is `1`. Example use case: When you want to use the first title of a document as the title of a document and you don't want to number it, set it to `order: 2`.
- `excludes`: Exclude certain files or folders in the `docs/` folder. Default is None. To exclude entire folders, append a slash (`folder/`).
- `includes`: The syntax is similar to `excludes` and it meant to be used together. You could for example exclude an entire folder but include several files from that folder.

### Example of using `excludes`

For example, there is a mkdocs directory structure as follows:

```shell
$ tree .
.
├── docs
│ ├── command
│ │ ├── rsync.md
│ │ ├── sed.md
| ...
└── mkdocs.yml
```

To exclude rsync file, add the excludes option as follows:

```yaml
plugins:
     - search
     - mkdocs-add-number-plugin:
         excludes:
         	- command/rsync
```

If you want to exclude the command folder, add the excludes option as follows:

```yaml
plugins:
     - search
     - mkdocs-add-number-plugin:
         excludes:
         	- command/
```

------ CHINESE VERSION ------

# mkdocs-add-number-plugin

一个mkdocs插件：为你的每个页面的标题（h1~h6）自动编号。**这只影响你的html渲染结果，并不影响markdown文档本身！**

## 提供的选项

### strict_mode

指定编号的模式。

语法：

```yaml
strict_mode: True|False
```

2. True：严格模式。顺序地为你的html页面的标题编号。必须从h1开始撰写文档，且不能有跳级（比如`# title1\n### title2\n`，*title2*不会被编号，可以选用非严格模式为其编号），但是可以不必用到所有级数。
2. False：非严格模式（默认值）。顺序地为你的html页面的标题编号。没有上述的限制。

**注意**：两种模式的标题级数都不能有倒序出现。比如`### title1\n# title2\n`，这会导致编号异常。并且每个标题后面都要有空格与文字隔开，比如这样`# title`是正确的，而这样`#title`是不行的。

#### 效果

非严格模式效果：

![](img/none_strict_mode.png)

严格模式效果：

![](img/strict_mode.png)



### order

从第几个标题开始编号。在某些场景下是有用的：你想要将文档的第一个标题作为文档的题目而不想对其进行编号时，设置为`order: 2`。

语法：

```yaml
order: 数字
```

数字必须是自然数，默认值是1。

### excludes

排除某些文件或文件夹。

语法：

```yaml
excludes: 列表|'*'
```

- 列表：遵循`yaml`文件的列表语法，文件或文件夹填写`docs`文件夹下的相对路径，不必填写文件后缀。**以`/`或`\`结尾的值表示文件夹**。
- '*'：表示排除所有的文件。因为默认值为空列表`[]`，意味着对所有的文件进行编号，所以你需要使用此值来不对所有的文件进行编号。

#### 例子

比如现在有一mkdocs目录结构如下：

```shell
$ tree .
.
├── docs
│   ├── command
│   │   ├── rsync.md
│   │   ├── sed.md
|   ...
└── mkdocs.yml
```

想要排除rsync文件，添加的excludes选项如下：

```yaml
plugins: 
    - search
    - mkdocs-add-number-plugin:
        excludes: 
        	- command\rsync
```

若想要排除command文件夹，添加的excludes选项如下：

```yaml
plugins: 
    - search
    - mkdocs-add-number-plugin:
        excludes: 
        	- command\
```



### includes

包含某些文件或文件夹。

语法与`excludes`类似：

```yaml
includes: 列表
```

在被`excludes`排除的文件或文件夹如果在`includes`选项中出现，那么会对其进行编号。默认值为空列表`[]`。

**注意**：includes是作为excludes的辅助选项使用的（意味着必须和excludes一起使用，单独使用此选项没有意义）。



## 安装
有以下两种方法：
### 从源码构建安装
克隆此项目到你的计算机上，然后执行以下命令：

```shell
cd mkdocs-add-number-plugin
mkdir wheels
cd wheels
# if you have installed the plugin
# pip uninstall mkdocs-add-number-plugin -y
pip wheel ..
pip install mkdocs_add_number_plugin-*-py2-none-any.whl
```

### 使用 pip 安装

```shell
# if you have installed the plugin
# pip uninstall mkdocs-add-number-plugin -y
pip install mkdocs-add-number-plugin
```



## 使用

在`mkdocs.yml`文件中的`plugins`选项添加此插件：

```yaml
plugins: 
    - search
    - mkdocs-add-number-plugin:
        strict_mode: False
        order: 1
        excludes: 
        	- sql/
        	- command/rsync
        includes:
        	- sql/MySQL
```

