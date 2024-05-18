**About**

A wrapper of AWS S3 (boto3) that facilitate some operations. 

**Usage**

```python 

is_public = True

bs3 = BetterS3("bucket name", "AWS_SECRET_ACCESS_KEY", "AWS_ACCESS_KEY_ID", "AWS_REGION")

# Single file
bs3.upload(f"sub_folder/another_folder/", "test1.py", is_public, use_default_progress_bar=True)

# Multiple files
bs3.upload(f"sub_folder/another_folder/", ["test1.py", "test2.py"], is_public)
```
