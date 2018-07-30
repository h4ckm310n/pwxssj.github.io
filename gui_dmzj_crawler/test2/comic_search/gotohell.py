def run_search(self, result_search):
    tree_search = etree.HTML(result_search.text)
    page_search = tree_search.xpath(
        '//div[@class="bottom_page page"]/a[text()!="上一页"][text()!="下一页"]/text()')

    i_comic_sum = 0
    title_search_sum = []
    auth_search_sum = []
    latest_search_sum = []
    link_search_sum = []

    for i_page_search in range(0, len(page_search)):
        result_search = requests.get(self.url_search + '/' + page_search[i_page_search])
        tree_search = etree.HTML(result_search.text)

        page_search = tree_search.xpath(
            '//div[@class="bottom_page page"]/a[text()!="上一页"][text()!="下一页"]/text()')

        title_search = tree_search.xpath('//ul[@class="update_con autoHeight"]/li/a[1]/@title')
        auth_search = tree_search.xpath('//p[@class="auth"]/text()')
        latest_search = tree_search.xpath('//p[@class="newPage"]/text()')
        link_search = tree_search.xpath('//ul[@class="update_con autoHeight"]/li/a/@href')

        # 该页漫画信息

        for i_comic in range(0, len(title_search)):
            title_search_sum.append(title_search[i_comic])
            auth_search_sum.append(auth_search[i_comic])
            latest_search_sum.append(latest_search[i_comic])
            link_search_sum.append(link_search[i_comic])

            i_comic_sum = i_comic_sum + 1
    self.state.emit(3)
    self.result.emit([title_search_sum, auth_search_sum, latest_search_sum, link_search_sum, i_comic_sum])
