from boto3.s3.transfer import ProgressCallbackInvoker, TransferConfig, create_transfer_manager, KB, MB
from botocore.config import Config as BotoConfig
from boto3 import client as boto_client
import sys
import os

class BetterS3():
  __multipart_chunksize   = 8   * MB
  __io_chunksize          = 256 * KB
  __progress_len          = 100
  __max_threads           = 10
  
  __progress_data         = None
  __client                = None
  __bucket                = None
  __secret                = None
  __region                = None
  __key                   = None
  
  def __init__(
    self, 
    bucket : str, 
    secret=None, 
    key=None, 
    region=None, 
    client=None, 
    multipart_chunksize=None,
    io_chunksize=None,
    progress_len=None,
    max_threads=None,
  ):
    self.__secret = secret
    self.__region = region
    self.__bucket = bucket
    self.__client = client
    self.__key = key
    
    self.__multipart_chunksize = multipart_chunksize if multipart_chunksize else self.__multipart_chunksize
    self.__io_chunksize = io_chunksize if io_chunksize else self.__io_chunksize
    self.__progress_len = progress_len if progress_len else self.__progress_len
    self.__max_threads = max_threads if max_threads else self.__max_threads
    
  def __progress_handler(self, chunk):
    pd = self.__progress_data
    
    first = (pd["bytes"] == 0)
    pd["bytes"] += chunk
    
    if (first):
      sys.stdout.write("[%s]" % (" " * self.__progress_len))
      sys.stdout.flush()
      sys.stdout.write("\b" * (self.__progress_len + 1))
    
    curr = int(self.__progress_len * (pd["bytes"] / pd["size"]))
    
    sys.stdout.write("-" * (curr - pd["pos"]))
    sys.stdout.flush()
    pd["pos"] = curr
    
    if (pd["bytes"] == pd["size"]):
      sys.stdout.write("]\n")
  
  def set_multipart_chunksize(self, size):
    self.__multipart_chunksize = size
  
  def set_io_chunksize(self, size):
    self.__io_chunksize = size
  
  def set_progress_len(self, size):
    self.__progress_len = size
  
  def __get_client(self):
    if (self.__client is None):
      self.__client = boto_client("s3", 
        config=BotoConfig(max_pool_connections=self.__max_threads),
        aws_secret_access_key=self.__secret, 
        aws_access_key_id=self.__key, 
        region_name=self.__region
      )
    
    return self.__client
  
  def __make_transfer_manager(self):
    return create_transfer_manager(self.__get_client(), TransferConfig(
      multipart_chunksize=self.__multipart_chunksize,
      multipart_threshold=self.__multipart_chunksize,
      max_concurrency=self.__max_threads,
      io_chunksize=self.__io_chunksize,
      use_threads=True, 
    ))
  
  def url(self, key):
    return  f'https://{self.__bucket}.s3.{self.__region}.amazonaws.com/{key}'
  
  def list_objects(self):
    return self.get_client().list_objects(Bucket=self.__bucket).get("Contents", [])
  
  def upload(self, s3_dir, files, is_public = True, progress_bar=None, use_default_progress_bar=False):
    if (progress_bar is None):
      if (use_default_progress_bar):
        progress_bar = self.__progress_handler
        
        self.__progress_data = {
          "bytes": 0,
          "size": 0,
          "pos": 0,
        }
    
    tm = self.__make_transfer_manager()
    
    for filename in ([files] if (files is str) else files):
      if (use_default_progress_bar):
        self.__progress_data["size"] += os.path.getsize(filename)
        
      tm.upload(
        filename, 
        self.__bucket, 
        os.path.join(s3_dir, os.path.basename(filename)), 
        ({'ACL':'public-read'} if is_public else None), 
        ([ProgressCallbackInvoker(progress_bar)] if progress_bar else None)
      )
    
    tm.shutdown()