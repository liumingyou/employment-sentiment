import os
import re
import random
import datetime
import pandas as pd
import requests
from time import sleep


def trans_time(v_str):
    """Convert GMT time to standard format"""
    GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
    timeArray = datetime.datetime.strptime(v_str, GMT_FORMAT)
    ret_time = timeArray.strftime("%Y-%m-%d %H:%M:%S")
    return ret_time


def tran_gender(gender_tag):
    """Convert gender"""
    gender_dict = {'m': '男', 'f': '女', '-1': '未知'}
    return gender_dict.get(gender_tag, '未知')


def search_weibo(keyword_list):
    """
    Search Weibo and return related Weibo IDs
    :param keyword_list: List of search keywords
    :return: List of Weibo IDs
    """
    weibo_ids = []
    for keyword in keyword_list:
        url = f'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{keyword}&page_type=searchall'
        headers = {
            "user-agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "referer": "https://m.weibo.cn/search/",
            "x-requested-with": "XMLHttpRequest",
            "cookie": "SCF=AhqvF-ZBJQvh3CXFexObHSqIt46i0wyDnDpjVo4j36IARJs8RHsR4dS8VnzOG2lQ2uIsw6hfRSG5w4gkpRlPlNs.; SUB=_2A25EGBfhDeRhGeFH6VoV9CvIzj6IHXVnVBUprDV6PUJbktAbLVLCkW1Ne5DijFdEMa8vkjMegWED0We2iT4fSYd6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhVSpCT11H_oVm6kpq_ZpeN5JpX5KMhUgL.FoM4eonXSh-XSKz2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoM4e0MpSh-RSoM0; SSOLoginState=1763469233; ALF=1766061233; MLOGIN=1; _T_WM=66754943900; WEIBOCN_FROM=1110006030; XSRF-TOKEN=dbc615; M_WEIBOCN_PARAMS=oid%3D5233272570774230%26luicode%3D10000011%26lfid%3D102803%26uicode%3D10000011%26fid%3D231583"
        }

        try:
            r = requests.get(url, headers=headers, timeout=10)
            print(f"Search status code: {r.status_code}")

            if r.status_code == 200:
                response_data = r.json()
                print("Search successful, parsing data...")

                if 'data' in response_data:
                    data = response_data['data']
                    if 'cards' in data:
                        cards = data['cards']
                        card_count = 0
                        for card in cards:
                            if card.get('card_type') == 9:
                                mblog = card['mblog']
                                weibo_id = str(mblog['id'])
                                if weibo_id not in weibo_ids:
                                    weibo_ids.append(weibo_id)
                                    card_count += 1
                                    print(f"Found Weibo ID: {weibo_id}")
                        print(f"Found {card_count} weibos for this keyword")
                    else:
                        print("No 'cards' field in response")
                else:
                    print("No 'data' field in response")
            else:
                print(f"Search failed, status code: {r.status_code}")

        except Exception as e:
            print(f"Search error: {e}")
            continue

    return weibo_ids


def get_comments(v_weibo_ids, v_comment_file, v_max_page):
    """
    Crawl Weibo comments
    :param v_weibo_id: List of Weibo IDs
    :param v_comment_file: Output filename
    :param v_max_page: Maximum pages to crawl
    :return: None
    """
    for weibo_id in v_weibo_ids:
        print(f"\nProcessing Weibo ID: {weibo_id}")
        max_id = '0'

        for page in range(1, v_max_page + 1):
            wait_seconds = random.uniform(1, 3)
            print(f'Waiting {wait_seconds:.2f} seconds')
            sleep(wait_seconds)

            print(f'Starting to crawl page {page}')
            if page == 1:
                url = f'https://m.weibo.cn/comments/hotflow?id={weibo_id}&mid={weibo_id}&max_id_type=0'
            else:
                if max_id == '0':
                    print('max_id is 0, stop crawling')
                    break
                url = f'https://m.weibo.cn/comments/hotflow?id={weibo_id}&mid={weibo_id}&max_id_type=0&max_id={max_id}'

            headers = {
                "user-agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
                "accept": "application/json, text/plain, */*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
                "referer": f"https://m.weibo.cn/detail/{weibo_id}",
                "x-requested-with": "XMLHttpRequest",
                "cookie": "SCF=AhqvF-ZBJQvh3CXFexObHSqIt46i0wyDnDpjVo4j36IARJs8RHsR4dS8VnzOG2lQ2uIsw6hfRSG5w4gkpRlPlNs.; SUB=_2A25EGBfhDeRhGeFH6VoV9CvIzj6IHXVnVBUprDV6PUJbktAbLVLCkW1Ne5DijFdEMa8vkjMegWED0We2iT4fSYd6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhVSpCT11H_oVm6kpq_ZpeN5JpX5KMhUgL.FoM4eonXSh-XSKz2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoM4e0MpSh-RSoM0; SSOLoginState=1763469233; ALF=1766061233; MLOGIN=1; _T_WM=66754943900; WEIBOCN_FROM=1110006030; XSRF-TOKEN=dbc615; M_WEIBOCN_PARAMS=oid%3D5233272570774230%26luicode%3D10000011%26lfid%3D102803%26uicode%3D10000011%26fid%3D231583"
            }

            try:
                r = requests.get(url, headers=headers, timeout=10)
                print(f"Comment request status code: {r.status_code}")

                if r.status_code == 200:
                    response_data = r.json()
                    if 'data' in response_data:
                        comment_data = response_data['data']
                        max_id = comment_data['max_id']

                        if 'data' in comment_data and comment_data['data']:
                            datas = comment_data['data']
                            print(f"Found {len(datas)} comments on this page")

                            page_list = []
                            id_list = []
                            text_list = []
                            time_list = []
                            source_list = []
                            user_id_list = []
                            user_gender_list = []

                            for data in datas:
                                if str(data['id']) in id_list:
                                    continue
                                page_list.append(page)
                                id_list.append(str(data['id']))
                                dr = re.compile(r'<[^>]+>', re.S)
                                text2 = dr.sub('', data['text'])
                                text_list.append(text2)
                                time_list.append(trans_time(v_str=data['created_at']))
                                source_list.append(data['source'])
                                user_id_list.append(data['user']['id'])
                                user_gender_list.append(tran_gender(data['user']['gender']))

                            if id_list:
                                df = pd.DataFrame({
                                    'max_id': max_id,
                                    '微博id': [weibo_id] * len(time_list),
                                    '评论页码': page_list,
                                    '评论id': id_list,
                                    '评论时间': time_list,
                                    '评论者IP归属地': source_list,
                                    '评论者id': user_id_list,
                                    '评论者性别': user_gender_list,
                                    '评论内容': text_list,
                                })

                                if os.path.exists(v_comment_file):
                                    header = False
                                else:
                                    header = True

                                df.to_csv(v_comment_file, mode='a+', index=False, header=header, encoding='utf_8_sig')
                                print(f'Successfully saved {len(id_list)} comments to: {v_comment_file}')
                            else:
                                print("No new comments on this page")
                        else:
                            print("No comment data")
                    else:
                        print("No 'data' field in comment response")
                else:
                    print(f"Comment request failed, status code: {r.status_code}")

            except Exception as e:
                print(f'Comment crawling error: {e}')
                continue


if __name__ == '__main__':
    keyword_list = ['毕业生找工作']

    print("Starting Weibo search...")
    weibo_id_list = list(set(search_weibo(keyword_list)))
    print(f"\nFound {len(weibo_id_list)} Weibo IDs: {weibo_id_list}")

    if weibo_id_list:
        max_page = 10
        comment_file = '毕业生找工作.csv'

        if os.path.exists(comment_file):
            os.remove(comment_file)
            print(f"Deleted old file: {comment_file}")

        print("\nStarting comment crawling...")
        get_comments(v_weibo_ids=weibo_id_list, v_comment_file=comment_file, v_max_page=max_page)
        print("Crawling completed!")
    else:
        print("No related weibos found, program ended")