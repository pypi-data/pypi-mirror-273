## Find root directory simply

You can find the root directory intuitively, quickly and simply.

### Usage

1. Install by `pip install rootdir`
2. Add `__root__.py` to your root path.
3. `import rootdir`
4. use as `rootdit.root_dir(__file__)`

### example1

If you need root directory, you could get it simply.

```python
import rootdir

if __name__ == "__main__":
    print(rootdir.root_dir(__file__))
```

### example2

If you've found a directory for Python dependencies, you can solve it all at once with the following function.

```python
import rootdir
rootdir.root_dependency(__file__)
```

Now you can import Python dependencies from root directory. 

