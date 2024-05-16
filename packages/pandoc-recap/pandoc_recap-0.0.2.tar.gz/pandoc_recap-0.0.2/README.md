[![PyPI version](https://badge.fury.io/py/pandoc-recap.svg)](https://pypi.org/project/pandoc-recap/)

# pandoc-recap

Render a recap of the notes inside a document

## Example

Write a markdown file, define metadata variable,
and use them inside the with double brackets.

```mardown
# My advices in life

## Chapter 1 - Health

::: tip
Brush your teeth
:::

## Chapter 2 - Friendship

::: tip
Be nice
:::

## Conclusion

::: {#recap .tip .BulletList}
```

Then call the filter when you generate the document:

```
$ pandoc foo.md --filter=pandoc-recap
<h1 id="my-advices-in-life">My advices in life</h1>
<h2 id="chapter-1---health">Chapter 1 - Health</h2>
<div class="tip">
<p>Brush your teeth</p>
</div>
<h2 id="chapter-2---friendship">Chapter 2 - Friendship</h2>
<div class="tip">
<p>Be nice</p>
</div>
<h2 id="conclusion">Conclusion</h2>
<ul>
<li>Brush your teeth</li>
<li>Be nice</li>
</ul>
```

## Install

```
pip install pandoc-recap
```
