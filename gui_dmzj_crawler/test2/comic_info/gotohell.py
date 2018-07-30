'''headers = {'referer': self.url}
r_cover = requests.get(cover_url, headers=headers)
self.cover = r_cover.content

self.state = tree.xpath('//div[@class="anim-main_list"]/table/tr[5]/td/text()')
self.intro = tree.xpath('//div[@class="line_height_content"]/text()')
self.vols = tree.xpath('//div[@class="cartoon_online_border"]/ul/li/a/text')
self.vols_urls = tree.xpath('//div[@class="cartoon_online_border"]/ul/li/a/@href')
self.info_state.emit(3)
self.info.emit([self.title, self.cover, self.auth, self.latest, self.state, self.intro, self.vols, self.vols_urls])'''