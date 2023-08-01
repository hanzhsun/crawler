import requests

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    params = { 'id' : id, 'confirm' : 1 }
    response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    print(destination+'start')
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    print(destination+'done')

if __name__ == "__main__":
    path = './so-vits-svc/logs/44k/'
    d_id = '1BVFFOXR62I9AVDc5hfonOmRmuotAbANt'
    d_des = path + 'D_0.pth'
    download_file_from_google_drive(d_id, d_des)
    g_id = '1jJ_URYDczTw33fMizBZ5zTmmiLjUUK6f'
    g_des = path + 'G_0.pth'
    download_file_from_google_drive(g_id, g_des)