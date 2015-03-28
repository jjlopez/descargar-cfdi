class Header:

    def __init__(self):
        self.__user_agent = ('Mozilla/5.0 '
                             '(Windows NT 6.1; WOW64; Trident/7.0; AS; '
                             'rv:11.0) like Gecko')
        self.__accept = ('text/html,application/xhtml+xml,application/xml;'
                         'q=0.9,*/*;q=0.8')

    def obtener(self, host, referer):
        encabezado = {
            'Accept': self.__accept,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': host,
            'Referer': referer,
            'User-Agent': self.__user_agent,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        return encabezado

    def obtener_ajax(self, host, referer):
        encabezado = {
            'Accept': self.__accept,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': host,
            'Referer': referer,
            'User-Agent': self.__user_agent,
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-MicrosoftAjax': 'Delta=true',
            'x-requested-with': 'XMLHttpRequest',
            'Pragma': 'no-cache'
        }
        return encabezado
