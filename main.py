import re
import requests
import urllib.request

client_id = ""  # put your client-id here
api_url = 'https://api.twitch.tv/helix/clips?id='


# Remove all non clip-ID related stuff from link with huge if block
# There are 3 types of clip links + straight ID we need to remove all non ID stuff and make api url
def make_giga_url(url):
    url = str(url)  # in case of non str input
    end_check = url.find('?filter')
    # print(end_check)
    start_check = url.find('clip/')
    # print(start_check)
    extra_check = url.find('clips.twitch.tv/')
    # print(url[start_check:end_check][5:])
    # print(extra_check)
    if extra_check != -1:
        main_url = api_url + url[extra_check:][16:]
    elif end_check == -1 and start_check == -1:
        main_url = api_url + url
    elif end_check == -1:
        main_url = api_url + url[start_check:][5:]
    else:
        main_url = api_url + url[start_check:end_check][5:]
    return main_url


# Downloading video from api link
def get_vid(url):
    # print(url)
    headers = {'Client-ID': client_id, "Accept": "application/vnd.twitchtv.v5+json"}
    response = requests.get(url, headers=headers)
    # print(response)
    # print(response.text)
    # print(response.status_code)
    if response.status_code == 401:  # if you are not authorized
        print('Invalid Client-ID')
        exit(-1)
    response = response.json()
    # print(response['data'])
    if not response['data']:  # check if twitch return data
        print('Post link or ID of clip bro, not that shit')
        return None
    user_name = response['data'][0]['broadcaster_name']  # basically search all info to make your video looks pretty
    pic_url = response['data'][0]['thumbnail_url']
    title = response['data'][0]['title']
    slice_point = pic_url.index("-preview-")
    mp4_url = pic_url[:slice_point] + '.mp4'
    regex = re.compile('[^a-zA-Z0-9_]') # replacing all not appropriate symbols
    title = title.replace(' ', '_')
    out_filename = regex.sub('', title) + '.mp4'
    output_path = ("E:\\TwitchClips" + '\\' + user_name + '-' + out_filename)  # change your path where to save here
    print('Downloading ' + out_filename)
    urllib.request.urlretrieve(mp4_url, output_path)
    print('Done. file placed at: ' + output_path)
    # print(title)
    # print(mp4_url)


def main():
    while True:
        print('Press Enter or Ctrl+Z to stop, otherwise paste the link')
        link = input()
        if link == '':
            break
        giga_url = make_giga_url(link)
        get_vid(giga_url)


if __name__ == '__main__':
    main()
