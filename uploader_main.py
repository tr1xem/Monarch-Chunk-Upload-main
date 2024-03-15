import os
import requests
import argparse
from pathlib import Path
import math 
api_url = "https://api.monarchupload.cc/v3/upload"

CHUNK_SIZE = 5242880
MAX_RETRY = 3

# Function to read a file in chunks similar to the JavaScript code
def read_in_chunks(file_path, chunk_size):
    global total_chunks
    total_chunks = math.ceil(os.path.getsize(file_path) / chunk_size)
    chunk_no = 0
    with open(file_path, "rb") as file:
        
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk, chunk_no
            chunk_no += 1



def print_progress_bar(percent):
    bar_length = 50
    num_blocks = int(percent / 100 * bar_length)
    progress_bar = "[" + "#" * num_blocks + " " * (bar_length - num_blocks) + "]"
    #os.system("cls")
    print(f"\rProgress: {progress_bar} {percent:.2f}%", end="\n", flush=True)

# Upload your file by breaking it into chunks and sending each piece
def upload(file, url ="https://api.monarchupload.cc/v3/upload"):
    api_url = "https://api.monarchupload.cc/v3/upload"
    apiKey = "api_key"
    chunked = True
    global total_chunks
    content_name = os.path.basename(file)
    content_path = os.path.abspath(file)
    content_size = os.path.getsize(content_path)
    os.system("cls")
    print(content_name, content_path, content_size )

    with open(content_path, "rb") as f:
        index = 0
        headers = {}

        for chunk, chunk_no in read_in_chunks(content_path, CHUNK_SIZE):
#            print(content_name, content_path, content_size )
            offset = index + len(chunk)
            index = offset
            first_chunk = chunk_no == 0
            if offset == content_size:
                last_chunk = "true"
            else:
                last_chunk = "false"
      #      headers["Content-Type"] = "multipart/form-data" 
            
           # headers['Content-Range'] = 'bytes %s-%s/%s' % (index - len(chunk), offset - 1, content_size)
            headers = {
                "name ":"file",
                'filename':content_name,
                'secret': apiKey,
                'chunked': "true",
                'private':"false",
                'lastchunk': str(last_chunk),
                "content-type": "multipart/form-data",
              #  "content-range": 'bytes %s-%s/%s' % (index - len(chunk), offset - 1, content_size)
            }

            percent = (chunk_no / total_chunks) * 100
            print_progress_bar(percent)
            retry_count = 0
           # while retry_count < MAX_RETRY:
            try:
                files = {"file": (content_name,chunk),
                "filename" : content_name}
                r = requests.post(url, data=headers , files=files)
                response_json = r.json()
                if last_chunk == "true":
                    os.system("cls")
                    print("Upload Successful" , response_json["data"]['url'])
                    
                else:
                    os.system("cls")
                    print("Total Chunks:" , total_chunks , "\nSuccessfully uploaded chunk no. " , chunk_no + 1)               

                
            except Exception as e:
                print(e)
                pass
                """print("Upload failed, retrying...")
                retry_count += 1
                if retry_count == MAX_RETRY:
                    print("Maximum retry attempts reached. Upload failed.")
                    return
                    
                    """
                    

# Add a path to the file you want to upload, and away we go! 




def main():
    parser = argparse.ArgumentParser(description="Upload a file to monarchupload.cc API")
    parser.add_argument("file_name", help="Name of the file to upload")
    parser.add_argument("--private", action="store_true", help="Set to make the file private (password-protected)")
    parser.add_argument("--file_key", help="Password to unlock the password-protected file")
    parser.add_argument("--chunked", action="store_true", help="Set for chunked upload")
    parser.add_argument("--last_chunk", action="store_true", help="Set to true on the last file chunk in chunked upload")
    
    args = parser.parse_args()

    file_path = Path(args.file_name).resolve()
    
    try:
        if not file_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        upload(file_path , api_url)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
