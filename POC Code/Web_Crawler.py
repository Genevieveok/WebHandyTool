__author__ = 'Abe'
import subprocess
from bs4 import BeautifulSoup
from urllib2 import *
import datetime
import urllib2
import re
from urllib import urlretrieve

class Web_Crawler(object):

    """
    Main class, it is for crawling.
    Class variable includes depth,algo,choices,choice,output,seed,list of links
    """
    def __init__(self):
        self.depth = 0
        self.algo = 'bfs'
        self.choices = {'1':'download', '2':'error', '3':'search', '4':'crawl','5':'web Depth'}
        self.search_choices = {'1':'exact', '2':'similar'}
        self.choice = self.choices['4'] #the default is crawl
        self.search_choice = self.choices['1'] #the default is crawl
        self.output = ""
        self.seed = ""
        self.list_of_links = []
        self.NOT_LINK = ['data','#', ]
        self.SCHEME_HTTP = "http"
        self.SCHEME_HTTPS = "https"
        self.SUPPORTED_SCHEMES = (self.SCHEME_HTTP, self.SCHEME_HTTPS)

    def option(self):
        """
        Gets user input to set various program options related to
        how the user would like to handle crawling a webpage.

        Ask for users option choices

        :return:
        """
        choice = raw_input("Choose your option \n"
                           + "Download Resources = 1 \n"
                           + "Check for Errors = 2 \n"
                           + "Search for Query = 3 \n"
                           + "Just Crawl = 4  \n"
                           + "Web Depth= 5  \n")

        self.choice = self.choices.get(choice)
        print self.choices.get(choice)

        link = raw_input("Website you would like use: ")
        link = self.HTML_corrector(link).geturl()

        self.depth_setter(input("Choose a depth of 0 or greater to parse the website using."));
        #parseType = raw_input("Would you like to do a breadth-first (0) or depth-first (1) search?");
        print self.depth
        self.choice = self.choices.get(choice)

        if self.choice == "download":
            self.download_resources(link)

        elif self.choice == "error":
            self.list_of_links = crawler.bfs(link)
            self.check_errors(link,self.list_of_links)

        elif self.choice == "search":
            self.list_of_links = crawler.bfs(link)
            # indexes = self.exact_query('ehima',self.HTML_text(link))
            # print indexes
            # for i in range(0,len(indexes)):
            #     print self.HTML_text(link)[indexes[i]-30:indexes[i]+30]
            choice = raw_input("Choose your option \n"
                       + "Exact Search = 1 \n"
                       + "Similar Search = 2 \n")


            self.search_choice = self.search_choices.get(choice)
            print self.search_choices.get(choice)
            query = raw_input("What's your query: ")
            crawler.query_search(query,link,self.list_of_links,self.search_choice)

        elif self.choice == "crawl":
            self.list_of_links = crawler.bfs(link)
            print self.list_of_links

        elif self.choice == "web structure":
            print "===================================================="
            print "\t\t\tWeb Tree"
            print "===================================================="
            self.website_Depth(link,self.depth)

        else:
            print "Incorrect input."

    def dfs(self, choice):
        #TODO implement
        pass
        
    def bfs(self, link):
        """
        Finds all the links on a give website using the BFS algorithm
        :param link:
        :return A list of all the links found by BFS:
        """

        count = 0
        base_link = self.HTML_corrector(link)
        current_depth = [link]
        next_depth = []
        links = []
        while count <= self.depth:
            print "Depth " + str(count)
            print "LINKS USED IN DEPTH " + str(count)
            print current_depth
            for link in current_depth:
                links.append(self.HTML_corrector(link).geturl())
                correct_link = self.absolute_HTML_corrector(link,base_link).geturl()
                new_links = self.find_links(correct_link)
                if new_links:
                    for link in new_links:
                        next_depth.append(self.absolute_HTML_corrector(link,base_link).geturl())
                    print "Links on this page: " + str(correct_link) + " HERE is the list: "
                    print new_links

            print "ALL LINKS FOUND IN DEPTH " + str(count)
            print next_depth

            current_depth = next_depth
            next_depth = []
            count += 1
        return links

    def HTML_corrector(self,link):
        """
        Fixes the link passed in such that it becomes either a functioning link or is flagged as a broken link.
        :param link:
        :return  Url object of split url result corrected link Ex; SplitResult(scheme=u'http', netloc=u'canvasgroup.ca', path=u'/zdfzd', query=u'', fragment=u'') :
        """
        HTML_corrector_helper = HTML_corrector_help()
        if not link:
            raise ValueError('The URL must not be empty')
        split_result = urlparse.urlsplit(link)

        if not split_result.scheme:
            if split_result.netloc:
                url = self.SCHEME_HTTP + ":" + link
            else:
                url = self.SCHEME_HTTP + "://" + link
            split_result = urlparse.urlsplit(url)

        split_result = HTML_corrector_helper.convert_iri_to_uri(split_result)

        return split_result

    def absolute_HTML_corrector(self,link,base_link_split):
        """
        Takes in the base url and appends any relative or absolute links to the base urk.

        :param link:
        :param base_link_split:
        :return Url object of split url result corrected link Ex; SplitResult(scheme=u'http', netloc=u'canvasgroup.ca', path=u'/zdfzd', query=u'', fragment=u'') ::
        """
        new_link = urlparse.urljoin(base_link_split.geturl(), link)

        return self.HTML_corrector(new_link)

    def download_resources(self,link,options = '-rA', file_type=None):
        """
        Writes all resources matching the given file type from the page link to the file specified by destination.

        :param link:
        :param options:
        :param file_type:
        :return:
        """

        file_type = raw_input("Enter the extension you would like to download: ")
        more_request = raw_input('Do you want more, enter Y or N: ')

        while more_request.lower() == 'y':
            more_file_type = raw_input("Enter the next extension you would like to download: ")
            file_type+= "," + more_file_type
            print file_type
            more_request = raw_input('Do you want to enter more extensions? Enter Y or N:')

        if file_type:
            # Call UNIX wget process to download files
            p = subprocess.call(["wget",options,file_type,link])
        else:
            p = subprocess.call(["wget",options,link])


    def exact_query(self,query,data):
        """
        Searches through a String for a certain phrase or term. Returns the starting index for all occurrences of the query String.
        If the query is not located, it will return an empty array.

        :param query - The String we are looking for:
        :param data - The String we are searching through.:
        :return Indexes corresponding to the beginning of the location of the String in question.:
        """
        locations = [];
        queryIndex = 0;
        
        data.strip();
        query.strip();
        query = query.lower();
        data = data.lower();
                                                    # Impossible for data to contain query or query is nonsensical.
        if len(query) > len(data) or (len(query) == len(data) and not query is data) or len(query) == 0: 
            return [];
        
        for i in range(0, len(data)):
            if data[i] == query[queryIndex]:        # Current location is matching the query pattern so far.
                if queryIndex == len(query) - 1:    # The whole query pattern is matched, add starting index.
                    locations.append(i - len(query) + 1);
                    queryIndex = 0;
                else:
                    queryIndex += 1;
                
            else:                                   #Current location didn't match the pattern.
                if data[i] == query[0]:
                    queryIndex = 1;
                else:
                    queryIndex = 0;   
                
        return locations;

    def similar_query(self, query, data, proximity):
        """
        Searches through a String for a certain phrase or term. Returns results that are close to the query as well.
        (i.e. "ap ple" or "bpple" would be noted for "apple") Returns the starting index for all occurrences of Strings sufficiently close to
        the query. If the query is not located, it will return an empty array.

        :param: query  - The String we are looking for.
        :param: data - The String we are searching through.:
        :param: proximity - The size of the acceptable variation from the query.:
        :return:Indexes corresponding to the beginning of the location of the String in question.
        """
        locations = [];
        queryIndex = 0;
        distance = 0;
        
        data.strip();
        query.strip();
        query = query.lower();
        data = data.lower();
        
        if len(query) > len(data) or (len(query) == len(data) and not query is data) or len(query) == 0 or proximity > (0.4) * len(query):
            return [];
        
        for i in range(0, len(data)):
            if data[i] == query[queryIndex]:
                if queryIndex == len(query) - 1:
                    locations.append(i - len(query) + 1);
                    queryIndex = 0;
                    distance = 0;
                else:
                    queryIndex += 1;
            elif distance < proximity:
                if queryIndex == len(query) - 1:
                    locations.append(i - len(query) + 1);
                    queryIndex = 0;
                    distance = 0;
                elif self.whitespace_checker(data[i]):
                    distance += 1;
                else:
                    distance += 1;
                    queryIndex += 1;
            else:
                if data[i] == query[0]:
                    queryIndex = 0;
                    distance = 0;
                else:
                    queryIndex = 0;
                    distance = 0;

        return locations;

    def whitespace_checker(self,character):
        """
        Returns true if the character passed in is a whitespace character such as tab, space or newline.

        :param character - The character to be checked.:
        :return boolean, if there is whitespace True,Whether the character is whitespace:
        """
        return character == ' ' or character == '    ' or character == os.linesep;

    def find_links(self,link,destination=None):
        """
        Finds all the links (<a></a> anchor tags on page) on a page, also removes all
        the link that start with '#' or 'data:' as these are not valid urls

        :param link:
        :param destination:
        :return List of Links:
        """

        HTML_corrector_helper = HTML_corrector_help()

        data = self.BS_parse_data(link)
        if data == 'HTTP Error':
            return False
        links = []

        if destination:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
            f = open('Found Links at' +timestamp +'.txt','w')
            f.write(data.find_all('a'))
            f.close()

        for link in data.find_all('a'):
            links.append(link.get('href'))

        links = [link for link in links if HTML_corrector_helper.is_link(link)]

        # More understandable version of code above
        #list_of_valid_links = []
        #for link in links:
        #    if self.is_link(link):
        #       list_of_valid_links.append(link)

        return links

    def check_errors(self,link,list_of_links=None):
        """
        Checks the all the links and reports the error message associated with
        all the links inputted

        :param link:
        :param list_of_links:
        :return List of Errors:
        """

        status_msg_list = []
        base_url = self.HTML_corrector(link)


        if list_of_links:
            for link in list_of_links:
                corrected_link = self.absolute_HTML_corrector(link,base_url).geturl()
                request = urllib2.Request(corrected_link)

                try:
                   response = urllib2.urlopen(request)
                   success = 'Status code: ' + str(response.getcode())
                   print str(corrected_link) + ' -- ' + success
                   status_msg_list.append(str(corrected_link) + ' -- ' + success)

                except urllib2.HTTPError, e:
                   error = 'Error code: ' + str(e.code)
                   print str(corrected_link) + ' -- ' + error
                   status_msg_list.append(str(corrected_link) + ' -- ' + error)

            return status_msg_list

        else:
            base_url = base_url.geturl()
            request = urllib2.Request(base_url)
            try:
               response = urllib2.urlopen(request)
               success = response.getcode()
               print str(base_url)  + ' -- ' + success

            except urllib2.HTTPError, e:
               error = 'Error code: ' + str(e.code)
               print str(base_url)  + ' -- ' + error

               return str(base_url) + ' -- ' + error

            return str(base_url) + ' -- ' + success

    def BS_parse_data(self,link):
        """
        Returns BeautifulSoup object for the link given, this will allow modules parse through pages data much faster

        :param link:
        :return BeautifulSoup :
        """

        try:
            soup = BeautifulSoup(urlopen(link),"html.parser")
        except urllib2.HTTPError:
            soup = 'HTTP Error'

        return soup
    
    def HTML_text(self,link):
        """
        Returns HTML text data for Query search

        :param link:
        :return String :
        """

        try:
            soup = BeautifulSoup(urlopen(link),"html.parser")
            data = re.sub(r'\n\s*\n', r'\n\n', soup.get_text().strip(), flags=re.M)
        except urllib2.HTTPError:
            soup = 'HTTP Error'
            return soup
        return data

    def query_search(self,query,link,list_of_links = None,choice='exact'):
        """
        Find queries

        :param query:
        :param data:
        :param choice:
        :return Query results:
        """
        if list_of_links:
            print 'Links searching...'
            print list_of_links
            for link in list_of_links:
                data = self.HTML_text(link)
                if self.search_choice == "exact":
                    print 'Hey Buddy...I just searched ' + str(link)
                    indexes = self.exact_query(query,data)
                    print indexes
                    for index in indexes :
                        print 'Found at index ' + str(index)
                        print '---------------------------------------------'
                        print data[index-30:index+30]
                        print '---------------------------------------------'

                elif self.search_choice == "similar":
                    proximity = raw_input("Set the promixity of similar query: ")
                    print 'Hey Buddy...I just searched ' + str(link)
                    indexes = self.similar_query(query,data,proximity)
                    print indexes
                    for index in indexes:
                        print 'Found at index ' + str(index)
                        print '---------------------------------------------'
                        print data[index-30:index+30]
                        print '---------------------------------------------'
        else:
            data = self.HTML_text(link)
            if self.search_choice == "exact":
                indexes = self.exact_query(query,data)
                print indexes
                for index in indexes :
                    print 'Found at index ' + str(index)
                    print '---------------------------------------------'
                    print data[index-30:index+30]
                    print '---------------------------------------------'

            elif self.search_choice == "similar":
                proximity = raw_input("Set the promixity of similar query: ")
                indexes = self.similar_query(query,data,proximity)
                print indexes
                for index in indexes:
                    print 'Found at index ' + str(index)
                    print '---------------------------------------------'
                    print data[index-30:index+30]
                    print '---------------------------------------------'

        return indexes

    def depth_setter(self, depth):
        """
        Sets the default max depth variable for the web crawler
        :param depth:
        :return:
        """

        self.depth = depth

    def website_Depth(self,link,depth):
        """
        It provides a structured model of the website and other site the initial site is connect to. It displays
        a hierarchy that will show users how crawled link interact with each other. Shows all the depths

        :param link:
        :param depth:
        :return A pretty print of Hierarchy:
        """
        crawler.bfs(link)
class HTML_corrector_help(object):
    """
    Library of helper functions that are used by HTML corrector to
    fix url links.
    """
    def __init__(self):
        self.NOT_LINK = ['data','#', ]
        
    def is_link(self,url):
        """
        Return True if the url is not base 64 data or a local ref (#)

        :param url:
        :return Boolean either True or False:
        """

        for prefix in self.NOT_LINK:
            try:
                if url.startswith(prefix):
                    return False
            except AttributeError as e:
                pass
        return True

    def convert_iri_to_uri(self,url_split):
        """
        Attempts to convert potential IRI to URI.

        IRI may contain non-ascii characters.
        :param url_split:
        :return:
        """
        new_parts = []
        for i, part in enumerate(url_split):
            if i == 1:
                # domain name
                new_parts.append(part.encode('idna').decode('ascii'))
            else:
                # other parts such as path or query string.
                new_parts.append(self.url_encode_non_ascii(part))
        return urlparse.SplitResult(*new_parts)

    def url_encode_non_ascii(self,url_part):
        """
        For each byte in url_part, if the byte is outside ascii range, quote the
        byte. UTF characters that take two bytes will be correctly converted using
        this technique.

        We do not quote the whole url part because it might contain already quoted
        characters, which would then be double-quoted.

        The url part is converted from utf-8 and then to utf-8, which might not
        always work if there is mixed or bad encoding.
        :param url_part:
        :return:
        """
        return re.sub(
            b'[\x80-\xFF]',
            lambda match: quote(match.group(0)).encode("utf-8"),
            url_part.encode("utf-8")).decode("ascii")

if __name__ == '__main__':
    crawler = Web_Crawler()
    option = crawler.option()

