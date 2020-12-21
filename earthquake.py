#!/bin/env python
import re
import os
import requests
import json
import sys
import settings
from bs4 import BeautifulSoup

class Earthquake(object):

    # setting.py include
    # init settings
    def __init__(self):
        self.file_url = os.path.join(
                            os.path.dirname(__file__),
                            settings.FILE
                            )
        self.session = requests.session()
        self.reqest = self.session.get(
                            settings.URL,
                            timeout=20,
                            headers=settings.UA
                            )
        if self.reqest.status_code != 200: sys.exit()
        self.soup = BeautifulSoup(
                            self.reqest.content, 
                            "lxml", 
                            from_encoding='utf-8'
                            )

    def data(self):
        element = self.soup.find_all("small")
        try:
            image = self.soup.find_all(
                            "div",
                            attrs={"id": "earthquake-01"}
                            )[0].find("img")['src']
        except IndexError:
            return None

        message = [x.text.strip() for x in element]
        chg_msg = (
                  message[10].replace('/', '／')
                + "　　：" + message[11].replace('/', '／')
                )

        output = (
                message[0] + "　　　：" + message[1] + "\n"
                + message[2] + "　　　　：" + message[3] + "\n"
                + message[4] + "　　　：" + message[5] + "\n"
                + message[6] + "：" + message[7] + "\n"
                + message[8] + "　　　　　：" + message[9] + "\n"
                + chg_msg + "\n" + message[12] + "　　　　　："
                + re.sub("。","。\n　　　　　　　：",message[13][:-1])
                + "\n電車情報　　　：" + settings.TRAIN + "\n"
                )

        data_check = (
                message[1] + "\n"
                + message[3] + "\n"
                + message[5]
                )

        if "津波情報" in message[13]:
            output += (
                    "津波情報　　　：" + settings.TSUNAMI + "\n"
                    + "ハザードマップ：" + settings.HAZARD
                    + message[3].split("県")[0] + "県>\n"
                    )

        if message[5] != "---":
            e = re.match(r'([0-7]+)', message[5])

            # an earthquake with an intensity of 4 or more.
            if int(e.group(0)) >= 4:
                with open(self.file_url) as f: text = f.read()
                if text != data_check:
                    with open(self.file_url, mode="w") as f: f.write(data_check)
                    return output,image

def main():
    eq = Earthquake() 
    eq_content = eq.data()
    headers = {'Content-Type': 'application/json'}
    if eq_content != None:
        eq_data = eq_content[0]
        eq_image = eq_content[1]
        embeds = [
                    {
                       'color': 16718337,
                       'image': {
                          'url': eq_image 
                       }
                    }
                 ]
        eq_content = {
                       "content" : eq_data,
                       "embeds" : embeds
                     }

        requests.post(
                    settings.TESTSRV,
                    data=json.dumps(eq_content),
                    headers = headers
                    )

        requests.post(
                    settings.YUNSRV,
                    data=json.dumps(eq_content),
                    headers = headers
                    )
        requests.post(
                    settings.MAMANSRV,
                    data=json.dumps(eq_content),
                    headers = headers
                    )

if __name__ == "__main__": main()
